import time, requests, re, asyncio, aiohttp
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import errors

from app.db.session import get_raw_db
from log import logger

semaphore = asyncio.Semaphore(10)  # Limit concurrent requests to 10


def check_connection():
    try:
        # get_raw_db 컨텍스트 매니저를 사용하여 MongoDB 연결 시도
        with get_raw_db() as db:
            # 서버 상태 확인
            db.command("ping")
            print("MongoDB connection: Success")
    except errors.ServerSelectionTimeoutError as err:
        # 연결 실패시 에러 메시지
        print("MongoDB connection: Failed", err)
        logger.error(f"Error when Connection db : {err}")
        raise


def inch_to_cm(data: str, is_reach=False):
    """
    Inches를 센티미터로 변환합니다.

    :param data: 변환할 데이터 문자열 (예: "6'0"").
    :param is_reach: True일 경우, 리치 데이터로 간주하여 다르게 처리합니다.
    :return: 변환된 센티미터 값.
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
    """
    파운드를 킬로그램으로 변환합니다.

    :param data: 변환할 데이터 문자열 (예: "170 lbs").
    :return: 변환된 킬로그램 값.
    """
    to_int = round((int(re.sub("[^0-9]", "", data)) / 2.205), 1)
    return to_int


async def fetch_fighter_info_async(session: aiohttp.ClientSession, url: str):
    """
    주어진 URL에서 파이터 정보를 비동기적으로 크롤링합니다.

    :param session: aiohttp 클라이언트 세션.
    :param url: 크롤링할 URL.
    :return: 크롤링된 파이터 정보 리스트.
    """
    async with session.get(url) as response:
        req = await response.text()

    await asyncio.sleep(1)
    html = BeautifulSoup(req, "html.parser")

    fighter_list = []
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
            model_dict["name"] = fighter_info_list[0] + " " + fighter_info_list[1]
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
                0 if fighter_info_list[7] == "--" else int(fighter_info_list[7])
            )
            model_dict["lose"] = (
                0 if fighter_info_list[8] == "--" else int(fighter_info_list[8])
            )
            model_dict["draw"] = (
                0 if fighter_info_list[9] == "--" else int(fighter_info_list[9])
            )
            fighter_list.append(model_dict)
    print("tesettest", url, len(fighter_list))

    return fighter_list


async def fetch_match_info_async(session: aiohttp.ClientSession, url: str) -> dict:
    """
    주어진 URL에서 매치 정보를 비동기적으로 크롤링합니다.

    :param session: aiohttp 클라이언트 세션.
    :param url: 크롤링할 URL.
    :return: 크롤링된 매치 정보 리스트.
    """
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
                datetime.strptime(match_info[0], "%B %d, %Y") if match_info else None
            )

            match_loc = match_info[1] if match_info else None
            match_list = []
            for td in html.find_all(
                "tr",
                "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click",
            ):
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
                model_dict["winner_strike"] = infos[5]
                model_dict["winner_td"] = infos[7]
                model_dict["winner_sub"] = infos[9]
                model_dict["looser"] = infos[2]
                model_dict["looser_strike"] = infos[6]
                model_dict["looser_td"] = infos[8]
                model_dict["looser_sub"] = infos[10]
                model_dict["weight_class"] = infos[11]
                model_dict["finish_method"] = infos[12]
                model_dict["finish_tech"] = infos[13]
                model_dict["finish_round"] = infos[14]
                model_dict["finish_time"] = infos[15]
                match_list.append(model_dict)
    return match_list


async def fetch_all_fighters_info_async():
    """
    모든 알파벳에 대해 UFC 통계 사이트에서 파이터 정보를 비동기적으로 크롤링합니다.

    :return: 모든 알파벳에 대한 크롤링 결과 리스트.
    """
    url_template = "http://www.ufcstats.com/statistics/fighters?char={}&page=all"

    async with aiohttp.ClientSession() as session:
        coroutines_fighter_info = [
            asyncio.create_task(
                fetch_fighter_info_async(session, url_template.format(chr(alphabet)))
            )
            for alphabet in range(ord("a"), ord("z") + 1)
        ]

        res = await asyncio.gather(*coroutines_fighter_info)
    return res


async def fetch_all_matches_info_async():
    """
    UFC 통계 사이트에서 완료된 모든 이벤트의 매치 정보를 비동기적으로 크롤링합니다.

    :return: 크롤링된 모든 이벤트의 매치 정보 리스트.
    """

    url = "http://www.ufcstats.com/statistics/events/completed?page=all"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            res = await response.text()
            html = BeautifulSoup(res, "html.parser")

            coroutines = [
                asyncio.create_task(fetch_match_info_async(session, i["href"]))
                for i in html.find_all("a", "b-link b-link_style_black")
            ]

            res = await asyncio.gather(*coroutines)
    return res


def execute_match_info_fetching():
    """
    크롤링한 게임 데이터를 저장하기 위해 `craw_game` 함수를 실행
    합니다. 실행 결과는 MongoDB에 저장됩니다.
    """
    loop = asyncio.get_event_loop()
    match_data = loop.run_until_complete(fetch_all_matches_info_async())
    save_data_to_database(match_data=match_data)


def execute_fighter_info_fetching():
    loop = asyncio.get_event_loop()
    fighters_data = loop.run_until_complete(fetch_all_fighters_info_async())
    save_data_to_database(fighters_data=fighters_data)


def save_data_to_database(
    fighters_data: List[dict] = None, match_data: List[dict] = None
):
    if fighters_data:
        data_list = [
            {k: (None if v == "" else v) for k, v in fighter.items()}
            for fighter_list in fighters_data
            for fighter in fighter_list
        ]
        with get_raw_db() as db:
            try:
                db["fighters"].delete_many({})
            except Exception as e:
                logger.error(f"Error deleting fighters data: {e}")

            try:
                db["fighters"].insert_many(data_list)
                logger.warning(f"UFC fighters insert : {len(data_list)}")
            except Exception as e:
                logger.error(f"Error save fighters data: {e}")

    elif match_data:
        data_list = [
            {k: (None if v == "" else v) for k, v in match.items()}
            for match_list in match_data
            for match in match_list
        ]
        with get_raw_db() as db:
            try:
                db["fighters"].delete_many({})
            except Exception as e:
                logger.error(f"Error deleting match data: {e}")

            try:
                db["matches"].insert_many(data_list)
                logger.warning(f"UFC matches insert : {len(data_list)}")
            except Exception as e:
                logger.error(f"Error save match data: {e}")
    else:
        return
