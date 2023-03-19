import time, requests, re
from bs4 import BeautifulSoup

# a-z
# for alphabet in range(97, 123):
#     url = f"http://www.ufcstats.com/statistics/fighters?char={chr(alphabet)}&page=all"


def feet_to_cm(data):
    # str_feet = re.sub("[^0-9]", "", data)
    H_feet = data.split(" ")[0]
    H_inch = data.split(" ")[-1]
    H_feet_e = int(re.sub("[^0-9]", "", H_feet))
    H_inch_e = int(re.sub("[^0-9]", "", H_inch))
    print(H_feet_e, H_inch_e)

    # H_feet_e = int(re.sub("[^0-9]", "", H_feet)) * 12
    # H_inch_e = int(re.sub("[^0-9]", "", H_inch))
    # to_cm = (H_feet_e + H_inch_e) * 2.54
    # return to_cm


url = f"http://www.ufcstats.com/statistics/fighters?char=a&page=all"
req = requests.get(url).text
time.sleep(1)
html = BeautifulSoup(req, "html.parser")
k = 0
for i in html.find_all("tr")[2:]:
    print("--------")
    fighter_info_td = i.find_all("td")
    fighter_info_list = [fighter.text.strip() for fighter in fighter_info_td]

    fighter_id = i.find("a", "b-link b-link_style_black")["href"].split("/")[-1]
    name = fighter_info_list[0] + fighter_info_list[1]
    nickname = fighter_info_list[2]
    if fighter_info_list[3] == "--":
        print(fighter_info_list[3])
    # height = feet_to_cm(fighter_info_list[3])
    # print(height)
    # print(fighter_info_list)
    print("--------")
# for i in html.find_all("tbody"):

# for i in html.find_all("a", "b-link b-link_style_black"):
#     fighter_id = i["href"].split("/")[-1]


# body > section > div > div > div > table > tbody
