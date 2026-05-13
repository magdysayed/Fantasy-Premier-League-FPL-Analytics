import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Step 1: Basic Page Setup
st.set_page_config(page_title="FPL Analytics Dashboard", layout="wide")
st.title("⚽ FPL Performance Analytics")

# Define Professional Color Palette
COLORS = {
    'primary': '#1E3A8A',    # Navy Blue
    'secondary': '#3B82F6',  # Bright Blue
    'accent': '#64748B',     # Slate Gray
    'background': '#F8FAFC', # Off White
    'marker': '#0F172A'      # Dark Slate
}

# Step 2: Load and Clean Data
try:
    df = pd.read_csv("clean_fpl_analysis.csv")
    df = df.dropna(subset=['team_name'])
    
    # Standardize Price
    if df['now_cost'].max() > 100:
        df['price'] = df['now_cost'] / 10
    else:
        df['price'] = df['now_cost']

    # Map Positions
    if 'position' not in df.columns:
        pos_mapping = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}
        df['position'] = df['element_type'].map(pos_mapping)

    # --------------------------------------------------
    # Sidebar Filters
    # --------------------------------------------------
    st.sidebar.header("Navigation & Filters")
    
    all_teams = sorted(df['team_name'].unique())
    selected_team = st.sidebar.multiselect("Teams", options=all_teams, default=all_teams)

    all_positions = df['position'].unique()
    selected_position = st.sidebar.multiselect("Positions", options=all_positions, default=all_positions)

    selected_price = st.sidebar.slider(
        "Price Range (£m)",
        min_value=float(df['price'].min()),
        max_value=float(df['price'].max()),
        value=(float(df['price'].min()), float(df['price'].max()))
    )

    filtered_df = df[
        (df['team_name'].isin(selected_team)) & 
        (df['price'] >= selected_price[0]) & 
        (df['price'] <= selected_price[1]) &
        (df['position'].isin(selected_position))
    ].copy()

    # --------------------------------------------------
    # Row 1: The Main Scatter Plot (Single Row)
    # --------------------------------------------------
    st.subheader("🎯 Value Discovery: Price vs Total Points")
    fig_scatter = px.scatter(
        filtered_df, x='price', y='total_points',
        text='player', color='position',
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], '#94A3B8'],
        hover_data=['team_name', 'selected_by_percent']
    )
    fig_scatter.update_traces(marker=dict(size=12, opacity=0.7, line=dict(width=1, color='White')))
    fig_scatter.update_layout(
        plot_bgcolor='white',
        xaxis=dict(title="Price (£m)", showgrid=True, gridcolor='#E2E8F0'),
        yaxis=dict(title="Total Points", showgrid=True, gridcolor='#E2E8F0'),
        height=600,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # --------------------------------------------------
    # Row 2: Performance & The "Super" ROI Chart
    # --------------------------------------------------
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 Efficiency: Points per Million")
        filtered_df['ppm'] = filtered_df['total_points'] / filtered_df['price']
        top_val = filtered_df.sort_values(by='ppm', ascending=False).head(10)
        
        fig_val = px.bar(top_val, x='ppm', y='player', orientation='h',
                         color_discrete_sequence=[COLORS['primary']])
        fig_val.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white')
        st.plotly_chart(fig_val, use_container_width=True)

    with col2:
        st.subheader("💎 The ROI Gem Index")
        # معادلة خارقة: النقط لكل مليون مقسومة على نسبة الملكية 
        # الهدف: إيجاد لاعبين نقاطهم عالية وسعرهم رخيص ومش عند حد (Differential)
        filtered_df['roi_gem'] = (filtered_df['total_points'] / filtered_df['price']) / (filtered_df['selected_by_percent'] + 1)
        top_gem = filtered_df.sort_values(by='roi_gem', ascending=False).head(10)
        
        fig_gem = px.bar(top_gem, x='roi_gem', y='player', orientation='h',
                         color_discrete_sequence=[COLORS['secondary']])
        fig_gem.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white')
        st.plotly_chart(fig_gem, use_container_width=True)

    # --------------------------------------------------
    # Row 3: Advanced Stats (Threat & Saves)
    # --------------------------------------------------
    st.divider()
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🔥 Offensive Threat Index")
        top_threat = filtered_df.sort_values(by='threat', ascending=False).head(10)
        fig_threat = px.bar(top_threat, x='player', y='threat', 
                            color_discrete_sequence=[COLORS['accent']])
        fig_threat.update_layout(plot_bgcolor='white')
        st.plotly_chart(fig_threat, use_container_width=True)

    with col4:
        st.subheader("🧤 Goalkeeper Shot-Stopping")
        gk_df = filtered_df[filtered_df['position'] == 'GK']
        save_col = next((c for c in ['Performance_Saves', 'saves', 'Saves'] if c in gk_df.columns), None)
        
        if save_col and not gk_df.empty:
            top_gk = gk_df.sort_values(by=save_col, ascending=False).head(10)
            fig_gk = px.bar(top_gk, x='player', y=save_col, 
                            color_discrete_sequence=[COLORS['marker']])
            fig_gk.update_layout(plot_bgcolor='white')
            st.plotly_chart(fig_gk, use_container_width=True)
        else:
            st.info("Select Goalkeepers to see shot-stopping data.")

    # --------------------------------------------------
    # Row 4: Raw Data View
    # --------------------------------------------------
    with st.expander("📂 View Full Filtered Dataset"):
        st.dataframe(filtered_df.sort_values(by='total_points', ascending=False), use_container_width=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
