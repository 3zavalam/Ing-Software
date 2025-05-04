import os
import LanusStats as ls
import pandas as pd

fbref = ls.Fbref()

output_path = './data/radar'

def rename_duplicate_columns(df):
    seen = {}
    new_columns = []
    for col in df.columns:
        if col not in seen:
            seen[col] = 0
            new_columns.append(col)
        else:
            seen[col] += 1
            new_columns.append(f"{col}_{seen[col]}")
    df.columns = new_columns
    return df

def get_fbref_stats(leagues_seasons):
    all_players = []
    all_keepers = []

    # Loop through each league and season in the dictionary
    for league, season in leagues_seasons.items():
        # Create a directory for the league if it doesn't exist
        league_path = os.path.join(output_path, league.replace(" ", "_"))
        os.makedirs(league_path, exist_ok=True)

        # Retrieve stats for the league and season
        all_stats = fbref.get_all_player_season_stats(league, season, save_csv=False)

        # Player stats and keeper stats
        players_df = all_stats[0]
        players_df = players_df[players_df['stats_Pos'] != 'GK']
        keepers_df = all_stats[1]

        # Ensure 'stats_90s' column is numeric
        players_df['stats_90s'] = pd.to_numeric(players_df['stats_90s'], errors='coerce')
        keepers_df['keepers_90s'] = pd.to_numeric(keepers_df['keepers_90s'], errors='coerce')

        # Drop rows with NaN values in 'stats_90s' after conversion
        players_df = players_df.dropna(subset=['stats_90s'])
        keepers_df = keepers_df.dropna(subset=['keepers_90s'])

        # Calculate quantile thresholds for each league
        threshold_players_90s = players_df['stats_90s'].quantile(0.35)
        threshold_keepers_90s = keepers_df['keepers_90s'].quantile(0.35)

        # Filter players and keepers based on their respective thresholds
        players_df = players_df[players_df['stats_90s'] >= threshold_players_90s]
        keepers_df = keepers_df[keepers_df['keepers_90s'] >= threshold_keepers_90s]

        # Save filtered players and keepers to league-specific CSV files
        players_file_path = os.path.join(league_path, 'players.csv')
        keepers_file_path = os.path.join(league_path, 'keepers.csv')

        players_df.to_csv(players_file_path, index=False)
        keepers_df.to_csv(keepers_file_path, index=False)

        # Append filtered data to the lists for all leagues
        all_players.append(players_df)
        all_keepers.append(keepers_df)

    # Concatenate all player and keeper stats across leagues
    all_players_df = pd.concat(all_players, ignore_index=True)
    all_keepers_df = pd.concat(all_keepers, ignore_index=True)

    # Save the concatenated DataFrames
    players_file_path = os.path.join(league_path, 'players.csv')
    keepers_file_path = os.path.join(league_path, 'keepers.csv')

    # Renombrar columnas duplicadas antes de guardar
    players_df = rename_duplicate_columns(players_df)
    keepers_df = rename_duplicate_columns(keepers_df)

    players_df.to_csv(players_file_path, index=False)
    keepers_df.to_csv(keepers_file_path, index=False)


    print('Players and keepers data saved by league and concatenated into all_players and all_keepers.')
    return all_players, all_keepers