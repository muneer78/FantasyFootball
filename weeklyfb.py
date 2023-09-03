import pandas as pd
from datetime import date, datetime

excluded = pd.read_csv("fbexcluded.csv")

# Load the data
dfrbdsm_off = pd.read_csv('rbsdm.comstats.csv')
dfrbdsm_def = pd.read_csv('rbsdm.comstats (1).csv')
dfrbdsm_qb = pd.read_csv('rbsdm.comstats (2).csv')
dffbref_off = pd.read_csv('off.csv')
dffbref_qb = pd.read_csv('qb.csv')
dffbref_def = pd.read_csv('def.csv')
dffbref_advdef = pd.read_csv('advdef.csv')

today = date.today()

def rb(filepath):
    '''Creates weekly offensive calcs'''
    df = pd.read_csv(filepath, index_col=["-additional"])

    df = df.drop(0)
    filter = df[(df["G"] >= 1)]
    df = df.applymap(lambda x: x.replace('*', ''))
    df.rename(columns={"K%-": "K", "BB%-": "BB"}, inplace=True)
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["-additional"].isin(excluded["PlayerId"])]

    filters = df[
        (df["Att"] > 8)
        & (df["Y/G"] > 45)
        & (df["A/G"] > 9)
    ].sort_values(by="YScm", ascending=False)
    return filters

def qb(filepath):
    '''Creates weekly offensive calcs'''
    df = pd.read_csv(filepath, index_col=["-additional"])

    df = df.drop(0)
    filter = df[(df["G"] >= 1)]
    df = df.applymap(lambda x: x.replace('*', ''))
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["-additional"].isin(excluded["PlayerId"])]

    filters = df[
        (df["Att"] > 15)
        & (df["Int%"] <= 2.5 )
        & (df["ANY/A"] >= 5.5)
    ].sort_values(by="YScm", ascending=False)
    return filters

def wr(filepath):
    '''Creates weekly offensive calcs'''
    df = pd.read_csv(filepath, index_col=["-additional"])

    df = df.drop(0)
    filter = df[(df["G"] >= 1)]
    df = df.applymap(lambda x: x.replace('*','').replace('%', ''))
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["-additional"].isin(excluded["PlayerId"])]

    filters = df[
        (df["Succ%"] >= 50.0)
        & (df["Y/G"] > 45)
        & (df["R/G"] > 4)
        & (df["Ctch%"] > 70.0)
    ].sort_values(by="YScm", ascending=False)
    return filters

def te(filepath):
    '''Creates weekly offensive calcs'''
    df = pd.read_csv(filepath, index_col=["-additional"])

    df = df.drop(0)
    filter = df[(df["G"] >= 1)]
    df.columns = df.columns.str.replace("[+,-,%,*,]", "", regex=True)
    df = df.applymap(lambda x: x.replace('*', ''))
    df.rename(columns={"K%-": "K", "BB%-": "BB"}, inplace=True)
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["-additional"].isin(excluded["PlayerId"])]

    filters = df[
        (df["wRC"] > 135)
        & (df["OPS"] > 0.8)
        & (df["K"] < 100)
        & (df["BB"] > 100)
        & (df["Off"] > 3)
        & (df["Barrel"] > 10)
    ].sort_values(by="Off", ascending=False)
    return filters

def defense(filepath):
    df = pd.read_csv(filepath, index_col=["-additional"])

    df = df.drop(0)
    filter = df[(df["G"] >= 1)]

    df.columns = df.columns.str.replace("[+,-,%,]", "", regex=True)
    df = df.applymap(lambda x: x.replace('*', ''))
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["-additional"].isin(excluded["PlayerId"])]

    filters = df[
        (df["wRC"] > 115)
        & (df["OPS"] > 0.8)
        & (df["K"] < 110)
        & (df["BB"] > 90)
        & (df["Off"] > 5)
        & (df["Barrel"] > 10)
        & (df["PA"] > 40)
    ].sort_values(by="Off", ascending=False)
    return filters

# Preprocess and export the dataframes to Excel workbook sheets
hitdaywindow = [7, 14]
pawindow = [40]
pitchdaywindow = [14, 30]
ipwindow = [10, 30]

df_list = []

# Initialize a list to keep track of printed titles
printed_titles = []

with open("weeklyadds.csv", "w+") as f:
    for w in hitdaywindow:
        df = hitters_wk_preprocessing(f"fgl_hitters_last_{w}.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"Hitters Last {w} Days"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)

    for w in pawindow:
        df = hitters_pa_preprocessing(f"fgl_hitters_{w}_pa.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"Hitters {w} PA"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)

    for w in ipwindow:
        df = sp_preprocessing(f"fgl_pitchers_{w}_ip.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"SP {w} Innings"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)

        df = rp_preprocessing(f"fgl_pitchers_{w}_ip.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"RP {w} Innings"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)

    for w in pitchdaywindow:
        df = sp_preprocessing(f"fgl_pitchers_last_{w}.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"Pitchers Last {w} Days"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)

        df = rp_preprocessing(f"fgl_pitchers_last_{w}.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"RP Last {w} Days"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)
