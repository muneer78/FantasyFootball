import pandas as pd
import numpy as np

dfath = pd.read_csv('AthleticOLine.csv')
dfcbs = pd.read_csv('CBSSportsSOS.csv')
dffp = pd.read_csv('FantasyProsOLine.csv')
dffbs = pd.read_csv('PFFOLine.csv')
dffpp = pd.read_csv('fg.csv')
dfplayer = pd.read_csv('Player List.csv')

dflist = [dfath, dfcbs, dffpp, dffp, dffbs, dfplayer]
for index in range(len(dflist)):
    dflist[index].replace(r'[^\w\s]|_\*', '', regex=True, inplace = True)
    dflist[index].replace(' Jr', '', regex=True, inplace = True)
    dflist[index].replace(' II', '', regex=True, inplace = True)

dfadp = dfadp.astype(str)

func = lambda x: ''.join([i[:3] for i in x.strip().split(' ')])
dffgpit['Key'] = dffgpit.Name.apply(func)
dfstuff['Key'] = dfstuff.player_name.apply(func)
dfadp['Key'] = dfadp.Player.apply(func)
dfzpit['Key'] = dfzpit.Name.apply(func)
dfzhit['Key'] = dfzhit.Name.apply(func)
dffghit['Key'] = dffghit.Name.apply(func)
dflaghezza['Key'] = dflaghezza.Name.apply(func)

dflist2 = [dffgpit, dfzpit, dfadp, dfstuff]
for index in range(len(dflist2)):
    dflist2[index].columns.str.strip()

dfadp = dfadp.drop(['ESPN','CBS','RTS','NFBC','FT'], axis=1)

df1 = dfadp.merge(dffgpit, on=["Key"], how="left").merge(dfstuff[['Key', 'STUFFplus', 'LOCATIONplus', 'PITCHINGplus']], on=["Key"], how="left").merge(dfzpit[['Key', 'Total Z-Score']], on=["Key"], how="left").merge(dfzhit[['Key', 'Total Z-Score']], on=["Key"], how="left").merge(dffghit, on=["Key"], how="left").merge(dflaghezza[['Key', 'LaghezzaRank']], on=["Key"], how="left")
df1 = df1.fillna(value=0)

cols = ['Rank', 'LaghezzaRank']
df1[cols] = df1[cols] = df1[cols].apply(pd.to_numeric, errors='coerce', axis=1)

df1 = df1.drop_duplicates(subset=['Player', 'Rank'], keep='last')
df1['Total Z-Score'] = df1['Total Z-Score_x'].mask(df1['Total Z-Score_x'].eq(0), df1['Total Z-Score_y'])
df1['CombinedRank'] = df1['LaghezzaRank'].mask(df1['LaghezzaRank'].eq(0), df1['Rank'])
df1.loc[(df1.LaghezzaRank.isnull(),  'LaghezzaRank')] = df1.Rank
df1["RankDiff"] = df1["Rank"] - df1["LaghezzaRank"].mask(df1['LaghezzaRank'].eq(0), df1['Rank'])
df1 = df1.rename(columns = {'Rank':'ADP'})
df1.to_csv('fulldraftsheet.csv')

df2 = pd.read_csv('fulldraftsheet.csv')

columns = ['Player', 'Team_x', 'Total Z-Score', 'ADP', 'LaghezzaRank', 'RankDiff']
df2 = pd.DataFrame(df2, columns=columns)
df2 = df2.rename(columns = {'Team_x':'Team'})
df2['ADP'] = sorted(df2['ADP'], key = float)
df2.to_csv('draftsheet.csv')

df3 = pd.read_csv('draftsheet.csv', index_col=False)
columns = ['Player', 'Team']
df3 = pd.DataFrame(df3, columns=columns)
df3.to_csv('fantrax.csv')