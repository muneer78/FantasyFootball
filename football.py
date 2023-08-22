"""
Use pandas to create and work with dataframes
"""
import pandas as pd
import pandas_log

def convert_column_headers_to_proper_case(df_temp):
    """
    Define the function to convert column headers to proper case
    """
    df_temp.columns = [column.title() for column in df_temp.columns]


dfpff = pd.read_csv("PFFOLine.csv", usecols=["Team", "PFFRank"])
dfcbsoline = pd.read_csv("CBSOLine.csv", usecols=["Team", "CBSOLineRank"])
dfpfn = pd.read_csv("PFNOLine.csv", usecols=["Team", "Rank"])
dfcbs = pd.read_csv("CBSSportsSOS.csv", usecols=["Team", "CBSRank"])
dffbs = pd.read_csv("FBSchedulesSOS.csv", usecols=["TEAM", "FBRank"])
dfpfnsos = pd.read_csv("PFNSOS.csv", usecols=["Team", "PFNSOSRank"])
dfdk = pd.read_csv("DKSOS.csv", usecols=["Team", "DKRank"])
dfplayer = pd.read_csv("Player List.csv", usecols=["Rank", "Player", "Team", "POS"])
df_laghezza = pd.read_csv("laghezzaranks.csv")
# noinspection PyArgumentList
teammap = pd.read_csv("TeamDict.csv", index_col=0).squeeze().to_dict()

dataframes = [dfpff, dfpfn, dfcbs, dfcbsoline, dffbs, dfpfnsos, dfdk, dfplayer, df_laghezza]

for df in dataframes:
    convert_column_headers_to_proper_case(df)

dfpff["Team"] = dfpff["Team"].map(lambda x: teammap.get(x, x))
dfcbsoline["Team"] = dfcbsoline["Team"].map(lambda x: teammap.get(x, x))
dfpfn["Team"] = dfpfn["Team"].map(lambda x: teammap.get(x, x))
dfcbs["Team"] = dfcbs["Team"].map(lambda x: teammap.get(x, x))
dffbs["Team"] = dffbs["Team"].map(lambda x: teammap.get(x, x))
dfpfnsos["Team"] = dfpfnsos["Team"].map(lambda x: teammap.get(x, x))
dfdk["Team"] = dfdk["Team"].map(lambda x: teammap.get(x, x))

dflist = [dfplayer, df_laghezza]
for index, df in enumerate(dflist):
    df.replace(r"[^\w\s]|_\*", "", regex=True, inplace=True)
    df.replace(" Jr", "", regex=True, inplace=True)
    df.replace(" II", "", regex=True, inplace=True)

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
    df_oline[["Team", "Olinerank"]], on=["Team"], how="left")\
    .merge(df_laghezza[['Name', 'Ranking']], left_on='Player', right_on='Name', how='left')\
    .merge(df_sos[["Team", "Sosrank"]], on=["Team"], how="left")

# Drop the 'name' column as it's no longer needed
df_players.drop(columns=['Name'], inplace=True)

df_players = df_players.rename(
    columns={"Rank": "ADP", "Player": "Name", "Pos": "Position", "Ranking": "LagRank"}
)

cols3 = ["ADP", "Olinerank", "Sosrank"]
df_players[cols3] = df_players[cols3].apply(pd.to_numeric, errors="coerce")
df_players["PlayerScore"] = df_players[["ADP", "Olinerank", "Sosrank"]].sum(axis=1)
sorted = df_players.sort_values(by=["PlayerScore"])
neworder = ["Name", "Team", "Position", "Olinerank", "Sosrank", "LagRank", "PlayerScore"]
# sorted = sorted.reindex(columns=neworder)

sorted.to_csv("FantasyFootballRanks.csv", index=False)
