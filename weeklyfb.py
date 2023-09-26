import pandas as pd

# Read the data from the CSV file into a dataframe
df = pd.read_csv("FantasyPros_Fantasy_Football_2023_Offense_Snap_Count_Analysis.csv")

# Read the "fbexcluded.csv" file into a dataframe
df_excluded = pd.read_csv("fbexcluded.csv")

def clean_player_data(df):
    df.replace(r"[^\w\s]|_\*| Jr| III", "", regex=True, inplace=True)
    return df

# Create a list of excluded player names
excluded_players = df_excluded["PLAYER NAME"].tolist()

# Create dataframe 1 where Pos = QB
df1 = df[df['Pos'] == 'QB']

# Create dataframe 2 where Pos is WR, RB, or TE
df2 = df[df['Pos'].isin(['WR', 'RB', 'TE'])]

df1 = clean_player_data(df1)
df2 = clean_player_data(df2)

# Filter out players from df1 and df2 if their names are in the excluded list
df1_filtered = df1[~df1["Player"].isin(excluded_players)]
df2_filtered = df2[~df2["Player"].isin(excluded_players)]

# Create dataframe 1 where Pos = QB
df1_filtered = df1_filtered[df1_filtered['Pos'] == 'QB']

# Create dataframe 2 where Pos is WR, RB, or TE
df2 = df2_filtered[df2_filtered['Pos'].isin(['WR', 'RB', 'TE'])]

# Sort both dataframes by "Fantasy Pts" column
df1_filtered = df1_filtered.sort_values(by="Fantasy Pts", ascending=False)
df2_filtered = df2_filtered.sort_values(by="Fantasy Pts", ascending=False)

# Write df1 to a CSV file with a title
with open("fbpickups.csv", "w", newline="") as csvfile:
    # Write title for df1
    csvfile.write("QBs\n")
    # Write headers for df1
    csvfile.write(','.join(df1_filtered.columns) + "\n")
    # Write data for df1
    for _, row in df1_filtered.head(10).iterrows():
        csvfile.write(','.join(map(str, row.values)) + "\n")

# Append df2 to the same CSV file with a title and headers
with open("fbpickups.csv", "a", newline="") as csvfile:
    # Write title for df2
    csvfile.write("\n\nWR/RB/TE\n")
    # Write headers for df2
    csvfile.write(','.join(df2_filtered.columns) + "\n")
    # Write data for df2
    for _, row in df2_filtered.head(50).iterrows():
        csvfile.write(','.join(map(str, row.values)) + "\n")
