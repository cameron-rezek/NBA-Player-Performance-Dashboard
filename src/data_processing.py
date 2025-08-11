import pandas as pd
import numpy as np

def load_and_clean_data():
    """Load raw data and perform basic cleaning"""
    print("Loading and cleaning NBA data...")
    
    stats_df = pd.read_csv('data/raw/sample_player_stats.csv')
    
    # Basic cleaning
    # Remove rows where player didn't play (0 games played)
    stats_df = stats_df[stats_df['GP'] > 0]
    
    # Fill any missing values with 0
    stats_df = stats_df.fillna(0)
    
    print(f"Cleaned data: {len(stats_df)} player-seasons")
    return stats_df

def calculate_per_game_stats(df):
    """Calculate per-game averages"""
    print("Calculating per-game statistics...")
    
    # Points, rebounds, assists per game
    df['PPG'] = df['PTS'] / df['GP']
    df['RPG'] = df['REB'] / df['GP'] 
    df['APG'] = df['AST'] / df['GP']
    df['SPG'] = df['STL'] / df['GP']  # Steals per game
    df['BPG'] = df['BLK'] / df['GP']  # Blocks per game
    
    # Minutes per game
    df['MPG'] = df['MIN'] / df['GP']
    
    return df

def calculate_advanced_metrics(df):
    """Calculate advanced basketball metrics"""
    print("Calculating advanced metrics...")
    
    # True Shooting Percentage (accounts for 3-pointers and free throws)
    df['TS_PCT'] = df['PTS'] / (2 * (df['FGA'] + (0.44 * df['FTA'])))
    df['TS_PCT'] = df['TS_PCT'].fillna(0)
    
    # Simple Efficiency Rating (points + rebounds + assists - missed shots - turnovers)
    df['EFFICIENCY'] = (df['PTS'] + df['REB'] + df['AST'] + df['STL'] + df['BLK']) - \
                      ((df['FGA'] - df['FGM']) + (df['FTA'] - df['FTM']) + df['TOV'])
    
    # Efficiency per minute played
    df['EFF_PER_MIN'] = df['EFFICIENCY'] / df['MIN']
    df['EFF_PER_MIN'] = df['EFF_PER_MIN'].fillna(0)
    
    # Usage estimate (how much of team's offense when player is on court)
    df['USAGE_EST'] = (df['FGA'] + (df['FTA'] * 0.44) + df['TOV']) / df['GP']
    
    return df

def add_performance_categories(df):
    """Categorize players by performance level"""
    print("Adding performance categories...")
    
    # Only categorize seasons where player played significant minutes
    active_seasons = df[df['MPG'] >= 15].copy()
    
    if len(active_seasons) > 0:
        # Create scoring tiers based on PPG
        active_seasons['SCORING_TIER'] = pd.cut(active_seasons['PPG'], 
                                               bins=[0, 10, 15, 20, 25, 50], 
                                               labels=['Bench', 'Role Player', 'Starter', 'Star', 'Superstar'])
        
        # Merge back to main dataframe
        df = df.merge(active_seasons[['PLAYER_NAME', 'SEASON_ID', 'SCORING_TIER']], 
                     on=['PLAYER_NAME', 'SEASON_ID'], how='left')
    
    return df

def create_career_summary(df):
    """Create career summary statistics"""
    print("Creating career summaries...")
    
    career_stats = df.groupby('PLAYER_NAME').agg({
        'SEASON_ID': 'count',  # Number of seasons
        'GP': 'sum',           # Total games
        'PTS': 'sum',          # Total points
        'PPG': 'mean',         # Average PPG across career
        'RPG': 'mean',         # Average RPG
        'APG': 'mean',         # Average APG
        'TS_PCT': 'mean',      # Average shooting efficiency
        'EFFICIENCY': 'mean'   # Average efficiency
    }).round(2)
    
    career_stats.columns = ['SEASONS', 'TOTAL_GAMES', 'TOTAL_PTS', 
                           'CAREER_PPG', 'CAREER_RPG', 'CAREER_APG', 
                           'CAREER_TS_PCT', 'CAREER_EFFICIENCY']
    
    return career_stats

def main():
    """Main processing pipeline"""
    print("=== NBA Data Processing Pipeline ===\n")
    
    # Step 1: Load and clean
    df = load_and_clean_data()
    
    # Step 2: Calculate per-game stats
    df = calculate_per_game_stats(df)
    
    # Step 3: Calculate advanced metrics
    df = calculate_advanced_metrics(df)
    
    # Step 4: Add performance categories
    df = add_performance_categories(df)
    
    # Step 5: Create career summary
    career_summary = create_career_summary(df)
    
    # Save processed data
    print("\nSaving processed data...")
    df.to_csv('data/processed/player_stats_processed.csv', index=False)
    career_summary.to_csv('data/processed/career_summaries.csv')
    
    print(f"\nProcessing complete!")
    print(f"Processed {len(df)} player-seasons")
    print(f"Career summaries for {len(career_summary)} players")
    
    # Show sample results
    print("\nSample processed data:")
    sample_cols = ['PLAYER_NAME', 'SEASON_ID', 'PPG', 'RPG', 'APG', 'TS_PCT', 'EFFICIENCY', 'SCORING_TIER']
    print(df[sample_cols].head(10))

if __name__ == "__main__":
    main()