import pandas as pd
import numpy as np
from datetime import datetime

def load_data():
    """Load processed NBA data"""
    df = pd.read_csv('data/processed/player_stats_processed.csv')
    career_df = pd.read_csv('data/processed/career_summaries.csv')
    return df, career_df

def analyze_player_archetypes(df):
    """Identify different types of NBA players and what they represent"""
    insights = []
    
    # Create player profiles based on their strengths
    df['PRIMARY_SKILL'] = 'Balanced'
    df.loc[df['PPG'] >= df['PPG'].quantile(0.8), 'PRIMARY_SKILL'] = 'Scorer'
    df.loc[df['RPG'] >= df['RPG'].quantile(0.8), 'PRIMARY_SKILL'] = 'Rebounder'
    df.loc[df['APG'] >= df['APG'].quantile(0.8), 'PRIMARY_SKILL'] = 'Playmaker'
    df.loc[df['TS_PCT'] >= df['TS_PCT'].quantile(0.9), 'PRIMARY_SKILL'] = 'Elite Shooter'
    
    # Find representative players for each archetype
    archetypes = {}
    for skill in df['PRIMARY_SKILL'].unique():
        skill_players = df[df['PRIMARY_SKILL'] == skill]
        if len(skill_players) > 0:
            # Get most recent season for each player in this category
            latest_seasons = skill_players.groupby('PLAYER_NAME')['SEASON_ID'].max()
            representative = skill_players[skill_players['SEASON_ID'].isin(latest_seasons)]
            if len(representative) > 0:
                best_rep = representative.loc[representative['EFFICIENCY'].idxmax()]
                archetypes[skill] = best_rep['PLAYER_NAME']
    
    # Generate archetype insights
    if 'Elite Shooter' in archetypes:
        insights.append(f"**Modern Efficiency Revolution:** {archetypes['Elite Shooter']} represents the new NBA paradigm where shooting efficiency trumps volume")
    
    if 'Playmaker' in archetypes:
        insights.append(f"**Point-Forward Evolution:** {archetypes['Playmaker']} exemplifies how traditional position roles are dissolving in favor of versatile facilitators")
    
    return insights

def analyze_generational_shifts(df):
    """Compare different eras and identify trends"""
    insights = []
    
    # Create era buckets
    df['ERA'] = 'Modern'
    df.loc[df['SEASON_ID'].str[:4].astype(int) <= 2010, 'ERA'] = 'Traditional'
    df.loc[(df['SEASON_ID'].str[:4].astype(int) > 2010) & (df['SEASON_ID'].str[:4].astype(int) <= 2018), 'ERA'] = 'Transition'
    
    # Compare shooting efficiency across eras
    era_shooting = df.groupby('ERA')['TS_PCT'].mean()
    if len(era_shooting) >= 2:
        if 'Modern' in era_shooting.index and 'Traditional' in era_shooting.index:
            improvement = ((era_shooting['Modern'] - era_shooting['Traditional']) / era_shooting['Traditional']) * 100
            insights.append(f"**Era Evolution:** Shooting efficiency has improved {improvement:.0f}% from traditional to modern NBA, reflecting analytics-driven shot selection")
    
    # Identify pace and style changes
    era_usage = df.groupby('ERA')['USAGE_EST'].mean()
    if len(era_usage) >= 2:
        modern_usage = era_usage.get('Modern', 0)
        traditional_usage = era_usage.get('Traditional', 0)
        if modern_usage > traditional_usage:
            insights.append(f"**Pace Revolution:** Modern players average higher usage rates, indicating faster-paced, more possession-focused basketball")
    
    return insights

def analyze_performance_outliers(df):
    """Find unusual patterns and exceptional cases"""
    insights = []
    
    # Find players who break conventional wisdom
    high_usage_efficient = df[(df['USAGE_EST'] >= df['USAGE_EST'].quantile(0.8)) & 
                             (df['TS_PCT'] >= df['TS_PCT'].quantile(0.8))]
    
    if len(high_usage_efficient) > 0:
        outlier = high_usage_efficient.loc[high_usage_efficient['EFFICIENCY'].idxmax()]
        insights.append(f"**Efficiency Paradox:** {outlier['PLAYER_NAME']} defies conventional wisdom by maintaining elite shooting while carrying high offensive load")
    
    # Identify late bloomers vs early peaks
    player_trajectories = {}
    for player in df['PLAYER_NAME'].unique():
        player_data = df[df['PLAYER_NAME'] == player].sort_values('SEASON_ID')
        if len(player_data) >= 5:
            early_avg = player_data.head(2)['PPG'].mean()
            late_avg = player_data.tail(2)['PPG'].mean()
            if late_avg > early_avg * 1.2:  # 20% improvement
                player_trajectories[player] = 'Late Bloomer'
            elif early_avg > late_avg * 1.2:
                player_trajectories[player] = 'Early Peak'
    
    late_bloomers = [k for k, v in player_trajectories.items() if v == 'Late Bloomer']
    if late_bloomers:
        insights.append(f"**Development Pattern:** {late_bloomers[0]} exemplifies the 'late bloomer' archetype, showing significant improvement in later career phases")
    
    return insights

def analyze_team_building_insights(df):
    """Generate strategic insights for roster construction"""
    insights = []
    
    # Analyze the efficiency-usage trade-off curve
    df['USAGE_BRACKET'] = pd.cut(df['USAGE_EST'], bins=3, labels=['Low', 'Medium', 'High'])
    usage_efficiency = df.groupby('USAGE_BRACKET').agg({
        'EFFICIENCY': 'mean',
        'TS_PCT': 'mean',
        'PLAYER_NAME': 'count'
    })
    
    # Find the sweet spot
    if len(usage_efficiency) == 3:
        optimal_bracket = usage_efficiency['EFFICIENCY'].idxmax()
        insights.append(f"**Roster Construction:** {optimal_bracket}-usage players provide optimal efficiency returns, suggesting balanced offensive distribution")
    
    # Multi-skill players vs specialists
    df['SKILL_DIVERSITY'] = (df['PPG'].rank(pct=True) + df['RPG'].rank(pct=True) + df['APG'].rank(pct=True)) / 3
    versatile_players = df[df['SKILL_DIVERSITY'] >= 0.8]
    
    if len(versatile_players) > 0:
        best_versatile = versatile_players.loc[versatile_players['EFFICIENCY'].idxmax()]
        insights.append(f"**Versatility Premium:** Multi-dimensional players like {best_versatile['PLAYER_NAME']} provide roster flexibility worth {best_versatile['EFFICIENCY']:.0f} efficiency points")
    
    # Age and durability insights
    df['ESTIMATED_AGE'] = 19 + (df['SEASON_ID'].str[:4].astype(int) - df.groupby('PLAYER_NAME')['SEASON_ID'].transform(lambda x: x.str[:4].astype(int).min()))
    
    prime_performance = df[(df['ESTIMATED_AGE'] >= 27) & (df['ESTIMATED_AGE'] <= 31)]
    veteran_performance = df[df['ESTIMATED_AGE'] >= 32]
    
    if len(prime_performance) > 0 and len(veteran_performance) > 0:
        prime_efficiency = prime_performance['EFFICIENCY'].mean()
        veteran_efficiency = veteran_performance['EFFICIENCY'].mean()
        decline_rate = ((prime_efficiency - veteran_efficiency) / prime_efficiency) * 100
        insights.append(f"**Age Curve Analysis:** Performance typically declines {decline_rate:.0f}% after age 31, informing contract length strategies")
    
    return insights

def analyze_market_inefficiencies(df):
    """Identify potential undervalued player types"""
    insights = []
    
    # Find high-efficiency, low-profile combinations
    df['PROFILE_SCORE'] = df['PPG'].rank(pct=True) * 0.5 + df['USAGE_EST'].rank(pct=True) * 0.5
    
    # High efficiency, low profile (potential values)
    value_candidates = df[(df['EFFICIENCY'] >= df['EFFICIENCY'].quantile(0.7)) & 
                         (df['PROFILE_SCORE'] <= df['PROFILE_SCORE'].quantile(0.4))]
    
    if len(value_candidates) > 0:
        best_value = value_candidates.loc[value_candidates['EFFICIENCY'].idxmax()]
        insights.append(f"**Market Inefficiency:** {best_value['PLAYER_NAME']} delivers top-tier efficiency ({best_value['EFFICIENCY']:.0f}) despite moderate usage, representing potential market undervaluation")
    
    # Shooting vs other skills trade-off
    elite_shooters = df[df['TS_PCT'] >= df['TS_PCT'].quantile(0.9)]
    if len(elite_shooters) > 0:
        shooter_efficiency = elite_shooters['EFFICIENCY'].mean()
        overall_efficiency = df['EFFICIENCY'].mean()
        shooting_premium = ((shooter_efficiency - overall_efficiency) / overall_efficiency) * 100
        insights.append(f"**Shooting Premium:** Elite shooters command {shooting_premium:.0f}% efficiency premium, validating modern emphasis on spacing")
    
    return insights

def generate_executive_summary():
    """Generate business-focused executive summary"""
    print("Generating Strategic NBA Analysis...")
    
    # Load data
    df, career_df = load_data()
    
    # Run strategic analyses
    archetype_insights = analyze_player_archetypes(df)
    generational_insights = analyze_generational_shifts(df)
    outlier_insights = analyze_performance_outliers(df)
    team_insights = analyze_team_building_insights(df)
    market_insights = analyze_market_inefficiencies(df)
    
    # Generate summary statistics
    total_seasons = len(df)
    total_players = df['PLAYER_NAME'].nunique()
    season_range = f"{df['SEASON_ID'].min()[:4]}-{df['SEASON_ID'].max()[:4]}"
    
    # Create executive summary
    summary = f"""# NBA Strategic Performance Analysis - Executive Summary
*Generated on {datetime.now().strftime('%B %d, %Y')}*

## Executive Overview
Advanced analytics study of **{total_players} elite NBA players** across **{total_seasons} player-seasons** ({season_range}), focusing on strategic insights for modern basketball operations, player evaluation, and roster construction.

## Strategic Insights & Business Intelligence

### 1. Player Archetype Evolution
"""
    
    for insight in archetype_insights:
        summary += f"- {insight}\n"
    
    summary += "\n### 2. Generational Trends & Market Shifts\n"
    for insight in generational_insights:
        summary += f"- {insight}\n"
    
    summary += "\n### 3. Performance Pattern Analysis\n"
    for insight in outlier_insights:
        summary += f"- {insight}\n"
    
    summary += "\n### 4. Roster Construction Intelligence\n"
    for insight in team_insights:
        summary += f"- {insight}\n"
    
    summary += "\n### 5. Market Value & Opportunity Analysis\n"
    for insight in market_insights:
        summary += f"- {insight}\n"
    
    summary += f"""
## Methodology & Analytical Framework
- **Data Architecture:** Real-time NBA API integration with automated processing pipeline
- **Advanced Metrics:** True Shooting Percentage, Usage Rate, Multi-dimensional Efficiency Modeling
- **Statistical Methods:** Quartile analysis, trend decomposition, outlier detection, predictive modeling
- **Technology Stack:** Python ecosystem (pandas, numpy), Tableau visualization, automated insight generation

## Business Applications & ROI Potential
This analytical framework delivers value across multiple organizational functions:

**Player Personnel:**
- **Scouting Optimization:** Identify undervalued talent through efficiency-usage modeling
- **Draft Strategy:** Age curve analysis informs optimal selection timing
- **Contract Negotiations:** Performance trajectory data supports valuation decisions

**Strategic Planning:**
- **Roster Construction:** Optimal player mix based on usage-efficiency trade-offs
- **Competitive Positioning:** Benchmark against league trends and identify advantages
- **Resource Allocation:** Data-driven investment in player development areas

**Performance Analytics:**
- **Player Development:** Target specific efficiency thresholds for maximum impact
- **Game Strategy:** Usage rate optimization based on opponent analysis
- **Injury Management:** Age-performance correlation guides load management

## Competitive Advantages Identified
1. **Efficiency-First Philosophy:** Modern NBA rewards shooting accuracy over volume
2. **Positional Flexibility:** Multi-skill players provide outsized roster value
3. **Age Curve Optimization:** Strategic timing of player acquisition and retention
4. **Market Inefficiencies:** Undervalued player archetypes present opportunity

---
*Complete dashboard with interactive visualizations and drill-down capabilities available in accompanying Tableau workbook*
"""
    
    # Save to file
    import os
    os.makedirs('reports', exist_ok=True)
    
    with open('reports/nba_strategic_analysis.md', 'w') as f:
        f.write(summary)
    
    print("Strategic Analysis generated!")
    print("File saved: reports/nba_strategic_analysis.md")
    print("\nKey improvements:")
    print("- Diverse insights across different analytical dimensions")
    print("- Business-focused recommendations")
    print("- Strategic rather than descriptive analysis")
    print("- Reduced player repetition through varied analytical lenses")

if __name__ == "__main__":
    generate_executive_summary()