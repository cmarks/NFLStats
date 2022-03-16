import glob
import pandas as pd 
inputdir = "/Users/jeffreyigims/Desktop/Team_Scotti/ManGamesLost/csv/*.xlsx"

# for file in glob.glob(inputdir):
#     print("[INFO] processing " + file)
#     df = pd.read_excel(file, "Data Sheet - CONFIDENTIAL")
#     print(df.head())

# file = "/Users/jeffreyigims/Desktop/Team_Scotti/ManGamesLost/csv/2020.xlsx"
# df = pd.read_excel(file, "Data Sheet - CONFIDENTIAL")
# df.to_csv("/Users/jeffreyigims/Desktop/Team_Scotti/ManGamesLost/csv/2020.csv")

# melt the table 
df = pd.read_csv("/Users/jeffreyigims/Desktop/Team_Scotti/ManGamesLost/csv/2020.csv", index_col=0)
value_vars = df.columns[4:]
df = pd.melt(df, id_vars=["Team", "Game", "Date", "Opp"], value_vars=value_vars, var_name="name")
df = df[df["value"].notna()]

# parse to [outcome, score, gameStatus, injured, injuryStatus, injury]
def parseValue(val):
    # player did not play for non-injury reasons 
    if val == "DNP/SUS/PRA":
        return ["", "", "DNP/SUS/PRA", 0, "", ""]
    vals = val.split() 
    ind, *rest = vals 
    if ind == "INJ": 
        parseInj = "".join(rest)[1:].split(":")
        # player is injured but injury part is not specified 
        if len(parseInj) == 1:
            return ["", "", "OUT", 1] + parseInj + [""]
        # player is injured and injury part is specified
        else: 
            return ["", "", "OUT", 1] + parseInj
    # player is not injured and participated in the game 
    else:
        return [ind, rest[0], "ACTIVE", 0, "", ""]

def testParseValue():
    print(parseValue("DNP/SUS/PRA")) 
    print(parseValue("INJ - Questionable: Hand"))
    print(parseValue("INJ - Injured Reserve: "))
    print(parseValue("INJ - Injured Reserve: Ankle"))
    print(parseValue("INJ - Sidelined COVID19"))
    print(parseValue("W 40-23 6"))

# drop all players who became free agents or are now with another team
def shouldDrop(val):
    vals = val.split() 
    ind, *_ = vals 
    if ind == "free" or ind == "with": return 1  
    else: return 0 

# df[["firstName", "lastName"]] = df.apply(lambda x: x[4].split(), axis=1, result_type="expand")
# df[["outcome", "score"]] = df.apply(lambda x: x[5].split()[:-1], axis=1, result_type="expand")
# df["outcome"] = df.value.apply(lambda x: x.split()[:-1])

# get rid of players listed as free agents or with another team
df = df[df.apply(lambda x: shouldDrop(x[5]), axis=1, result_type="expand") == 0]

# parse to [outcome, score, gameStatus, injured, injuryStatus, injury]
df[["outcome", "score", "gameStatus", "injured", "injuryStatus", "injury"]] = df.apply(lambda x: parseValue(x[5]), axis=1, result_type="expand")

print(df.head())
df.to_csv("/Users/jeffreyigims/Desktop/Team_Scotti/ManGamesLost/csv/2020_clean.csv")
