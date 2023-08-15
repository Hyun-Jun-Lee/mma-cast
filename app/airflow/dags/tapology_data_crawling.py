import time, requests, re, asyncio, aiohttp
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from log import logger

# 크롬 드라이버 기본 모듈
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 크롬 드라이버 자동 업데이트을 위한 모듈
from webdriver_manager.chrome import ChromeDriverManager

semaphore = asyncio.Semaphore(10)

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.headless = True  # 브라우저 창이 띄우지 않게 설정
chrome_options.add_experimental_option("detach", False)
# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 드라이버 최신 버전 설정
service = Service(executable_path=ChromeDriverManager().install())

browser = webdriver.Chrome(service=service, options=chrome_options)


url_list = [
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Atomweight-105-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Strawweight-115-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Flyweight-125-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Bantamweight-135-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Featherweight-145-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Lightweight-155-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Welterweight-170-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Middleweight-185-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Light_Heavyweight-205-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Heavyweight-265-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Super_Heavyweight-over-265-pounds",
]


url = "https://www.tapology.com/fightcenter/fighters/chan-sung-jung-the-korean-zombie"

browser.get(url)

html_content = browser.page_source  # 모든 컨텐츠가 로드된 페이지의 HTML 소스 코드 가져오기

browser.quit()  # 웹 드라이버 종료

html = BeautifulSoup(html_content, "html.parser")
details_two_columns_div = html.find("div", id="stats")  # id를 사용하여 요소 찾기

span_tags = details_two_columns_div.find_all("span")

span_texts = [tag.text for tag in span_tags]

print(span_texts)


async def weight_classes():
    for url in url_list:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, ssl=False) as res:
                    res = await res.text()
                    html = BeautifulSoup(res, "html.parser")
                    res = html.find_all("table", "siteSearchResults")
                    coroutines = [
                        fighters(url=a.get("href"))
                        for table in res
                        for a in table.find_all("a")
                    ]

                    res = await asyncio.gather(*coroutines)
    return res


sample = [
    "정찬성, Jung Chan Sung",
    "17-7-0 (Win-Loss-Draw)",
    "\nThe Korean Zombie\n",
    "1 Loss",
    "36",
    "1987.03.17",
    "April 09, 2022",
    "in",
    "UFC",
    "Featherweight",
    "\n144.5 lbs\n",
    "Fight Ready MMA",
    "5'7\" (171cm)",
    '72.0" (183cm)',
    "$524,000 USD",
    "\nPohang, South Korea\n",
    "\nPohang, South Korea\n",
    "\nEddie Cha\n",
    "\nN/A\n",
]


async def fighters_detail(url):
    model_dict = {}
    browser.get(url)
    html_content = browser.page_source  # 모든 컨텐츠가 로드된 페이지의 HTML 소스 코드 가져오기
    browser.quit()  # 웹 드라이버 종료

    html = BeautifulSoup(html_content, "html.parser")
    details_two_columns_div = html.find("div", id="stats")  # id를 사용하여 요소 찾기

    span_texts = [tag.text if "N/A" not in tag.text else None for tag in span_tags]

    span_texts = [tag.text for tag in span_tags]
    if span_texts:
        name = (
            span_texts[0].split(",")[1].replace(" ", "_")
            if "," in span_texts[0]
            else span_texts[0].replace(" ", "_")
        )
        model_dict["name"] = span_texts[0]
        model_dict["pro_mma_record"] = span_texts[1]
        model_dict["nickname"] = span_texts[2] if span_texts[2] else None
        model_dict["current_streak"] = (
            0 if span_texts[3] == "--" else inch_to_cm(span_texts[3])
        )
        model_dict["age"] = 0 if span_texts[4] == "--" else lbs_to_kg(span_texts[4])
        model_dict["birth"] = None
        model_dict["last_fight"] = 0 if span_texts[6] == "--" else span_texts[6]
        model_dict["weight_class"] = 0 if span_texts[7] == "--" else span_texts[7]
        model_dict["last_weigh_in"] = 0 if span_texts[8] == "--" else span_texts[8]
        model_dict["affiliation"] = 0 if span_texts[9] == "--" else span_texts[9]
        model_dict["height"] = 0 if span_texts[9] == "--" else span_texts[9]
        model_dict["reach"] = 0 if span_texts[9] == "--" else span_texts[9]
        model_dict["career_earnings"] = 0 if span_texts[9] == "--" else span_texts[9]
        model_dict["born"] = 0 if span_texts[9] == "--" else span_texts[9]
        model_dict["fighting_outof"] = 0 if span_texts[9] == "--" else span_texts[9]
        model_dict["head_coach"] = 0 if span_texts[9] == "--" else span_texts[9]
        model_dict["other_coanees"] = 0 if span_texts[9] == "--" else span_texts[9]
