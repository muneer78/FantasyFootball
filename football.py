import pandas as pd

dfath = pd.read_csv('AthleticOLine.csv', usecols=['Team', 'Rank'])
dfcbs = pd.read_csv('CBSSportsSOS.csv', usecols=['Team', 'CBSRank'])
dffp = pd.read_csv('FantasyProsOLine.csv', usecols=['Team', 'FPRank'])
dffbs = pd.read_csv('FBSchedulesSOS.csv', usecols=['Team', 'FBRank'])
dfpff = pd.read_csv('PFFOLine.csv', usecols=['Team', 'PFFRank'])
dfplayer = pd.read_csv('Player List.csv', usecols=['RK', 'PLAYER NAME', 'Team', 'POS'])
teammap = pd.read_csv('TeamDict.csv', index_col=0, squeeze=True).to_dict()

dfcbs['Team'] = dfcbs['Team'].map(teammap)
dffp['Team'] = dffp['Team'].map(teammap)
dffbs['Team'] = dffbs['Team'].map(teammap)
dfpff['Team'] = dfpff['Team'].map(teammap)

dflist = [dfplayer]
for index in range(len(dflist)):
    dflist[index].replace(r'[^\w\s]|_\*', '', regex=True, inplace = True)
    dflist[index].replace(' Jr', '', regex=True, inplace = True)
    dflist[index].replace(' II', '', regex=True, inplace = True)

df_oline = dffp.merge(dfpff[['Team', 'PFFRank']], on=["Team"], how="left").merge(dfath[['Team', 'Rank']], on=["Team"], how="left")
df_oline = df_oline.fillna(value=0)

cols = df_oline.columns.drop('Team')
df_oline[cols] = df_oline[cols].apply(pd.to_numeric, errors='coerce')
df_oline['OLineRank'] = df_oline.iloc[:, 1:3].mean(axis=1)

df_sos = dfcbs.merge(dffbs[['Team', 'FBRank']], on=["Team"], how="left")
df_sos = df_sos.fillna(value=0)

cols2 = df_sos.columns.drop('Team')
df_sos[cols2] = df_sos[cols2].apply(pd.to_numeric, errors='coerce')
df_sos['SOSRank'] = df_sos.iloc[:, 1:3].mean(axis=1)

df_players = dfplayer.merge(df_oline[['Team', 'OLineRank']], on=['Team'], how="left").merge(df_sos[['Team', 'SOSRank']], on=['Team'], how="left")
df_players = df_players.rename(columns = {'RK':'ADP', 'PLAYER NAME':'Name', 'POS':'Position'})

cols3 = ['ADP', "OLineRank", 'SOSRank']
df_players[cols3] = df_players[cols3].apply(pd.to_numeric, errors='coerce')
df_players['PlayerScore'] = df_players[['ADP', "OLineRank", 'SOSRank']].sum(axis=1)
sorted = df_players.sort_values(by=['PlayerScore'])
neworder = ['Name', 'Team', 'Position', 'OLineRank', 'SOSRank', 'PlayerScore']
sorted = sorted.reindex(columns=neworder)

sorted.to_csv('FantasyFootballRanks.csv', index=False)