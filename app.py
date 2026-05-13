import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Step 1: Basic Page Setup
st.set_page_config(page_title="FPL Analytics Dashboard", layout="wide")
st.title("FPL Performance Analytics - Professional Dashboard")

# Step 2: Load and Clean Data
try:
    df = pd.read_csv("clean_fpl_analysis.csv")
    
    # Remove rows with missing team names or invalid costs
    df = df.dropna(subset=['team_name'])
    df = df[df['now_cost'] > 0]

    # Convert FPL cost to standard millions format
    df['price'] = df['now_cost'] / 10

    # Map position IDs to readable labels
    pos_mapping = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}
    df['position'] = df['element_type'].map(pos_mapping)

    # --------------------------------------------------
    # Sidebar Filters
    # --------------------------------------------------
    st.sidebar.header("Data Filters")

    # Player Search and Highlight Filter
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

    # Team Multiselect
    all_teams = sorted(df['team_name'].unique())
    selected_team = st.sidebar.multiselect(
        "Select Teams", 
        options=all_teams, 
        default=all_teams
    )

    # Position Multiselect
    all_positions = df['position'].unique()
    selected_position = st.sidebar.multiselect(
        "Select Positions", 
        options=all_positions, 
        default=all_positions
    )

    # Price Range Slider
    selected_price = st.sidebar.slider(
        "Select Price Range (£m)",
        min_value=float(df['price'].min()),
        max_value=float(df['price'].max()),
        value=(float(df['price'].min()), float(df['price'].max()))
    )

    # Apply all filters to the dataframe
    filtered_df = df[
        (df['team_name'].isin(selected_team)) & 
        (df['price'] >= selected_price[0]) & 
        (df['price'] <= selected_price[1]) &
        (df['position'].isin(selected_position))
    ].copy()

    # --------------------------------------------------
    # Row 1: High-Level Performance Metrics
    # --------------------------------------------------


    
        # Scatter Plot: Price vs Total Points
    fig1 = go.Figure(data=go.Scatter(
            x=filtered_df['price'], 
            y=filtered_df['total_points'],
            text=filtered_df['player'],
            mode='markers',
            marker=dict(color='rgba(255, 0, 0, .8)', size=10)
        ))
    fig1.update_layout(
            title="Price vs Total Points Efficiency",
            xaxis_title="Price (m)",
            yaxis_title="Total Points",
            template="plotly_white",
            hovermode="closest"
        )
    st.plotly_chart(fig1, use_container_width=True)

    
        # Bar Chart: Top 10 Players by Points
    top_points = filtered_df.groupby('player')['total_points'].max().reset_index()
    top_points = top_points.sort_values(by='total_points', ascending=False).head(10)
        
    fig2 = go.Figure(data=go.Bar(
            x=top_points['player'], 
            y=top_points['total_points'],
            marker_color='rgb(255, 0, 0, .8)'
        ))
    fig2.update_layout(
            title="Elite Performers - Top 10 Total Points",
            xaxis_title="Player Name",
            yaxis_title="Total Points",
            template="plotly_white",
        )
    st.plotly_chart(fig2, use_container_width=True)

    # --------------------------------------------------
    # Row 2: Value and Threat Analysis
    # --------------------------------------------------
    st.divider()
    col3, col4 = st.columns(2)

    with col3:
        # Bar Chart: Points per Million (Efficiency)
        filtered_df['points_per_million'] = filtered_df['total_points'] / filtered_df['price']
        top_value = filtered_df.groupby('player')['points_per_million'].max().reset_index()
        top_value = top_value.sort_values(by='points_per_million', ascending=False).head(10)

        fig3 = go.Figure(data=go.Bar(
            x=top_value['player'], 
            y=top_value['points_per_million'],
            marker_color='rgba(255, 0, 0, .8)'
        ))
        fig3.update_layout(
            title="Value for Money - Points per Million",
            xaxis_title="Player Name",
            yaxis_title="Points per £1m",
            template="plotly_white",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # Bar Chart: Top 10 Threat Index (Scoring Potential)
        top_threat_data = filtered_df.groupby('player')['threat'].max().reset_index()
        top_threat_data = top_threat_data.sort_values(by='threat', ascending=False).head(10)

        fig_threat = go.Figure(data=go.Bar(
            x=top_threat_data['player'],
            y=top_threat_data['threat'],
            marker_color='crimson'
        ))
        fig_threat.update_layout(
            title="Top 10 Offensive Threat (Expected Impact)",
            xaxis_title="Player Name",
            yaxis_title="Threat Index",
            template="plotly_white",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_threat, use_container_width=True)

    # --------------------------------------------------
    # Row 3: Advanced Role Distribution (Scatter)
    # --------------------------------------------------
    st.divider()
    st.subheader("Role Profiling: Creativity vs Threat")
    
    fig_scatter_advanced = go.Figure(data=go.Scatter(
        x=filtered_df['creativity'],
        y=filtered_df['threat'],
        mode='markers',
        text=filtered_df['player'],
        marker=dict(
            size=12,
            color=filtered_df['total_points'],   
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Total Points")
        )
    ))
    fig_scatter_advanced.update_layout(
        xaxis_title="Creativity (Chances Created)",
        yaxis_title="Threat (Goal Scoring Potential)",
        template="plotly_white",
        height=600
    )
    st.plotly_chart(fig_scatter_advanced, use_container_width=True)

    # --------------------------------------------------
    # Row 4: Goalkeepers Analysis Section
    # --------------------------------------------------
    st.divider()
    st.header("Goalkeepers Specialized Analysis")
    
    gk_df = filtered_df[filtered_df['position'] == 'GK']

    if not gk_df.empty:
        col5, col6 = st.columns(2)
        
        with col5:
            top_gk_points = gk_df.sort_values(by='total_points', ascending=False).head(10)
            fig_gk_points = go.Figure(data=go.Bar(
                x=top_gk_points['player'],
                y=top_gk_points['total_points'],
                marker_color='teal'
            ))
            fig_gk_points.update_layout(title="Top 10 GKs by Total Points", xaxis_tickangle=-45)
            st.plotly_chart(fig_gk_points, use_container_width=True)

        with col6:
            # حل مشكلة الـ Saves: البحث عن أي عمود يحتوي على كلمة saves بغض النظر عن حالة الأحرف
            save_column = None
            possible_save_names = [col for col in gk_df.columns if 'save' in col.lower()]
            
            if possible_save_names:
                save_column = possible_save_names[0] # اختيار أول عمود مطابق
                top_gk_saves = gk_df.sort_values(by=save_column, ascending=False).head(10)
                fig_gk_saves = go.Figure(data=go.Bar(
                    x=top_gk_saves['player'],
                    y=top_gk_saves[save_column],
                    marker_color='goldenrod'
                ))
                fig_gk_saves.update_layout(title=f"Top 10 Shot Stoppers ({save_column})", xaxis_tickangle=-45)
                st.plotly_chart(fig_gk_saves, use_container_width=True)
            else:
                st.warning("⚠️ لم يتم العثور على عمود التصديات (Saves) في ملف البيانات المرفوع.")
                # طباعة أسماء الأعمدة المتاحة لمساعدتك في التأكد (تظهر لك فقط أثناء التطوير)
                # st.write("Columns found:", list(gk_df.columns)) 
    else:
        st.info("No Goalkeepers match current filter criteria.")

    # --------------------------------------------------
    # Defenders (DEF) Specialized Analysis
    # --------------------------------------------------
    st.divider()
    st.header(" Defenders Performance Analysis")

    def_df = filtered_df[filtered_df['position'] == 'DEF']

    if not def_df.empty:
        col_def1, col_def2 = st.columns(2)

        with col_def1:
        #best defenders by total points
            def_points = def_df.groupby('player')['total_points'].max().reset_index()
            top_def_points = def_points.sort_values(by='total_points', ascending=False).head(10)
            fig_def_points = go.Figure(data=go.Bar(
                x=top_def_points['player'], 
                y=top_def_points['total_points'], 
                marker_color='royalblue'
            ))
            fig_def_points.update_layout(title="Top 10 Defenders by Total Points", template="plotly_white")
            st.plotly_chart(fig_def_points, use_container_width=True)

        with col_def2:
        #best defenders by creativity (assist potential)
            top_def_creativity = def_df.sort_values(by='creativity', ascending=False).head(10)
            fig_def_creativity = go.Figure(data=go.Bar(
                x=top_def_creativity['player'], 
                y=top_def_creativity['creativity'], 
                marker_color='mediumpurple'
            ))
            fig_def_creativity.update_layout(title="Most Creative Defenders (Assist Potential)", template="plotly_white")
            st.plotly_chart(fig_def_creativity, use_container_width=True)

        # Scatter Plot: Defenders Threat vs Total Points
        st.subheader("⚔️ Defensive vs Offensive Contribution")
        
        fig_def_threat = go.Figure(data=go.Scatter(
            x=def_df['threat'], 
            y=def_df['total_points'],
            text=def_df['player'],
            mode='markers',
            marker=dict(
                size=def_df['price']*2, # point size based on price for visual emphasis
                color=def_df['total_points'],
                colorscale='Viridis',
                showscale=True
            )
        ))
        fig_def_threat.update_layout(
            title="Defenders Threat (Offensive Potential) vs Total Points",
            xaxis_title="Threat Index",
            yaxis_title="Total Points",
            template="plotly_white"
        )
        st.plotly_chart(fig_def_threat, use_container_width=True)

    else:
        st.info("No Defenders match current filter criteria.")

    # --------------------------------------------------
    # Raw Data Export
    # --------------------------------------------------
    st.divider()
    st.subheader(f"Filtered Dataset View ({len(filtered_df)} players found)")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Critical System Error: {e}")
