import time, requests, re
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class CrawlingModule:
    def __init__(self) -> None:
        self.base_url = "http://www.ufcstats.com/"

    def get_fighters(self):
        for alphabet in range(97, 123):
            url = f"{self.base_url}statistics/fighters?char={chr(alphabet)}&page=all"
            req = requests.get(url).text
            time.sleep(1)
            html = BeautifulSoup(req, "html.parser")

            for row in html.find_all("tr"):
                try:
                    fighter_id = row.find("a", "b-link b-link_style_black")[
                        "href"
                    ].split("/")[-1]
                except:
                    continue
                fighter_info_td = row.find_all("td")
                if fighter_info_td:
                    fighters_dict = self._crawling_fighter_info(fighter_info_td)
                    print(fighters_dict)
                    # Frighters.objects.update_or_create(**fighters_dict)
                # fighter_detail = self.crawling_fighter_detail(fighter_id)

    def crawling_fighter_detail(self, fighter_id):
        fighter_url = f"{self.base_url}fighter-details/{fighter_id}"
        req = requests.get(fighter_url).text
        html = BeautifulSoup(req, "html.parser")

    def _inch_to_cm(self, data: str, is_reach=False):
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

    def _lbs_to_kg(self, data: str):
        to_int = round((int(re.sub("[^0-9]", "", data)) / 2.205), 1)
        return to_int

    def _crawling_fighter_info(self, fighter_info_td: list):
        model_dict = {}
        fighter_info_list = [fighter.text.strip() for fighter in fighter_info_td]
        if len(fighter_info_list) > 1:
            model_dict["first_name"] = fighter_info_list[0]
            model_dict["last_name"] = fighter_info_list[1]
            model_dict["nickname"] = (
                fighter_info_list[2] if fighter_info_list[2] else None
            )
            model_dict["height"] = (
                0
                if fighter_info_list[3] == "--"
                else self._inch_to_cm(data=fighter_info_list[3])
            )
            model_dict["weight"] = (
                0
                if fighter_info_list[4] == "--"
                else self._lbs_to_kg(data=fighter_info_list[4])
            )
            model_dict["reach"] = (
                0
                if fighter_info_list[5] == "--"
                else self._inch_to_cm(data=fighter_info_list[5], is_reach=True)
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
            # print("--------")

        return model_dict


CrawlingModule().get_fighters()
