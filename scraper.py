import soccerdata as sd
import pandas as pd
import requests

def get_fpl_meta_data():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)
    data = response.json()
    elements_df = pd.DataFrame(data['elements'])
    teams_df = pd.DataFrame(data['teams'])
    
    fpl_df = elements_df[['first_name','second_name' , 'team', 'now_cost', 'selected_by_percent', 
                        'total_points', 'element_type', 'threat', 'creativity', 'influence']].copy()
    
    teams_map = teams_df.set_index('id')['name'].to_dict()
    fpl_df['team_name'] = fpl_df['team'].map(teams_map)
    fpl_df['full_name'] = fpl_df['first_name'] + ' ' + fpl_df['second_name']
    
    return fpl_df

def run_scraper():
    print("🚀 Starting Data Scraping (2025/2026 Season)...")
    
    fbref = sd.FBref(leagues='ENG-Premier League', seasons='2526')
    
    print("📊 Fetching Standard Stats (Gls, Ast, xG)...")
    player_stats = fbref.read_player_season_stats(stat_type='standard')
    player_stats.columns = [f"{col[0]}_{col[1]}" if "Unnamed" not in col[0] else col[1] for col in player_stats.columns]
    player_stats = player_stats.reset_index()

    print(" Fetching Keeper Stats (Saves)...")
    keeper_stats = fbref.read_player_season_stats(stat_type='keeper')
    keeper_stats.columns = [f"{col[0]}_{col[1]}" if "Unnamed" not in col[0] else col[1] for col in keeper_stats.columns]
    
    keeper_stats = keeper_stats.reset_index()[['player', 'Performance_Saves']]
    keeper_stats = keeper_stats.drop_duplicates(subset=['player'])

    print("🔗 Merging FBref Data Sources...")
    combined_fbref = pd.merge(player_stats, keeper_stats, on='player', how='left')
    
    print("📡 Loading FPL API Metadata...")
    fpl_meta = get_fpl_meta_data()

    print("🧬 Final Merging...")
    final_df = pd.merge(
        combined_fbref, 
        fpl_meta, 
        left_on='player', 
        right_on='full_name', 
        how='inner')

    for col in ['threat', 'creativity', 'influence']:
        final_df[col] = pd.to_numeric(final_df[col], errors='coerce').fillna(0)

    final_df.to_csv("clean_fpl_analysis.csv", index=False)
    print(f"✅ Done! Saved {len(final_df)} players with Advanced Metrics & Saves.")

if __name__ == "__main__":
    run_scraper()