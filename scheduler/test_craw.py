import time, requests, re
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from datetime import datetime


class CrawlingModule:
    def __init__(self) -> None:
        self.base_url = "http://www.ufcstats.com/"

    def get_fighters(self):
        """
        # get all fighers basic info & save to Fighter table
        # create Game table
        """
        for alphabet in range(97, 123):
            url = f"{self.base_url}statistics/fighters?char={chr(alphabet)}&page=all"
            req = requests.get(url).text
            time.sleep(1)
            html = BeautifulSoup(req, "html.parser")

            for row in html.find_all("tr"):
                fighters_dict = self._crawling_fighter_info(row)
                # fighter_all_game = self._set_fighter_all_game(
                #     fighters_dict["fighter_id"]
                # )
                # Frighters.objects.update_or_create(**fighters_dict)

    def get_all_games(self):
        """
        # get all game info
        """
        self._set_title()
        self._set_match()
        self._set_match_stat()
        pass

    def _set_title(self):
        url = f"{self.base_url}statistics/events/completed?page=all"
        req = requests.get(url).text
        time.sleep(1)
        html = BeautifulSoup(req, "html.parser")

        for tr in html.find_all("tr", "b-statistics__table-row"):
            if tr.find("a"):
                title = tr.find("a").text.strip()
                url = tr.find("a")["href"]
                if tr.find("span"):
                    game_date = tr.find("span").text.strip()
                    game_date = datetime.strptime(game_date, "%B %d, %Y").date()
                    # print(game_date)
                if tr.find(
                    "td",
                    "b-statistics__table-col b-statistics__table-col_style_big-top-padding",
                ):
                    location = tr.find(
                        "td",
                        "b-statistics__table-col b-statistics__table-col_style_big-top-padding",
                    ).text.strip()
                # Title.objects.get_or_create(url=url,title=title, game_date=game_date,location=location)

    def _set_match(self):
        pass

    def _set_match_stat(self):
        pass

    def _set_fighter_all_game(self, fighter_id):
        fighter_url = f"{self.base_url}fighter-details/{fighter_id}"
        req = requests.get(fighter_url).text
        html = BeautifulSoup(req, "html.parser")

        for line in html.find_all(
            "tr",
            "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click",
        ):
            print("-----")

            match_id = re.sub("[^0-9a-zA-Z]", "", line["onclick"].split("/")[-2:][1])

            # game_result = line.find("td", "b-fight-details__table-col").text.strip()
            # vs_fighter = " ".join(
            #     str(
            #         re.sub(
            #             "[^a-zA-Z]",
            #             "/",
            #             line.find(
            #                 "td", "b-fight-details__table-col l-page_align_left"
            #             ).text.strip(),
            #         )
            #     ).split("/")[-2:]
            # )

            # match_info_list = []
            # for i in line.find_all("td", "b-fight-details__table-col")[3:]:
            #     match_info_list.append(
            #         list(
            #             filter(
            #                 None, list(set(i.text.strip().replace("\n", "").split(" ")))
            #             )
            #         )
            #     )
            #     # match_info_list.append(re.sub("[^0-9a-zA-Z]", "/", i.text.strip()))
            # print(match_info_list)

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

    def _crawling_fighter_info(self, row: list):
        fighter_info_td = row.find_all("td")
        try:
            fighter_id = row.find("a", "b-link b-link_style_black")["href"].split("/")[
                -1
            ]
        except:
            fighter_id = None
        model_dict = {}
        fighter_info_list = [fighter.text.strip() for fighter in fighter_info_td]
        if len(fighter_info_list) > 1:
            model_dict["fighter_id"] = fighter_id
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


CrawlingModule().get_all_games()
