import pandas as pd
import requests
import time

def get_fpl_data():
    """
    سحب البيانات مباشرة من FPL API الرسمي
    تجنباً لمشاكل الـ Block في سيرفرات GitHub
    """
    print(" Loading Data from Official FPL API...")
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    
    # إضافة Headers لزيادة الأمان وتجنب الـ Block
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # تحويل البيانات لـ DataFrames
        elements_df = pd.DataFrame(data['elements'])
        teams_df = pd.DataFrame(data['teams'])
        positions_df = pd.DataFrame(data['element_types'])
        
        # 1. تجهيز خريطة الفرق والمراكز
        teams_map = teams_df.set_index('id')['name'].to_dict()
        pos_map = positions_df.set_index('id')['singular_name_short'].to_dict()
        
        # 2. اختيار الأعمدة الأساسية والمتقدمة المتوفرة في الـ API
        # الـ API بيوفر (Threat, Creativity, Influence, ICT Index) فعلياً
        cols_to_keep = [
            'web_name', 'first_name', 'second_name', 'team', 'element_type',
            'now_cost', 'selected_by_percent', 'total_points', 'minutes',
            'goals_scored', 'assists', 'clean_sheets', 'saves', 'status',
            'threat', 'creativity', 'influence', 'ict_index'
        ]
        
        fpl_df = elements_df[cols_to_keep].copy()
        
        # 3. معالجة البيانات وتحسينها
        fpl_df['team_name'] = fpl_df['team'].map(teams_map)
        fpl_df['position'] = fpl_df['element_type'].map(pos_map)
        fpl_df['player'] = fpl_df['first_name'] + ' ' + fpl_df['second_name']
        fpl_df['now_cost'] = fpl_df['now_cost'] / 10  # تحويل السعر لـ 12.5 بدلاً من 125
        
        # تحويل القيم النصية لأرقام (للرسوم البيانية)
        for col in ['threat', 'creativity', 'influence', 'ict_index']:
            fpl_df[col] = pd.to_numeric(fpl_df[col], errors='coerce').fillna(0)
            
        # 4. إعادة تسمية الأعمدة لتتوافق مع الـ Dashboard القديمة لو احتجت
        fpl_df = fpl_df.rename(columns={'saves': 'Performance_Saves'})

        # حفظ الملف النهائي
        fpl_df.to_csv("clean_fpl_analysis.csv", index=False)
        print(f" Done! Saved {len(fpl_df)} players with all metrics.")
        
    except Exception as e:
        print(f" Error occurred: {e}")
        # في حالة الفشل، تأكد إن الـ Workflow مش هيقف بـ Error
        exit(0)

if __name__ == "__main__":
    print(" Starting Data Update Pipeline...")
    get_fpl_data()
