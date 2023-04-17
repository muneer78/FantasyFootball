import pandas as pd
import numpy as np

dfath = pd.read_csv('AthleticOLine.csv', usecols=['Team', 'Rank'])
dfcbs = pd.read_csv('CBSSportsSOS.csv', usecols=['Team', 'CBSRank'])
dffp = pd.read_csv('FantasyProsOLine.csv', usecols=['Team', 'FPRank'])
dffbs = pd.read_csv('FBSchedulesSOS.csv', usecols=['Team', 'FBRank'])
dfpff = pd.read_csv('PFFOLine.csv', usecols=['Team', 'PFFRank'])
dfplayer = pd.read_csv('Player List.csv'usecols=['RK', 'PLAYER NAME', 'TEAM', 'POS'])
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

cols = df_sos.columns.drop('Team')
df_oline[cols] = df_oline[cols].apply(pd.to_numeric, errors='coerce')
df_oline['OLineRank'] = df_oline.iloc[:, 1:3].mean(axis=1)

print(df_sos)

# # cols = ['Rank', 'LaghezzaRank']
# df1[cols] = df1[cols] = df1[cols].apply(pd.to_numeric, errors='coerce', axis=1)
#
# df1 = df1.drop_duplicates(subset=['Player', 'Rank'], keep='last')
# df1['Total Z-Score'] = df1['Total Z-Score_x'].mask(df1['Total Z-Score_x'].eq(0), df1['Total Z-Score_y'])
# df1['CombinedRank'] = df1['LaghezzaRank'].mask(df1['LaghezzaRank'].eq(0), df1['Rank'])
# df1.loc[(df1.LaghezzaRank.isnull(),  'LaghezzaRank')] = df1.Rank
# df1["RankDiff"] = df1["Rank"] - df1["LaghezzaRank"].mask(df1['LaghezzaRank'].eq(0), df1['Rank'])
# df1 = df1.rename(columns = {'Rank':'ADP'})
# df1.to_csv('fulldraftsheet.csv')
#
# df2 = pd.read_csv('fulldraftsheet.csv')
#
# columns = ['Player', 'Team_x', 'Total Z-Score', 'ADP', 'LaghezzaRank', 'RankDiff']
# df2 = pd.DataFrame(df2, columns=columns)
# df2 = df2.rename(columns = {'Team_x':'Team'})
# df2['ADP'] = sorted(df2['ADP'], key = float)
# df2.to_csv('draftsheet.csv')