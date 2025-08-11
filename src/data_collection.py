# NBA Data Collection Script
# This script fetches basic NBA player data and saves it to CSV

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
    """Get career stats for a diverse set of current and recent players"""
    # Expanded list with different eras, positions, and playing styles
    star_players = {
        # Current Superstars
        'LeBron James': 2544,
        'Stephen Curry': 201939,
        'Kevin Durant': 201142,
        'Giannis Antetokounmpo': 203507,
        'Luka Doncic': 1629029,
        'Nikola Jokic': 203999,
        'Joel Embiid': 203954,
        'Jayson Tatum': 1628369,
        
        # Recent Legends
        'Kobe Bryant': 977,
        'Tim Duncan': 1495,
        'Dirk Nowitzki': 1717,
        'Chris Paul': 101108,
        'Kawhi Leonard': 202695,
        'Russell Westbrook': 201566,
        
        # Rising Stars & Different Positions
        'Anthony Edwards': 1630162,
        'Ja Morant': 1629630,
        'Zion Williamson': 1629627,
        'Damian Lillard': 203081,
        'Jimmy Butler': 202710,
        'Paul George': 202331
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
            
            # Be nice to the API - wait a bit between requests
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