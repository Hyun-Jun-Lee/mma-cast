import time, requests, re
from bs4 import BeautifulSoup

# a-z
# for alphabet in range(97, 123):
#     url = f"http://www.ufcstats.com/statistics/fighters?char={chr(alphabet)}&page=all"


def feet_to_cm(data):
    """
    concert inch(ex.6'7") to cm
    """
    H_feet = data.split(" ")[0]
    H_inch = data.split(" ")[-1]

    H_feet_e = int(re.sub("[^0-9]", "", H_feet)) * 12
    H_inch_e = int(re.sub("[^0-9]", "", H_inch))
    to_cm = round(((H_feet_e + H_inch_e) * 2.54), 1)
    return to_cm


def lbs_to_kg(data):
    to_int = round((int(re.sub("[^0-9]", "", data)) / 2.205), 1)
    return to_int


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
    nickname = fighter_info_list[2] if fighter_info_list[2] else None
    height = 0 if fighter_info_list[3] == "--" else feet_to_cm(fighter_info_list[3])
    weight = 0 if fighter_info_list[4] == "--" else lbs_to_kg(fighter_info_list[4])
    print(weight)
    print("--------")

# ['Hunter', 'Azure', '', '5\' 8"', '145 lbs.', '69.0"', 'Orthodox', '9', '2', '0', '']
