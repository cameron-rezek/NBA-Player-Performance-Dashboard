import pandas as pd

def summarize_final_dataset():
    """Create a summary of our final dataset for Tableau"""
    
    # Load the raw stats (after re-running data collection)
    try:
        stats_df = pd.read_csv('data/raw/sample_player_stats.csv')
        
        print("=== FINAL DATASET SUMMARY ===")
        print(f"Total player-seasons: {len(stats_df)}")
        print(f"Unique players: {stats_df['PLAYER_NAME'].nunique()}")
        print(f"Season range: {stats_df['SEASON_ID'].min()} to {stats_df['SEASON_ID'].max()}")
        
        print(f"\nPlayers included:")
        for player in sorted(stats_df['PLAYER_NAME'].unique()):
            seasons = len(stats_df[stats_df['PLAYER_NAME'] == player])
            print(f"  - {player}: {seasons} seasons")
            
        print(f"\nReady for Tableau with rich, diverse dataset!")
        
    except FileNotFoundError:
        print("Run data_collection.py first to get the expanded dataset")

if __name__ == "__main__":
    summarize_final_dataset()