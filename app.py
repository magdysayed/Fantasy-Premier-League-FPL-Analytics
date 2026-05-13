import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Step 1: Basic Page Setup
st.set_page_config(page_title="FPL Analytics Dashboard", layout="wide")
st.title("FPL Performance Analytics - Professional Dashboard")

# Step 2: Load and Clean Data
try:
    df = pd.read_csv("clean_fpl_analysis.csv")
    
    # تنظيف البيانات الأساسية
    df = df.dropna(subset=['team_name'])
    
    # التأكد من أن السعر معالج بشكل صحيح (لو السكرابر بعته مقسوم جاهز أو لأ)
    if df['now_cost'].max() > 100:
        df['price'] = df['now_cost'] / 10
    else:
        df['price'] = df['now_cost']

    # تحويل أرقام المراكز لأسماء مفهومة (لو مش موجودة جاهزة من السكرابر)
    if 'position' not in df.columns:
        pos_mapping = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}
        df['position'] = df['element_type'].map(pos_mapping)

    # --------------------------------------------------
    # Sidebar Filters
    # --------------------------------------------------
    st.sidebar.header("Data Filters")

    # بحث عن لاعب محدد
    search_player = st.sidebar.selectbox(
        "Highlight a Specific Player", 
        options=["None"] + sorted(list(df['player'].unique()))
    )

    if search_player != "None":
        player_stats = df[df['player'] == search_player].iloc[0]
        st.sidebar.info(f"""
        **{search_player} Quick Stats:**
        - Team: {player_stats['team_name']}
        - Points: {player_stats['total_points']}
        - Price: £{player_stats['price']}m
        - Selected By: {player_stats['selected_by_percent']}%
        """)

    # فلتر الفرق
    all_teams = sorted(df['team_name'].unique())
    selected_team = st.sidebar.multiselect("Select Teams", options=all_teams, default=all_teams)

    # فلتر المراكز
    all_positions = df['position'].unique()
    selected_position = st.sidebar.multiselect("Select Positions", options=all_positions, default=all_positions)

    # فلتر السعر
    selected_price = st.sidebar.slider(
        "Select Price Range (£m)",
        min_value=float(df['price'].min()),
        max_value=float(df['price'].max()),
        value=(float(df['price'].min()), float(df['price'].max()))
    )

    # تطبيق الفلاتر
    filtered_df = df[
        (df['team_name'].isin(selected_team)) & 
        (df['price'] >= selected_price[0]) & 
        (df['price'] <= selected_price[1]) &
        (df['position'].isin(selected_position))
    ].copy()

    # --------------------------------------------------
    # Charts Section
    # --------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        fig1 = go.Figure(data=go.Scatter(
            x=filtered_df['price'], 
            y=filtered_df['total_points'],
            text=filtered_df['player'],
            mode='markers',
            marker=dict(color='crimson', size=10)
        ))
        fig1.update_layout(title="Price vs Total Points Efficiency", xaxis_title="Price (m)", yaxis_title="Total Points", template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        top_points = filtered_df.sort_values(by='total_points', ascending=False).head(10)
        fig2 = go.Figure(data=go.Bar(x=top_points['player'], y=top_points['total_points'], marker_color='darkred'))
        fig2.update_layout(title="Elite Performers - Top 10 Total Points", template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    col3, col4 = st.columns(2)

    with col3:
        filtered_df['ppm'] = filtered_df['total_points'] / filtered_df['price']
        top_val = filtered_df.sort_values(by='ppm', ascending=False).head(10)
        fig3 = go.Figure(data=go.Bar(x=top_val['player'], y=top_val['ppm'], marker_color='rgba(255, 0, 0, .8)'))
        fig3.update_layout(title="Value for Money - Points per Million", template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        top_threat = filtered_df.sort_values(by='threat', ascending=False).head(10)
        fig_threat = go.Figure(data=go.Bar(x=top_threat['player'], y=top_threat['threat'], marker_color='orange'))
        fig_threat.update_layout(title="Top 10 Offensive Threat Index", template="plotly_white")
        st.plotly_chart(fig_threat, use_container_width=True)

    # --------------------------------------------------
    # Goalkeepers specialized Analysis (التعديل المطلوب هنا)
    # --------------------------------------------------
    st.divider()
    st.header("Goalkeepers Specialized Analysis")
    
    gk_df = filtered_df[filtered_df['position'] == 'GK']

    if not gk_df.empty:
        col5, col6 = st.columns(2)
        
        with col5:
            top_gk_points = gk_df.sort_values(by='total_points', ascending=False).head(10)
            fig_gk_points = go.Figure(data=go.Bar(x=top_gk_points['player'], y=top_gk_points['total_points'], marker_color='teal'))
            fig_gk_points.update_layout(title="Top 10 GKs by Total Points")
            st.plotly_chart(fig_gk_points, use_container_width=True)

        with col6:
            # الحل الجذري لمشكلة الـ Saves
            # بندور على أي عمود فيه كلمة Saves بغض النظر عن الاسم بالظبط
            save_col = None
            possible_cols = ['Performance_Saves', 'saves', 'Saves']
            for c in possible_cols:
                if c in gk_df.columns:
                    save_col = c
                    break
            
            if save_col:
                top_gk_saves = gk_df.sort_values(by=save_col, ascending=False).head(10)
                fig_gk_saves = go.Figure(data=go.Bar(x=top_gk_saves['player'], y=top_gk_saves[save_col], marker_color='goldenrod'))
                fig_gk_saves.update_layout(title=f"Top 10 Shot Stoppers (Total Saves)")
                st.plotly_chart(fig_gk_saves, use_container_width=True)
            else:
                st.warning("Save statistics column not found. Please check your data source.")
    else:
        st.info("No Goalkeepers match current filter criteria.")

    st.divider()
    st.subheader(f"Filtered Dataset View ({len(filtered_df)} players found)")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Critical System Error: {e}")
