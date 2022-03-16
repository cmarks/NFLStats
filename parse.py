import pandas as pd
import json
import glob
import requests

inputdir = "/Users/jeffreyigims/Desktop/Team_Scotti/*.json"
outputFile = "/Users/jeffreyigims/Desktop/Team_Scotti/advanced_player_medical.csv"

def readAdvancedPlayerMedical():
    injuryData = []
    for file in glob.glob(inputdir):
        print("[INFO] processing " + file)
        with open(file, "r") as f:
            data = json.load(f)
            df = pd.json_normalize(data, record_path=["MedicalHistory"], meta=[
                                   "PlayerID", "Name", "Position"])
            injuryData.append(df)
    df = pd.concat(injuryData, ignore_index=True)
    cols = ["PlayerID", "Name", "Position"] + df.columns[:-3].tolist()
    df = df.reindex(columns=cols)
    df = df.set_index("AdvancedPlayerMedicalID")
    print(df.head())
    print("[INFO] writing resulting dataframe to " + outputFile)
    df.to_csv(outputFile)

readAdvancedPlayerMedical()


endpoint = "https://api.sportsdata.io/v3/nfl/stats/json/Injuries/"
years = ["2021"]
season_types = {"REG": (1, 17), "PRE": (0, 4), "POST": (1, 4)}
params = {"key": "5237cc16a51b4848b2006f631cba47eb"}


def getWeekInjuries(season, week):
    response = requests.get(endpoint+season+"/"+week, params=params)
    data = response.json()
    df = pd.json_normalize(data)
    return df

advanced_endpoint = "https://api.sportsdata.io/v3/nfl/advanced-metrics/json/AdvancedPlayerInfo/"
def getAdvancedInfo(player):
    response = requests.get(endpoint+str(player), params=params)
    data = response.json()
    # df = pd.from_json(data)
    return data

# data = getAdvancedInfo(1)
# print(data)

# weekInjuries = []
# for year in years:
#     for season_type in season_types:
#         start, finish = season_types[season_type]
#         for week in range(start, finish+1):
#             df = getWeekInjuries(year+season_type, str(week))
#             df["SeasonType"] = season_type
#             normal_week = week
#             if season_type == "REG":
#                 normal_week += 5
#             if season_type == "POST":
#                 normal_week += 22
#             df["NoramlizedWeek"] = normal_week
#             weekInjuries.append(df)
# df = pd.concat(weekInjuries, ignore_index=True)
# print(df.head())

# df = df.drop(columns=["Practice", "PracticeDescription"])
# outputFile = "/Users/jeffreyigims/Desktop/Team_Scotti/2021_weekly_injuries.csv"
# df.to_csv(outputFile)
