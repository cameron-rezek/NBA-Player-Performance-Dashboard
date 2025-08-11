import pandas as pd

def create_tableau_ready_data():
    """Create a single, clean dataset perfect for Tableau"""
    
    # Load processed data
    df = pd.read_csv('data/processed/player_stats_processed.csv')
    career_df = pd.read_csv('data/processed/career_summaries.csv')
    
    # Add some final calculated fields for Tableau
    df['DECADE'] = (df['SEASON_ID'].str[:4].astype(int) // 10) * 10
    df['SEASON_YEAR'] = df['SEASON_ID'].str[:4].astype(int)
    
    # Save final dataset
    df.to_csv('data/processed/nba_tableau_data.csv', index=False)
    career_df.to_csv('data/processed/nba_career_summary.csv', index=False)
    
    print("Tableau-ready datasets created!")
    print(f"Main dataset: {len(df)} rows, {len(df.columns)} columns")
    print(f"Career summary: {len(career_df)} players")

if __name__ == "__main__":
    create_tableau_ready_data()