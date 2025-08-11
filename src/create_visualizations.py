import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_processed_data():
    """Load our cleaned and processed data"""
    df = pd.read_csv('data/processed/player_stats_processed.csv')
    career_df = pd.read_csv('data/processed/career_summaries.csv')
    return df, career_df

def create_charts():
    """Create key visualizations"""
    df, career_df = load_processed_data()
    
    # Set style
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Chart 1: Career PPG comparison
    career_df_sorted = career_df.sort_values('CAREER_PPG', ascending=True)
    axes[0,0].barh(career_df_sorted['PLAYER_NAME'], career_df_sorted['CAREER_PPG'])
    axes[0,0].set_title('Career Points Per Game')
    axes[0,0].set_xlabel('PPG')
    
    # Chart 2: Efficiency vs Usage scatter
    recent_seasons = df[df['SEASON_ID'].str.contains('2020|2021|2022|2023')]
    if len(recent_seasons) > 0:
        axes[0,1].scatter(recent_seasons['USAGE_EST'], recent_seasons['EFFICIENCY'])
        axes[0,1].set_xlabel('Usage Estimate')
        axes[0,1].set_ylabel('Efficiency')
        axes[0,1].set_title('Usage vs Efficiency (Recent Seasons)')
    
    # Chart 3: LeBron's career trajectory
    lebron_data = df[df['PLAYER_NAME'] == 'LeBron James'].copy()
    lebron_data['SEASON_YEAR'] = lebron_data['SEASON_ID'].str[:4].astype(int)
    axes[1,0].plot(lebron_data['SEASON_YEAR'], lebron_data['PPG'], marker='o', label='PPG')
    axes[1,0].plot(lebron_data['SEASON_YEAR'], lebron_data['RPG'], marker='s', label='RPG')
    axes[1,0].plot(lebron_data['SEASON_YEAR'], lebron_data['APG'], marker='^', label='APG')
    axes[1,0].set_title("LeBron James Career Trajectory")
    axes[1,0].set_xlabel('Season')
    axes[1,0].legend()
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Chart 4: Performance tier distribution
    tier_counts = df['SCORING_TIER'].value_counts()
    axes[1,1].pie(tier_counts.values, labels=tier_counts.index, autopct='%1.1f%%')
    axes[1,1].set_title('Player Performance Distribution')
    
    plt.tight_layout()
    plt.savefig('data/processed/nba_analysis_charts.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Charts saved as 'nba_analysis_charts.png'")

if __name__ == "__main__":
    create_charts()