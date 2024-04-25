import asyncio, aiohttp, time
from bs4 import BeautifulSoup
from datetime import datetime

from .utils import save_data, get_element_safe
from dags.log import logger


async def extract_stats(cell_texts):
    fighters_names = cell_texts[0].split("\n\n\n")
    sig_strike_stats = cell_texts[2].split()
    takedown_stats = cell_texts[5].split()
    sub_attack_stats = cell_texts[7].split()
    control_time_stats = cell_texts[9].split()

    red_fighter = {
        "name": fighters_names[0],
        "total_strike": sig_strike_stats[2],
        "hit_strike": sig_strike_stats[0],
        "total_takedown": takedown_stats[2],
        "takedown": takedown_stats[0],
        "sub_attacks": sub_attack_stats[0],
        "control_time": control_time_stats[0],
    }
    blue_fighter = {
        "name": fighters_names[1],
        "total_strike": sig_strike_stats[5],
        "hit_strike": sig_strike_stats[3],
        "total_takedown": takedown_stats[5],
        "takedown": takedown_stats[3],
        "sub_attacks": sub_attack_stats[1],
        "control_time": control_time_stats[1],
    }

    return red_fighter, blue_fighter


async def extract_each_round_stat(tbody):
    total_round_stat = []
    round_info = 0

    for tr in tbody.find_all("tr"):
        each_round_stat = {}
        round_info += 1
        each_round_stat["round"] = round_info
        cell_texts = [td.text.strip() for td in tr.find_all("td")]

        red_fighter, blue_fighter = await extract_stats(cell_texts)

        each_round_stat["red_fighter"] = red_fighter
        each_round_stat["blue_fighter"] = blue_fighter
        total_round_stat.append(each_round_stat)

    return total_round_stat


async def extrat_total_fight_stat(tbody):
    total_stat = []
    for tr in tbody.find_all("tr"):
        cell_texts = [td.text.strip() for td in tr.find_all("td")]

        red_fighter, blue_fighter = await extract_stats(cell_texts)

    total_stat.append(red_fighter)
    total_stat.append(blue_fighter)
    return total_stat


async def fetch_fight_links(session, url, semaphore, all_fight_links):
    async with semaphore:
        async with session.get(url) as response:
            res = await response.text()
            html = BeautifulSoup(res, "html.parser")

            fight_links = {
                link["href"]
                for link in html.find_all("a", href=True)
                if "fight-details" in link["href"]
            }

            all_fight_links.update(fight_links)


async def fetch_all_fight(session, semaphore):
    """
    UFC 통계 사이트에서 완료된 모든 이벤트의 매치 정보를 비동기적으로 크롤링합니다.

    :return: 크롤링된 모든 이벤트의 매치 정보 리스트.
    """

    url = "http://www.ufcstats.com/statistics/events/completed?page=all"
    all_fight_links = set()

    async with semaphore:
        async with session.get(url) as response:
            res = await response.text()
            html = BeautifulSoup(res, "html.parser")

            event_urls = [
                i["href"] for i in html.find_all("a", "b-link b-link_style_black")
            ]

            match_info_tasks = [
                asyncio.create_task(
                    fetch_fight_links(session, event_url, semaphore, all_fight_links)
                )
                for event_url in event_urls
            ]

            res = await asyncio.gather(*match_info_tasks)
    return all_fight_links


async def fetch_fight_stat(session, semaphore, fight_links):
    async with semaphore:
        # for url in fight_links:
        url = "http://www.ufcstats.com/fight-details/01f7c28804746979"
        fighte_info = {}
        async with session.get(url) as response:
            res = await response.text()
            html = BeautifulSoup(res, "html.parser")

            main_event_title = html.find("h2").get_text(strip=True)
            fighte_info["main_event"] = main_event_title

            all_tables = html.find_all("table")
            total_tables = all_tables[0].find("tbody")
            total_round_tables = all_tables[1].find("tbody")
            total_detail_strike_tables = all_tables[2].find("tbody")
            total_detail_strike_round_tables = all_tables[3].find("tbody")

            total_stats = await extrat_total_fight_stat(total_tables)
            each_round_stat = await extract_each_round_stat(total_round_tables)
            total_round_detail = await extract_total_round_detail(
                total_detail_strike_tables
            )
            each_round_detail = await extract_each_round_detail(
                total_detail_strike_round_tables
            )

            fighte_info["total"] = total_stats
            fighte_info["rounds"] = each_round_stat

        # print(fighte_info)


async def main():
    semaphore = asyncio.Semaphore(3)

    async with semaphore:
        async with aiohttp.ClientSession() as session:
            # fight_links = await fetch_all_fight(session, semaphore)
            with open("fight_links.txt", "r") as file:
                fight_links = {line.strip() for line in file}

            data = await fetch_fight_stat(session, semaphore, fight_links)
            # 데이터 처리 로직
            # save_data(collection_name="fight-detail", data=data)


def execute_fight_detail_fetching():
    """
    UFC game 데이터 추출 및 저장
    """
    start_time = time.time()
    fight_links = asyncio.run(main())
    end_time = time.time()
    diff = end_time - start_time
    logger.warning(f"UFC match crawling time : {diff}")
    return
