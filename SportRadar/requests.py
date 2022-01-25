import http.client
import json
import pandas as pd 
import sqlalchemy as db
from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, String, MetaData, Integer

API_KEY = "eqf9xub6dfs9qffxcffnyn4p"
FORMAT = "json"

# retrieve injury report for a given week and year and flatten the JSON to a datatable 
def retrieve(year, week):
    YEAR, WEEK = str(year), str(week)
    if week < 10: 
        WEEK = "0"+WEEK
    conn = http.client.HTTPSConnection("api.sportradar.us")

    conn.request("GET", "/nfl/official/trial/v7/en/seasons/"+YEAR+"/REG/"+WEEK+"/injuries."+FORMAT+"?api_key="+API_KEY)

    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))

    df = pd.json_normalize(data, record_path=["teams"], meta=[["season", "id"], ["season", "year"], ["season", "type"], ["season", "name"], 
                                                            ["week", "id"], ["week", "sequence"], ["week", "title"], "_comment"])
    df = df.explode("players")
    normalized = pd.json_normalize(df.players).add_prefix("players.")
    df = pd.concat([df.reset_index(drop=True), normalized], axis=1)
    df.drop("players", 1, inplace=True)

    df = df.explode("players.injuries")
    normalized = pd.json_normalize(df["players.injuries"]).add_prefix("injuries.")
    df = pd.concat([df.reset_index(drop=True), normalized], axis=1)
    df.drop("players.injuries", 1, inplace=True)
    return df 

db_string = "postgresql://postgres:postgres@localhost:5432/nfl"
engine = db.create_engine(db_string)
connection = engine.connect()
metadata = db.MetaData()
ContractYear = db.Table("contract_years", metadata, autoload=True, autoload_with=engine)

# query the databse to get the cap_number, cash_spent of a player given a tean and year
def match(player, team, year):
    query = db.select([ContractYear.columns.cap_number, ContractYear.columns.cash_spent]) \
            .where(db.and_(ContractYear.columns.player == player, ContractYear.columns.team == team, ContractYear.columns.year == year))
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    if len(ResultSet) > 0: 
        return ResultSet[0]
    return 0, 0

# df = retrieve(2021, 1)
# print(df.head())
# df.to_csv("./week_injuries.csv")

# df = pd.read_csv("./sample.csv", index_col=0)
# print(df.head())
# df[["cap_number", "cash_spent"]] = df.apply(lambda x: match(x["players.name"], x["name"], str(x["season.year"])), axis=1, result_type="expand")
# print(df.head())
# df.to_csv("./sample.csv")

# retrieve roster for a given game and flatten the JSON to a datatable 
def retrieveRoster(game):
    GAME = game
    conn = http.client.HTTPSConnection("api.sportradar.us")

    conn.request("GET", "http://api.sportradar.us/nfl/official/trial/v7/en/games/"+GAME+"/roster.json?api_key="+API_KEY)

    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))

    df = pd.concat([pd.json_normalize(data, record_path=["home", "players"], meta=["id", "summary"], meta_prefix="season->"), pd.json_normalize(data, record_path=["away", "players"], meta=["id", "summary"], meta_prefix="season->")])
    # df = df.explode("players")
    # normalized = pd.json_normalize(df.players).add_prefix("players.")
    # df = pd.concat([df.reset_index(drop=True), normalized], axis=1)
    # df.drop("players", 1, inplace=True)

    # df = df.explode("players.injuries")
    # normalized = pd.json_normalize(df["players.injuries"]).add_prefix("injuries.")
    # df = pd.concat([df.reset_index(drop=True), normalized], axis=1)
    # df.drop("players.injuries", 1, inplace=True)
    return df 

df = retrieveRoster("7d06369a-382a-448a-b295-6da9eab53245")
print(df)
df.to_csv("./csv/game_roster.csv")