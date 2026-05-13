import pandas as pd
import requests

def run_scraper():
    print("🚀 Starting Data Update via FPL API (Safe Mode)...")
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    
    # الـ Headers دي هي اللي هتخلي الـ Request ينجح وتتخطى أي Block
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()

        elements_df = pd.DataFrame(data['elements'])
        teams_df = pd.DataFrame(data['teams'])
        
        # تجميع البيانات اللي إنت محتاجها
        fpl_df = elements_df[['first_name', 'second_name', 'team', 'now_cost', 'selected_by_percent', 
                             'total_points', 'element_type', 'threat', 'creativity', 'influence', 'saves']].copy()
        
        teams_map = teams_df.set_index('id')['name'].to_dict()
        fpl_df['team_name'] = fpl_df['team'].map(teams_map)
        fpl_df['player'] = fpl_df['first_name'] + ' ' + fpl_df['second_name']
        fpl_df['now_cost'] = fpl_df['now_cost'] / 10
        
        for col in ['threat', 'creativity', 'influence', 'saves']:
            fpl_df[col] = pd.to_numeric(fpl_df[col], errors='coerce').fillna(0)

        # حفظ الملف
        fpl_df.to_csv("clean_fpl_analysis.csv", index=False)
        print(f"✅ Success! Data saved for {len(fpl_df)} players.")

    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    run_scraper()
