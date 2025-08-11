# NBA Data Collection Script

import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import time
import os

def get_all_players():
    """Get list of all NBA players"""
    print("Fetching all NBA players...")
    all_players = players.get_players()
    players_df = pd.DataFrame(all_players)
    print(f"Found {len(players_df)} players in database")
    return players_df

def get_sample_player_stats():
    """Get career stats for a few star players (for testing)"""
    star_players = {
        'LeBron James': 2544,
        'Stephen Curry': 201939,
        'Kevin Durant': 201142,
        'Giannis Antetokounmpo': 203507,
        'Luka Doncic': 1629029
    }
    
    all_stats = []
    
    for name, player_id in star_players.items():
        print(f"Getting stats for {name}...")
        try:
            # Get career stats
            career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
            stats_df = career_stats.get_data_frames()[0]  # Season totals
            
            # Add player name for easier identification
            stats_df['PLAYER_NAME'] = name
            all_stats.append(stats_df)
            
            # wait a bit between requests
            time.sleep(1)
            
        except Exception as e:
            print(f"Error getting data for {name}: {e}")
            continue
    
    # Combine all player stats
    if all_stats:
        combined_stats = pd.concat(all_stats, ignore_index=True)
        return combined_stats
    else:
        return pd.DataFrame()

def save_data(df, filename):
    """Save dataframe to CSV in the data/raw folder"""
    # Make sure the directory exists
    os.makedirs('data/raw', exist_ok=True)
    
    filepath = f'data/raw/{filename}'
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")

def main():
    """Main function to run the data collection"""
    print("=== NBA Data Collection Started ===")
    
    # Step 1: Get all players list
    players_df = get_all_players()
    save_data(players_df, 'all_players.csv')
    
    # Step 2: Get sample career stats
    stats_df = get_sample_player_stats()
    if not stats_df.empty:
        save_data(stats_df, 'sample_player_stats.csv')
        print(f"\nCollected stats for {stats_df['PLAYER_NAME'].nunique()} players")
        print(f"Data shape: {stats_df.shape}")
        print("\nColumns available:")
        print(stats_df.columns.tolist())
    else:
        print("No stats data collected")
    
    print("\n=== Data Collection Complete ===")

if __name__ == "__main__":
    main()