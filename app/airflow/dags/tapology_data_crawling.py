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

semaphore = asyncio.Semaphore(5)

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.headless = True  # 브라우저 창이 띄우지 않게 설정
chrome_options.add_experimental_option("detach", False)
# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 드라이버 최신 버전 설정
service = Service(executable_path=ChromeDriverManager().install())

browser = webdriver.Chrome(service=service, options=chrome_options)

# 페이지 로딩이 완료될 때까지 대기하는 코드
browser.implicitly_wait(5)

base_url = "https://www.tapology.com"

url_list = [
    # "https://www.tapology.com/search/mma-fighters-by-weight-class/Atomweight-105-pounds",
    # "https://www.tapology.com/search/mma-fighters-by-weight-class/Strawweight-115-pounds",
    # "https://www.tapology.com/search/mma-fighters-by-weight-class/Flyweight-125-pounds",
    # "https://www.tapology.com/search/mma-fighters-by-weight-class/Bantamweight-135-pounds",
    "https://www.tapology.com/search/mma-fighters-by-weight-class/Featherweight-145-pounds",
    # "https://www.tapology.com/search/mma-fighters-by-weight-class/Lightweight-155-pounds",
    # "https://www.tapology.com/search/mma-fighters-by-weight-class/Welterweight-170-pounds",
    # "https://www.tapology.com/search/mma-fighters-by-weight-class/Middleweight-185-pounds",
    # "https://www.tapology.com/search/mma-fighters-by-weight-class/Light_Heavyweight-205-pounds",
    # "https://www.tapology.com/search/mma-fighters-by-weight-class/Heavyweight-265-pounds",
    # "https://www.tapology.com/search/mma-fighters-by-weight-class/Super_Heavyweight-over-265-pounds",
]

# for url in url_list:
#     res = requests.get(url).text
#     html = BeautifulSoup(res, "html.parser")
#     res = html.find_all("table", "siteSearchResults")
#     coroutines = [
#         a.get("href") for table in res for a in table.find_all("a") if a.get("href")
#     ]

# for i in coroutines:
#     print(i)
#     browser.get(i)
#     print("done")


async def crawling_fighter_by_weight(session):
    for url in url_list:
        results = []
        async with session.get(url, ssl=False) as res:
            res = await res.text()
            html = BeautifulSoup(res, "html.parser")
            print(111, url)
            # tbody 태그를 찾습니다.
            tbody = html.find("table")
            if tbody:
                # tbody 안의 모든 a 태그를 찾아 href 속성을 가져옵니다.
                fighter_urls = [
                    a.get("href") for a in tbody.find_all("a") if a.get("href")
                ]
            else:
                # tbody 태그가 없는 경우, 빈 리스트를 처리합니다.
                fighter_urls = []

        batch_size = 10
        for i in range(0, len(fighter_urls), batch_size):
            print(333, len(results))
            batch = fighter_urls[i : i + batch_size]
            tasks = [asyncio.create_task(crawling_fighter_detail(url)) for url in batch]
            results += await asyncio.gather(*tasks)

    return


def get_element(data: List, index: int, default_val=None):
    """
    list에 index가 존재하면 해당 value 없다면 default value return
    """
    try:
        return data[index]
    except IndexError:
        return default_val


async def crawling_fighter_detail(url):
    async with semaphore:
        model_dict = {}
        fighter_url = base_url + url
        print(999, fighter_url)
        browser.get(fighter_url)
        html_content = browser.page_source  # 모든 컨텐츠가 로드된 페이지의 HTML 소스 코드 가져오기

        html = BeautifulSoup(html_content, "html.parser")
        details_two_columns_div = html.find("div", id="stats")  # id를 사용하여 요소 찾기
        span_tags = details_two_columns_div.find_all("span")

        span_texts = [
            tag.text.replace("\n", "") if "N/A" not in tag.text else None
            for tag in span_tags
        ]
        if span_texts:
            name = get_element(span_texts, 0).replace(" ", "_")
            pro_mma_record = (
                get_element(span_texts, 1).split(" ")[0]
                if get_element(span_texts, 1)
                else None
            )
            nickname = (
                get_element(span_texts, 2).replace(" ", "_")
                if get_element(span_texts, 2)
                else None
            )
            current_streak = get_element(span_texts, 3)
            age = get_element(span_texts, 4)
            birth = get_element(span_texts, 5)
            last_fight = f"{get_element(span_texts, 6)} + {get_element(span_texts, 7)} + {get_element(span_texts, 8)}"
            weight_class = get_element(span_texts, 9)
            last_weigh_in = get_element(span_texts, 10)
            affiliation = get_element(span_texts, 11)
            height = get_element(span_texts, 12)
            reach = get_element(span_texts, 13)
            career_earnings = get_element(span_texts, 14)
            born = get_element(span_texts, 15)
            head_coach = get_element(span_texts, 17)
            other_coanees = get_element(span_texts, 18)

            model_dict["name"] = name
            model_dict["pro_mma_record"] = pro_mma_record
            model_dict["nickname"] = nickname
            model_dict["current_streak"] = current_streak
            model_dict["age"] = age
            model_dict["birth"] = birth
            model_dict["last_fight"] = last_fight
            model_dict["weight_class"] = weight_class
            model_dict["last_weigh_in"] = last_weigh_in
            model_dict["affiliation"] = affiliation
            model_dict["height"] = height
            model_dict["reach"] = reach
            model_dict["career_earnings"] = career_earnings
            model_dict["born"] = born
            model_dict["head_coach"] = head_coach
            model_dict["other_coanees"] = other_coanees
    return model_dict


async def main():
    async with aiohttp.ClientSession() as session:
        data = await crawling_fighter_by_weight(session)
    browser.quit()


if __name__ == "__main__":
    asyncio.run(main())
