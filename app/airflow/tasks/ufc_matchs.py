import asyncio, aiohttp, time
from bs4 import BeautifulSoup
from datetime import datetime

from .utils import save_data, get_element_safe
from dags.log import logger


async def fetch_event(session: aiohttp.ClientSession, url: str, semaphore: int) -> dict:
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
                model_dict["winner"] = get_element_safe(infos, 1)
                model_dict["winner_strike"] = get_element_safe(infos, 5)
                model_dict["winner_td"] = get_element_safe(infos, 7)
                model_dict["winner_sub"] = get_element_safe(infos, 9)
                model_dict["looser"] = get_element_safe(infos, 2)
                model_dict["looser_strike"] = get_element_safe(infos, 6)
                model_dict["looser_td"] = get_element_safe(infos, 8)
                model_dict["looser_sub"] = get_element_safe(infos, 10)
                model_dict["weight_class"] = get_element_safe(infos, 11)
                model_dict["finish_method"] = get_element_safe(infos, 12)
                model_dict["finish_tech"] = get_element_safe(infos, 13)
                model_dict["finish_round"] = get_element_safe(infos, 14)
                model_dict["finish_time"] = get_element_safe(infos, 15)
                match_list.append(model_dict)
    return match_list


async def fetch_all_matches_info():
    """
    UFC 통계 사이트에서 완료된 모든 이벤트의 매치 정보를 비동기적으로 크롤링합니다.

    :return: 크롤링된 모든 이벤트의 매치 정보 리스트.
    """

    url = "http://www.ufcstats.com/statistics/events/completed?page=all"
    all_fight_links = set()

    semaphore = asyncio.Semaphore(3)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            res = await response.text()
            html = BeautifulSoup(res, "html.parser")

            event_urls = [
                i["href"] for i in html.find_all("a", "b-link b-link_style_black")
            ]

            match_info_tasks = [
                asyncio.create_task(fetch_event(session, event_url, semaphore))
                for event_url in event_urls
            ]

            res = await asyncio.gather(*match_info_tasks)
    return res


def execute_match_info_fetching():
    """
    UFC game 데이터 추출 및 저장
    """
    start_time = time.time()
    match_data = asyncio.run(fetch_all_matches_info())
    save_data(collection_name="match", data=match_data)
    end_time = time.time()
    diff = end_time - start_time
    logger.warning(f"UFC match crawling time : {diff}")
    return
