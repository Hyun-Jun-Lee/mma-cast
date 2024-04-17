import asyncio, aiohttp, time
from bs4 import BeautifulSoup
from datetime import datetime

from .utils import save_data, get_element_safe
from dags.log import logger


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
        for url in fight_links:
            # url = "http://www.ufcstats.com/fight-details/894c44c3d04aaf6f"
            async with session.get(url) as response:
                res = await response.text()
                html = BeautifulSoup(res, "html.parser")

                main_event_title = html.find("h2").get_text(strip=True)

                all_tables = html.find_all("table")
                try:
                    for tr in all_tables[0].find_all("tbody"):
                        cell_texts = [td.text.strip() for td in tr.find_all("td")]
                        fighters = cell_texts[0].split("\n\n\n")
                except:
                    print(111, main_event_title)

            # headers = []
            # for th in html.find_all("th"):
            #     headers.append(th.text.strip())
            # print(headers)

            # for tr in html.find_all("tr"):
            #     tds = tr.find_all("td")
            #     if not tds:
            #         continue
            #     row_data = []
            #     for td in tds:
            #         row_data.append(td.get_text(strip=True))
            #     print(row_data)


async def main():
    semaphore = asyncio.Semaphore(3)

    async with semaphore:
        async with aiohttp.ClientSession() as session:
            fight_links = await fetch_all_fight(session, semaphore)
            with open("fight_links.txt", "w") as file:
                for link in fight_links:
                    file.write(link + "\n")
            # data = await fetch_fight_stat(session, semaphore, fight_links)
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
