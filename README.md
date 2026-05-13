# ⚽ FPL Analytics Hub: End-to-End Automated Pipeline & Dashboard

A professional data engineering and analytics suite designed to provide deep insights into Fantasy Premier League (FPL) performance. This project integrates live data scraping, advanced cleaning, and interactive visualization with zero-maintenance automation.

## 🚀 Project Overview

This project transforms raw FPL data into actionable insights. It automates the extraction of player statistics and visualizes them to help managers identify "Value for Money" assets and tactical trends using a modern tech stack.

## 📋 Full Development Journey

### Phase 1: Data Engineering & Scraper Logic

- **The Scraper:** Built `scraper.py` using `soccerdata` and direct API integrations to fetch live statistics.
- **Data Cleaning Pipeline:**
  - Handled missing team associations and null performance metrics.
  - Standardized player costs from internal API integers (e.g., 140) to standard millions (14.0m).
- **Challenge Faced:** Initial scraping attempts had data type mismatches.
- **The Fix:** Implemented a pre-processing layer in `pandas` to ensure all numerical columns are float-ready for visualization.

### Phase 2: Interactive Analytics (The Dashboard)

Developed an interactive UI using `Streamlit` with the following core features:

- **Simultaneous Filtering:** Users can filter by multiple teams, positions, and precise price ranges (£3.7m - £14.7m).
- **Player Deep-Dive:** A specialized search feature (e.g., for Mohamed Salah) that shows real-time "Quick Stats" including Ownership % and Points.
- **Efficiency Metrics:** Created the "Points per Million" chart to find budget-friendly "Gems."

### Phase 3: Advanced Tactical Visualization

- **Creativity vs Threat:** A 2D scatter plot profiling players based on their offensive roles.
- **Goalkeeper Analysis:** A dedicated section comparing "Total Points" against "Shot Stopping (Total Saves)" to identify high-floor GKs.
- **Data Transparency:** Included a "Filtered Dataset View" to allow users to inspect the raw numbers (426+ players).

### Phase 4: CI/CD & Automation

- **The Zero-Maintenance Setup:** Integrated **GitHub Actions** via `.github/workflows/update.yml`.
- **The Schedule:** The system automatically runs at **4:00 AM Riyadh Time** (01:00 UTC) every day.
- **Workflow:** Virtual environment setup -> Dependency installation -> Scraper execution -> Auto-commit of `clean_fpl_analysis.csv`.

## 🛠️ Tech Stack

- **Languages:** Python (Pandas, NumPy)
- **Visualization:** Plotly (Interactive Charts)
- **UI/UX:** Streamlit
- **DevOps:** GitHub Actions (Automation)
- **Data Source:** Official FPL API & SoccerData

## 📊 Dashboard Preview

### 1. Global Performance & Efficiency

Analysis of the top 10 elite performers and price vs points distribution.
![Efficiency Overview](Images/Screenshot%202026-05-13%20032506.png)

### 2. Market Value & Threat Index

Identifying the most efficient "Value for Money" players and high-impact offensive threats.
![Value Analysis](Images/Screenshot%202026-05-13%20032555.png)
![Raw Data](Images/Screenshot%202026-05-13%20032632.png)

### 4. Goalkeepers Specialized Analysis

Comparing the league's best shot-stoppers and point-scoring GKs.
![Role Profiling](Images/Screenshot%202026-05-13%20032705.png)


### 5. Advanced Search & Filtering

Detailed search for specific players and multi-select filters for teams and positions.
![Player Search](Images/Screenshot%202026-05-13%20032751.png)
![Filters](Images/Screenshot%202026-05-13%20032817.png)


Developed by Magdy ElSayed Fathy ElSayed
Software Engineer & Data Analyst
