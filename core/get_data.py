from fighters.models import *
import pandas as pd

"""
    age = models.IntegerField()
    name = models.TextField()
    win = models.TextField()
    lose = models.TextField()
    height = models.TextField()
    division = models.TextField()
    reach = models.TextField()
    ko_wins = models.IntegerField()
    ko_lose = models.IntegerField()
"""


col = [
    "date",
    "fight_url",
    "event_url",
    "result",
    "fighter",
    "opponent",
    "division",
    "stance",
    "dob",
    "method",
    "total_comp_time",
    "round",
    "time",
    "fighter_url",
    "opponent_url",
    "referee",
    "time_format",
    "reach",
    "height",
    "age",
    "knockdowns",
    "sub_attempts",
    "reversals",
    "control",
    "takedowns_landed",
    "takedowns_attempts",
    "sig_strikes_landed",
    "sig_strikes_attempts",
    "total_strikes_landed",
    "total_strikes_attempts",
    "head_strikes_landed",
    "head_strikes_attempts",
    "body_strikes_landed",
    "body_strikes_attempts",
    "leg_strikes_landed",
    "leg_strikes_attempts",
    "distance_strikes_landed",
    "distance_strikes_attempts",
    "clinch_strikes_landed",
    "clinch_strikes_attempts",
    "ground_strikes_landed",
    "ground_strikes_attempts",
]
col_num = [i for i in range(len(col))]
data = pd.read_csv("masterdataframe.csv", usecols=col_num)
data["result"] = data["result"].replace({1: "승", 0: "패"})

fighter_info = data.drop_duplicates("fighter")[["fighter", "age", "height", "reach"]]
# inch -> sm
fighter_info["height"] = round(fighter_info["height"] * 2.54, 1)
fighter_info["reach"] = round(fighter_info["reach"] * 2.54, 1)
# print(fighter_info.sample(5))


def makes_win_lose_info(data):
    win_lose_info = data.groupby(["fighter", "result"])["result"].count().to_dict()
    fighter_info = data.drop_duplicates("fighter")[
        ["fighter", "age", "height", "reach"]
    ]
    # inch -> sm
    fighter_info["height"] = round(fighter_info["height"] * 2.54, 1)
    fighter_info["reach"] = round(fighter_info["reach"] * 2.54, 1)
    # fighter_info = data["fighter"].drop_duplicates().to_frame()
    fighter_names = (
        data["fighter"].drop_duplicates().to_frame().values.flatten().tolist()
    )
    win_temp = pd.DataFrame(index=range(len(fighter_names)), columns=["fighter", "win"])
    lose_temp = pd.DataFrame(
        index=range(len(fighter_names)), columns=["fighter", "lose"]
    )
    for i, name in enumerate(fighter_names):
        win_tu = (f"{name}", "승")
        lose_tu = (f"{name}", "패")
        if win_tu in win_lose_info.keys():
            # print(i, name, win_lose_info[win_tu])
            win_temp.loc[i] = [name, win_lose_info[win_tu]]

        else:
            win_temp.loc[i] = [name, 0]

    for i, name in enumerate(fighter_names):
        lose_tu = (f"{name}", "패")
        if lose_tu in win_lose_info.keys():
            lose_temp.loc[i] = [name, win_lose_info[lose_tu]]

        else:
            lose_temp.loc[i] = [name, 0]

    win_lose_data = pd.merge(win_temp, lose_temp, how="left", on="fighter")
    fighter_data = pd.merge(fighter_info, win_lose_data, how="left", on="fighter")
    return fighter_data


print(makes_win_lose_info(data))
