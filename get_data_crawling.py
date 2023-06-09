import time, requests, re, time
from bs4 import BeautifulSoup
from datetime import datetime

""" async code
async def craw_game():
    url = "http://www.ufcstats.com/statistics/events/completed?page=all"
    req = requests.get(url).text
    time.sleep(1)
    html = BeautifulSoup(req, "html.parser")
    tasks = []
    for tr in html.find_all("tr", "b-statistics__table-row"):
        model_dict = {}
        if tr.find("a"):
            title = tr.find("a").text.strip()
            model_dict["title"] = title
            url = tr.find("a")["href"]
            task = asyncio.create_task(craw_match(url))
            tasks.append(task)
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
        print("--------")
        print(model_dict)
        print("--------")
    
    await asyncio.gather(*tasks)


async def craw_match(url: str = None) -> dict:
    req = requests.get(url).text
    time.sleep(1)
    html = BeautifulSoup(req, "html.parser")
    # Process the match data and save to database
    # ...

def execute_async_craw_game():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(craw_game())

dag = DAG(
    dag_id='async_crawling_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='0 0 * * *'  # Runs once a day at midnight
)

execute_async_craw_game_task = PythonOperator(
    task_id='execute_async_craw_game_task',
    python_callable=execute_async_craw_game,
    dag=dag
)

"""


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


def craw_fighter_info():
    # for alphabet in range(97, 123):
    #     url = f"http://www.ufcstats.com/statistics/fighters?char={chr(alphabet)}&page=all"
    url = f"http://www.ufcstats.com/statistics/fighters?char=a&page=all"
    req = requests.get(url).text
    time.sleep(1)
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


def craw_game():
    st = time.time()
    print("st :", st)
    url = f"http://www.ufcstats.com/statistics/events/completed?page=all"
    req = requests.get(url).text
    time.sleep(1)
    html = BeautifulSoup(req, "html.parser")
    i = 0

    for td in html.find_all("tr", "b-statistics__table-row"):
        print(f"{i}번째")
        i += 1
        # save to db
        model_dict = {}
        if td.find("a"):
            title = td.find("a").text.strip()
            model_dict["title"] = title
            url = td.find("a")["href"]
            craw_match(url)
            if td.find("span"):
                game_date = td.find("span").text.strip()
                game_date = datetime.strptime(game_date, "%B %d, %Y").date()
                model_dict["game_date"] = game_date
            if td.find(
                "td",
                "b-statistics__table-col b-statistics__table-col_style_big-top-padding",
            ):
                location = td.find(
                    "td",
                    "b-statistics__table-col b-statistics__table-col_style_big-top-padding",
                ).text.strip()
                model_dict["location"] = location

    ed = time.time()
    print("total time : ", ed - st)


def craw_match(url: str = None) -> dict:
    # url = "http://www.ufcstats.com/event-details/aec273fcb765330d"
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
