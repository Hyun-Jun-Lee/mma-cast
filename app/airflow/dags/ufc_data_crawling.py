import asyncio, aiohttp
from bs4 import BeautifulSoup
from datetime import datetime

from utils import inch_to_cm, lbs_to_kg, save_data

semaphore = asyncio.Semaphore(10)  # Limit concurrent requests to 10


async def fetch_fighter_info_async(
    session: aiohttp.ClientSession, url: str, semaphore: int
):
    """
    주어진 URL에서 파이터 정보를 비동기적으로 크롤링합니다.

    :param session: aiohttp 클라이언트 세션.
    :param url: 크롤링할 URL.
    :return: 크롤링된 파이터 정보 리스트.
    """
    async with semaphore, session.get(url) as response:
        req = await response.text()

    await asyncio.sleep(3)
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # 동시 요청 수를 3개로 제한하는 Semaphore 생성
    semaphore = asyncio.Semaphore(3)

    async with aiohttp.ClientSession(headers=headers) as session:
        coroutines_fighter_info = [
            asyncio.create_task(
                fetch_fighter_info_async(
                    session, url_template.format(chr(alphabet)), semaphore
                )
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
    save_data(match_data=match_data)


def execute_fighter_info_fetching():
    loop = asyncio.get_event_loop()
    fighters_data = loop.run_until_complete(fetch_all_fighters_info_async())
    save_data(fighters_data=fighters_data)
