import time, requests, re, asyncio, aiohttp
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from db.models import DataFighter, DataMatch
from db.session import get_db

semaphore = asyncio.Semaphore(10)  # Limit concurrent requests to 10


def inch_to_cm(data: str, is_reach=False):
    """
    concert inch(ex.6'7") to cm
    """
    if is_reach:
        reach = round((int(re.sub("[^0-9]", "", data)) * 2.54), 1)
        return reach
    H_feet = data.split(" ")[0]
    H_inch = data.split(" ")[-1]

    H_feet_e = int(re.sub("[^0-9]", "", H_feet)) * 12
    H_inch_e = int(re.sub("[^0-9]", "", H_inch))
    to_cm = round(((H_feet_e + H_inch_e) * 2.54), 1)
    return to_cm


def lbs_to_kg(data: str):
    to_int = round((int(re.sub("[^0-9]", "", data)) / 2.205), 1)
    return to_int


async def craw_fighter_info(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        req = await response.text()

    await asyncio.sleep(1)
    html = BeautifulSoup(req, "html.parser")

    for row in html.find_all("tr"):
        model_dict = {}
        try:
            web_fighter_id = row.find("a", "b-link b-link_style_black")["href"].split(
                "/"
            )[-1]
            model_dict["web_fighter_id"] = web_fighter_id
        except:
            continue
        fighter_info_td = row.find_all("td")

        fighter_info_list = [fighter.text.strip() for fighter in fighter_info_td]
        if fighter_info_list:
            model_dict["first_name"] = fighter_info_list[0]
            model_dict["last_name"] = fighter_info_list[1]
            model_dict["nickname"] = (
                fighter_info_list[2] if fighter_info_list[2] else None
            )
            model_dict["height"] = (
                0 if fighter_info_list[3] == "--" else inch_to_cm(fighter_info_list[3])
            )
            model_dict["weight"] = (
                0 if fighter_info_list[4] == "--" else lbs_to_kg(fighter_info_list[4])
            )
            model_dict["reach"] = (
                0
                if fighter_info_list[5] == "--"
                else inch_to_cm(data=fighter_info_list[5], is_reach=True)
            )
            model_dict["stance"] = (
                0 if fighter_info_list[6] == "--" else fighter_info_list[6]
            )
            model_dict["win"] = (
                0 if fighter_info_list[7] == "--" else fighter_info_list[7]
            )
            model_dict["lose"] = (
                0 if fighter_info_list[8] == "--" else fighter_info_list[8]
            )
            model_dict["draw"] = (
                0 if fighter_info_list[9] == "--" else fighter_info_list[9]
            )


async def craw_match(session: aiohttp.ClientSession, url: str) -> dict:
    async with semaphore:
        async with session.get(url) as response:
            res = await response.text()
            html = BeautifulSoup(res, "html.parser")

            match_info = [
                i.get_text(strip=True).split(":")[1]
                for i in html.find_all("li", class_="b-list__box-list-item")
            ]

            main_event = (
                html.find("span", "b-content__title-highlight").text.strip()
                if html.find("span", "b-content__title-highlight")
                else None
            )
            match_date = (
                datetime.strptime(match_info[0], "%B %d, %Y").date()
                if match_info
                else None
            )
            match_loc = match_info[1] if match_info else None

            for td in html.find_all(
                "tr",
                "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click",
            ):
                # TODO :  save to db
                model_dict = {
                    "main_event": main_event,
                    "match_date": match_date,
                    "match_loc": match_loc,
                }
                infos = [
                    i.text.strip()
                    for i in td.find_all("p", "b-fight-details__table-text")
                ]
                model_dict["winner"] = infos[1]
                model_dict["winner_str"] = infos[5]
                model_dict["winner_td"] = infos[7]
                model_dict["winner_sub"] = infos[9]
                model_dict["looser"] = infos[2]
                model_dict["looser_str"] = infos[6]
                model_dict["looser_td"] = infos[8]
                model_dict["looser_sub"] = infos[10]
                model_dict["weight_class"] = infos[11]
                model_dict["finish_method"] = infos[12]
                model_dict["finish_tech"] = infos[13]
                model_dict["finish_round"] = infos[14]
                model_dict["finish_time"] = infos[15]


async def craw_fighter():
    url_template = "http://www.ufcstats.com/statistics/fighters?char={}&page=all"

    async with aiohttp.ClientSession() as session:
        coroutines_fighter_info = [
            asyncio.create_task(
                craw_fighter_info(session, url_template.format(chr(alphabet)))
            )
            for alphabet in range(ord("a"), ord("z") + 1)
        ]

        await asyncio.gather(*coroutines_fighter_info)


async def craw_game():
    url = "http://www.ufcstats.com/statistics/events/completed?page=all"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            res = await response.text()
            html = BeautifulSoup(res, "html.parser")

            coroutines = [
                asyncio.create_task(craw_match(session, i["href"]))
                for i in html.find_all("a", "b-link b-link_style_black")
            ]

            await asyncio.gather(*coroutines)


def run_craw_game():
    loop = asyncio.get_event_loop()
    match_data = loop.run_until_complete(craw_game())
    save_data_to_database(match_data=match_data)


def run_craw_fighter():
    loop = asyncio.get_event_loop()
    match_data = loop.run_until_complete(craw_fighter())
    save_data_to_database(match_data=match_data)


def save_data_to_database(
    fighters_data: List[dict] = None, match_data: List[dict] = None
):
    if fighters_data:
        data_list = [
            DataFighter(**fighter)
            for fighter_list in fighters_data
            for fighter in fighter_list
        ]
    elif match_data:
        data_list = [
            DataMatch(**match) for match_list in match_data for match in match_list
        ]

    with get_db() as db_session:
        db_session.bulk_save_objects(data_list)
        db_session.commit()
