from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.filters import apply_filters, render_sidebar_filters
from app.components.metrics import render_kpi_grid
from app.utils.data_loader import load_data
from app.utils.transformations import calculate_summary_metrics


st.set_page_config(
    page_title="FMCG Promo ROI Analytics",
    page_icon="📊",
    layout="wide",
)


st.title("FMCG Promotional ROI Analytics Web App")
st.caption(
    "Commercial analytics + data science web app for promotional ROI, "
    "uplift, margin impact and cannibalisation risk analysis."
)

st.info(
    "This Streamlit app is Project 2.0 of the FMCG Promotional ROI case study. "
    "The Power BI version demonstrates dashboarding; this version productises the analysis "
    "into an interactive Python web app."
)

try:
    df = load_data()
except Exception as exc:
    st.error(f"Failed to load dataset: {exc}")
    st.stop()

filters = render_sidebar_filters(df)
filtered_df = apply_filters(df, filters)

if filtered_df.empty:
    st.warning("No rows match the selected filters. Please adjust the sidebar filters.")
    st.stop()

metrics = calculate_summary_metrics(filtered_df)

st.subheader("Filtered Executive Snapshot")
render_kpi_grid(metrics)

st.divider()

st.subheader("Business Question")

st.markdown(
    """
**Which promotions created profitable incremental growth, and which should be repeated, 
targeted, adjusted, or discontinued?**

This app keeps the commercial analytics logic from the Power BI case study and extends it 
with Python-based interactivity and data science demos.
"""
)

st.subheader("Available Pages")

st.markdown(
    """
1. **Executive Summary** — KPI cards, recommendation mix, promo ROI and campaign summary  
2. **Promo ROI by Campaign** — uplift vs ROI, top campaigns, and low-profit campaigns  
3. **Uplift vs Margin Impact** — discount depth, uplift response and margin pressure  
4. **Category / Region / Account Analysis** — category, region, account and product performance  
5. **Cannibalisation Risk** — category switching risk and high-risk campaign review  
6. **Data Science Lab** — regression and classification modelling demos  
7. **Data Explorer** — filtered raw data, downloads and metric definitions  
"""
)

st.warning(
    "Synthetic dataset caveat: all data is simulated for portfolio demonstration. "
    "Model outputs in later pages should be interpreted as data science demos, not production forecasts."
)