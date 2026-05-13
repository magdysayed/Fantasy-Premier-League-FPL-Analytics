import pandas as pd
import requests

def get_fpl_data():
    # الرابط الرسمي لبيانات الفانتازي
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    
    # الـ Headers دي هي "السر" اللي بيخلي الموقع يفتكرك متصفح حقيقي مش Bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Connection': 'keep-alive'
    }

    print("📡 Requesting data from FPL API...")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status() # هيطلع Error لو الموقع عمل Block
        data = response.json()

        # تحويل البيانات لـ DataFrames
        elements_df = pd.DataFrame(data['elements'])
        teams_df = pd.DataFrame(data['teams'])
        
        # تجهيز البيانات (نفس الأعمدة اللي إنت مهتم بيها)
        fpl_df = elements_df[['first_name', 'second_name', 'team', 'now_cost', 'selected_by_percent', 
                             'total_points', 'element_type', 'threat', 'creativity', 'influence', 'saves']].copy()
        
        # ربط اسم الفريق بدل الرقم
        teams_map = teams_df.set_index('id')['name'].to_dict()
        fpl_df['team_name'] = fpl_df['team'].map(teams_map)
        fpl_df['player'] = fpl_df['first_name'] + ' ' + fpl_df['second_name']
        fpl_df['now_cost'] = fpl_df['now_cost'] / 10
        
        # تحويل القيم لبيانات رقمية
        for col in ['threat', 'creativity', 'influence', 'saves']:
            fpl_df[col] = pd.to_numeric(fpl_df[col], errors='coerce').fillna(0)

        # حفظ الملف اللي الـ GitHub Action مستنيه
        fpl_df.to_csv("clean_fpl_analysis.csv", index=False)
        print(f"✅ Success! Data saved for {len(fpl_df)} players.")

    except Exception as e:
        print(f"❌ Request failed: {e}")
        # بنعمل exit(1) هنا عشان لو فشل الـ Action يديك علامة حمراء فتعرف
        exit(1)

if __name__ == "__main__":
    get_fpl_data()
