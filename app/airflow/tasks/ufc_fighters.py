import asyncio, aiohttp, time, traceback
from bs4 import BeautifulSoup
from datetime import datetime

from .utils import inch_to_cm, lbs_to_kg, save_data, get_element_safe
from dags.log import logger


async def fetch_fighter_birh(
    session: aiohttp.ClientSession, semaphore: int, fighter_id: str
):
    url = f"http://www.ufcstats.com/fighter-details/{fighter_id}"
    async with semaphore, session.get(url) as response:
        req = await response.text()
        html = BeautifulSoup(req, "html.parser")
        dob_item = html.find(lambda tag: tag.name == "li" and "DOB" in tag.text)
        if dob_item:
            dob_date = (
                dob_item.get_text(strip=True).split(":")[1].strip()
            )  # ':' 기준으로 분할하여 날짜 부분만 추출
        else:
            dob_date = None

    return dob_date


async def fetch_fighters(session: aiohttp.ClientSession, url: str, semaphore: int):
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
        except Exception as e:
            continue

        if "web_fighter_id" in model_dict:
            dob_date = await fetch_fighter_birh(
                session=session, fighter_id=web_fighter_id, semaphore=semaphore
            )
            model_dict["birth"] = dob_date

        fighter_info_td = row.find_all("td")
        fighter_info_list = [fighter.text.strip() for fighter in fighter_info_td]

        name_parts = [
            get_element_safe(fighter_info_list, 0),
            get_element_safe(fighter_info_list, 1),
        ]
        # None이 아닌 요소만 필터링 후, 공백 문자(" ")로 결합
        model_dict["name"] = " ".join(filter(None, name_parts))
        model_dict["nickname"] = get_element_safe(fighter_info_list, 2)
        model_dict["height"] = (
            0
            if get_element_safe(fighter_info_list, 3) == "--"
            else inch_to_cm(get_element_safe(fighter_info_list, 3))
        )
        model_dict["weight"] = (
            0
            if get_element_safe(fighter_info_list, 4) == "--"
            else lbs_to_kg(get_element_safe(fighter_info_list, 4))
        )
        model_dict["reach"] = (
            0
            if get_element_safe(fighter_info_list, 5) == "--"
            else inch_to_cm(get_element_safe(fighter_info_list, 5), is_reach=True)
        )
        model_dict["stance"] = get_element_safe(fighter_info_list, 6)
        model_dict["win"] = (
            0
            if get_element_safe(fighter_info_list, 7) == "--"
            else int(get_element_safe(fighter_info_list, 7))
        )
        model_dict["lose"] = (
            0
            if get_element_safe(fighter_info_list, 8) == "--"
            else int(get_element_safe(fighter_info_list, 8))
        )
        model_dict["draw"] = (
            0
            if get_element_safe(fighter_info_list, 9) == "--"
            else int(get_element_safe(fighter_info_list, 9))
        )

        fighter_list.append(model_dict)

    return fighter_list


async def fetch_all_fighters_info():
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
                fetch_fighters(session, url_template.format(chr(alphabet)), semaphore)
            )
            for alphabet in range(ord("a"), ord("z") + 1)
        ]

        res = await asyncio.gather(*coroutines_fighter_info)
    return res


def execute_fighter_info_fetching():
    """
    UFC fighter 데이터 추출 및 저장
    """
    start_time = time.time()
    fighters_data = asyncio.run(fetch_all_fighters_info())
    save_data(collection_name="fighters", data=fighters_data)
    end_time = time.time()
    diff = end_time - start_time
    logger.warning(f"UFC fighter crawling time : {diff}")
    return
