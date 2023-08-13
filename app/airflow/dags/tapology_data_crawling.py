import time, requests, re, asyncio, aiohttp
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from log import logger

base_url = "https://www.tapology.com"
search_url = base_url + "/search"
req = requests.get(search_url).text
time.sleep(1)
html = BeautifulSoup(req, "html.parser")

req = html.find("div", "siteSearchFightersByWeightClass")
req = req.find_all("dd")
for r in req:
    weghit_class = r.text.strip()
    href = r.find("a")["href"]
    print(1212, weghit_class, href)


async def weight_classes():
    base_url = "https://www.tapology.com"
    search_url = base_url + "/search"
    req = requests.get(search_url).text
    time.sleep(1)
    html = BeautifulSoup(req, "html.parser")

    req = html.find("div", "siteSearchFightersByWeightClass")
    req = req.find_all("dd")
    for r in req:
        weghit_class = r.text.strip()
        print(1212, weghit_class)
