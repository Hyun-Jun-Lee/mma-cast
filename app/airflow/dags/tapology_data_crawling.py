import time, requests, re, asyncio, aiohttp
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from log import logger

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

semaphore = asyncio.Semaphore(10)


url = "https://www.tapology.com/search/mma-fighters-by-weight-class/Super_Heavyweight-over-265-pounds"
response = requests.get(url)
html_content = response.text

html = BeautifulSoup(html_content, "html.parser")
res = html.find_all("table", "siteSearchResults")


async def weight_classes():
    for url in url_list:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as res:
                    res = await res.text()
                    html = BeautifulSoup(res, "html.parser")
                    coroutines = [
                        fighters(url=a.get("href"))
                        for table in res
                        for a in table.find_all("a")
                    ]

                    res = await asyncio.gather(*coroutines)
    return res


def fighters(url):
    pass
