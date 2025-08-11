import pandas as pd

def explore_data():
    print("=== NBA Data Exploration ===\n")
    
    # Load the collected data
    players_df = pd.read_csv('data/raw/all_players.csv')
    stats_df = pd.read_csv('data/raw/sample_player_stats.csv')
    
    print("1. PLAYERS DATA:")
    print(f"   - Total players in database: {len(players_df)}")
    print(f"   - Columns: {list(players_df.columns)}")
    print("\n   Sample players:")
    print(players_df.head())
    
    print("\n2. PLAYER STATS DATA:")
    print(f"   - Total rows (player-seasons): {len(stats_df)}")
    print(f"   - Players included: {stats_df['PLAYER_NAME'].unique()}")
    print(f"   - Seasons covered: {stats_df['SEASON_ID'].min()} to {stats_df['SEASON_ID'].max()}")
    
    print(f"\n   Available stats columns:")
    for i, col in enumerate(stats_df.columns):
        print(f"   {col}", end="")
        if (i + 1) % 3 == 0:
            print()
        else:
            print(", ", end="")
    
    print("\n\n3. SAMPLE CAREER DATA (LeBron's recent seasons):")
    lebron_recent = stats_df[(stats_df['PLAYER_NAME'] == 'LeBron James')].tail(3)
    print(lebron_recent[['SEASON_ID', 'PLAYER_NAME', 'GP', 'PTS', 'REB', 'AST', 'FG_PCT']])
    
    return players_df, stats_df

if __name__ == "__main__":
    players_df, stats_df = explore_data()