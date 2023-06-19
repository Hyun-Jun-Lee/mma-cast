import time, requests, re, asyncio, aiohttp
from bs4 import BeautifulSoup
from datetime import datetime

semaphore = asyncio.Semaphore(10)  # Limit concurrent requests to 10


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


# def run_craw_game():
#     asyncio.run(craw_game())


# async def execute_async_craw_game():
#     st = time.time()
#     await craw_game()
#     ed = time.time()
#     print("총 시간:", ed - st)


def run_craw_game():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(craw_game())


if __name__ == "__main__":
    st = time.time()
    run_craw_game()
    ed = time.time()
    print("총 시간:", ed - st)
