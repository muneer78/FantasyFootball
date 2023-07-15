import pandas as pd


# Define the function to convert column headers to proper case
def convert_column_headers_to_proper_case(df):
    df.columns = [column.title() for column in df.columns]


dfpff = pd.read_csv("PFFOLine.csv", usecols=["Team", "PFFRank"])
dfcbsoline = pd.read_csv("CBSOLine.csv", usecols=["Team", "CBSOLineRank"])
dfpfn = pd.read_csv("PFNOLine.csv", usecols=["Team", "Rank"])
dfcbs = pd.read_csv("CBSSportsSOS.csv", usecols=["Team", "CBSRank"])
dffbs = pd.read_csv("FBSchedulesSOS.csv", usecols=["TEAM", "FBRank"])
dfpfnsos = pd.read_csv("PFNSOS.csv", usecols=["Team", "PFNSOSRank"])
dfdk = pd.read_csv("DKSOS.csv", usecols=["Team", "DKRank"])
dfplayer = pd.read_csv("Player List.csv", usecols=["Rank", "Player", "Team", "POS"])
teammap = pd.read_csv("TeamDict.csv", index_col=0, squeeze=True).to_dict()

dataframes = [dfpff, dfpfn, dfcbs, dfcbsoline, dffbs, dfpfnsos, dfdk, dfplayer]

for df in dataframes:
    convert_column_headers_to_proper_case(df)

dfpff["Team"] = dfpff["Team"].map(lambda x: teammap.get(x, x))
dfcbsoline["Team"] = dfcbsoline["Team"].map(lambda x: teammap.get(x, x))
dfpfn["Team"] = dfpfn["Team"].map(lambda x: teammap.get(x, x))
dfcbs["Team"] = dfcbs["Team"].map(lambda x: teammap.get(x, x))
dffbs["Team"] = dffbs["Team"].map(lambda x: teammap.get(x, x))
dfpfnsos["Team"] = dfpfnsos["Team"].map(lambda x: teammap.get(x, x))
dfdk["Team"] = dfdk["Team"].map(lambda x: teammap.get(x, x))

dflist = [dfplayer]
for index in range(len(dflist)):
    dflist[index].replace(r"[^\w\s]|_\*", "", regex=True, inplace=True)
    dflist[index].replace(" Jr", "", regex=True, inplace=True)
    dflist[index].replace(" II", "", regex=True, inplace=True)

df_oline = dfpfn.merge(dfpff[["Team", "Pffrank"]], on=["Team"], how="left").merge(
    dfcbsoline[["Team", "Cbsolinerank"]], on=["Team"], how="left"
)
df_oline = df_oline.fillna(value=0)

cols = df_oline.columns.drop("Team")
df_oline[cols] = df_oline[cols].apply(pd.to_numeric, errors="coerce")
df_oline["Olinerank"] = df_oline.iloc[:, 1:3].mean(axis=1, numeric_only=True)

df_sos = dfcbs.merge(dffbs[["Team", "Fbrank"]], on=["Team"], how="left").merge(
    dfdk[["Team", "Dkrank"]], on=["Team"], how="left"
)
df_sos = df_sos.fillna(value=0)

cols2 = df_sos.columns.drop("Team")
df_sos[cols2] = df_sos[cols2].apply(pd.to_numeric, errors="coerce")
df_sos["Sosrank"] = df_sos.iloc[:, 1:3].mean(axis=1, numeric_only=True)

df_players = dfplayer.merge(
    df_oline[["Team", "Olinerank"]], on=["Team"], how="left"
).merge(df_sos[["Team", "Sosrank"]], on=["Team"], how="left")
df_players = df_players.rename(
    columns={"Rank": "ADP", "Player": "Name", "Pos": "Position"}
)

cols3 = ["ADP", "Olinerank", "Sosrank"]
df_players[cols3] = df_players[cols3].apply(pd.to_numeric, errors="coerce")
df_players["PlayerScore"] = df_players[["ADP", "Olinerank", "Sosrank"]].sum(axis=1)
sorted = df_players.sort_values(by=["PlayerScore"])
neworder = ["Name", "Team", "Position", "Olinerank", "Sosrank", "PlayerScore"]
sorted = sorted.reindex(columns=neworder)

sorted.to_csv("FantasyFootballRanks.csv", index=False)
