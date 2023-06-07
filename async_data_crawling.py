import time, requests, re, asyncio
from bs4 import BeautifulSoup
from datetime import datetime


async def test():
    url = "http://www.ufcstats.com/statistics/events/completed?page=all"
    req = requests.get(url).text
    time.sleep(1)
    html = BeautifulSoup(req, "html.parser")
    coroutines = [
        asyncio.create_task(craw_match(url=i["href"]))
        for i in html.find_all("a", "b-link b-link_style_black")
    ]
    # await asyncio.gather(*coroutines)


async def craw_game(page: int):
    print(f"페이지 : {page}")
    url = "http://www.ufcstats.com/statistics/events/completed?page=all"
    req = requests.get(url).text
    time.sleep(1)
    html = BeautifulSoup(req, "html.parser")
    # tasks = []
    for tr in html.find_all("tr", "b-statistics__table-row"):
        model_dict = {}
        if tr.find("a"):
            title = tr.find("a").text.strip()
            model_dict["title"] = title
            url = tr.find("a")["href"]
            # task = asyncio.create_task(craw_match(url))
            # tasks.append(task)
            if tr.find("span"):
                game_date = tr.find("span").text.strip()
                game_date = datetime.strptime(game_date, "%B %d, %Y").date()
                model_dict["game_date"] = game_date
            if tr.find(
                "td",
                "b-statistics__table-col b-statistics__table-col_style_big-top-padding",
            ):
                location = tr.find(
                    "td",
                    "b-statistics__table-col b-statistics__table-col_style_big-top-padding",
                ).text.strip()
                model_dict["location"] = location
    # await task

    # await asyncio.gather(*tasks)


async def craw_match(url: str = None) -> dict:
    print(f"url: {url}")
    req = requests.get(url).text
    time.sleep(1)
    html = BeautifulSoup(req, "html.parser")
    match_info = [
        i.get_text(strip=True).split(":")[1]
        for i in html.find_all("li", class_="b-list__box-list-item")
    ]
    main_event = html.find("span", "b-content__title-highlight").text.strip()
    match_date = datetime.strptime(match_info[0], "%B %d, %Y").date()
    match_loc = match_info[1]

    for td in html.find_all(
        "tr",
        "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click",
    ):
        # save to db
        model_dict = {
            "main_event": main_event,
            "match_date": match_date,
            "match_loc": match_loc,
        }
        infos = [
            i.text.strip() for i in td.find_all("p", "b-fight-details__table-text")
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


def execute_async_crawl_game():
    st = time.time()
    loop = asyncio.get_event_loop()
    coroutines = [craw_game(page) for page in range(1, 26)]
    loop.run_until_complete(asyncio.wait(coroutines))
    ed = time.time()
    print("Total time:", ed - st)


# async def execute_async_crawl_game():
#     st = time.time()
#     coroutines = [craw_game(page) for page in range(1, 26)]
#     await asyncio.gather(*coroutines)
#     ed = time.time()
#     print("Total time:", ed - st)


def execute_async_craw_game():
    st = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    ed = time.time()
    print("Total time:", ed - st)


# dag = DAG(
#     dag_id='async_crawling_dag',
#     start_date=datetime(2023, 1, 1),
#     schedule_interval='0 0 * * *'  # Runs once a day at midnight
# )

# execute_async_craw_game_task = PythonOperator(
#     task_id='execute_async_craw_game_task',
#     python_callable=execute_async_craw_game,
#     dag=dag
# )
