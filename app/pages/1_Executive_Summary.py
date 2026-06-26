from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.filters import apply_filters, render_sidebar_filters
from app.components.metrics import render_kpi_grid
from app.utils.charts import (
    bar_event_count_by_recommendation,
    bar_profit_by_recommendation,
    bar_roi_by_promo_type,
)
from app.utils.data_loader import load_data
from app.utils.display import display_percent_columns
from app.utils.formatting import format_currency, format_percent
from app.utils.transformations import (
    aggregate_campaigns,
    calculate_summary_metrics,
    promo_type_summary,
    recommendation_summary,
)


st.set_page_config(
    page_title="Executive Summary | FMCG Promo ROI",
    page_icon="??",
    layout="wide",
)

st.title("Executive Summary")
st.caption(
    "Promotional uplift, ROI, margin impact, trade spend and commercial recommendations."
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
render_kpi_grid(metrics)

st.divider()

rec_summary = recommendation_summary(filtered_df)
type_summary = promo_type_summary(filtered_df)

left, right = st.columns(2)

with left:
    st.plotly_chart(
        bar_profit_by_recommendation(rec_summary),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        bar_roi_by_promo_type(type_summary),
        use_container_width=True,
    )

left, right = st.columns(2)

with left:
    st.plotly_chart(
        bar_event_count_by_recommendation(rec_summary),
        use_container_width=True,
    )

with right:
    st.subheader("Business Interpretation")

    positive_roi = format_percent(metrics["positive_roi_rate"])
    incremental_profit = format_currency(metrics["total_incremental_profit"])
    avg_uplift = format_percent(metrics["avg_uplift_pct"])
    median_roi = format_percent(metrics["median_promo_roi"])

    st.markdown(
        f"""
Under the current filters, **{positive_roi}** of promotional events generated positive ROI.  
The selected promotions delivered **{incremental_profit}** in incremental profit after promo cost, 
with an average uplift of **{avg_uplift}** and median promo ROI of **{median_roi}**.

A promotion should not be judged by volume uplift alone. The strongest campaigns are those that 
balance uplift, margin quality, promotional cost and cannibalisation risk.
"""
    )

    st.info(
        "Commercial takeaway: repeat strong ROI promotions, target region-specific winners, "
        "and adjust promotions where discount depth or promo cost erodes margin."
    )

st.divider()

st.subheader("Campaign Summary Table")

campaigns = aggregate_campaigns(filtered_df)

if campaigns.empty:
    st.info("No promotional campaign rows available for the selected filters.")
else:
    display_cols = [
        "Campaign_ID",
        "Product",
        "Category",
        "Region",
        "Account",
        "Promo_Type",
        "Uplift_Pct",
        "Promo_ROI",
        "Incremental_Profit",
        "Promo_Cost",
        "Recommendation",
    ]

    campaign_display = (
        campaigns[display_cols]
        .sort_values("Incremental_Profit", ascending=False)
        .head(20)
        .copy()
    )

    campaign_display = display_percent_columns(
        campaign_display,
        ["Uplift_Pct", "Promo_ROI"],
    )

    st.dataframe(
        campaign_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Uplift_Pct": st.column_config.NumberColumn(
                "Uplift %",
                format="%.1f%%",
            ),
            "Promo_ROI": st.column_config.NumberColumn(
                "Promo ROI",
                format="%.1f%%",
            ),
            "Incremental_Profit": st.column_config.NumberColumn(
                "Incremental Profit",
                format="$%.0f",
            ),
            "Promo_Cost": st.column_config.NumberColumn(
                "Promo Cost",
                format="$%.0f",
            ),
        },
    )

    csv = campaign_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download campaign summary CSV",
        data=csv,
        file_name="campaign_summary_filtered.csv",
        mime="text/csv",
    )

st.caption(
    "Synthetic data caveat: this dashboard uses simulated FMCG promotional data for portfolio demonstration."
)
