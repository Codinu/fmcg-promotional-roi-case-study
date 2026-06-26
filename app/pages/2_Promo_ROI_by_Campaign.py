from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.filters import apply_filters, render_sidebar_filters
from app.utils.charts import campaign_uplift_roi_scatter
from app.utils.data_loader import load_data
from app.utils.display import display_percent_columns
from app.utils.transformations import aggregate_campaigns


st.set_page_config(
    page_title="Promo ROI by Campaign | FMCG Promo ROI",
    page_icon="??",
    layout="wide",
)

st.title("Promo ROI by Campaign")
st.caption(
    "Campaign-level view of uplift, ROI, incremental profit and commercial action."
)

try:
    df = load_data()
except Exception as exc:
    st.error(f"Failed to load dataset: {exc}")
    st.stop()

filters = render_sidebar_filters(df)
filtered_df = apply_filters(df, filters)

campaigns = aggregate_campaigns(filtered_df)

if campaigns.empty:
    st.warning("No promotional campaigns match the selected filters.")
    st.stop()

left, right = st.columns([1.35, 1])

with left:
    st.plotly_chart(
        campaign_uplift_roi_scatter(campaigns),
        use_container_width=True,
    )

with right:
    st.subheader("Business Explanation")
    st.markdown(
        """
High uplift does not automatically mean a good promotion.

A strong promotion should generate **profitable incremental growth** after discounting, 
margin impact and promotional cost. Campaigns with high uplift but weak or negative ROI 
should be reviewed before being repeated.
"""
    )
    st.info(
        "Use this page to separate volume response from commercial return. "
        "Repeat strong ROI campaigns; adjust campaigns where discount depth or promo cost erodes profit."
    )

st.divider()

top_campaigns = (
    campaigns[campaigns["Recommendation"].isin(["Repeat", "Targeted repeat"])]
    .sort_values("Incremental_Profit", ascending=False)
    .head(10)
    .copy()
)

adjust_campaigns = (
    campaigns[campaigns["Recommendation"].isin(["Adjust depth/mechanic", "Discontinue"])]
    .sort_values("Incremental_Profit", ascending=True)
    .head(10)
    .copy()
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Campaigns by Incremental Profit")

    top_display = top_campaigns[
        [
            "Campaign_ID",
            "Product",
            "Category",
            "Region",
            "Account",
            "Promo_Type",
            "Uplift_Pct",
            "Promo_ROI",
            "Incremental_Profit",
            "Recommendation",
        ]
    ].copy()

    top_display = display_percent_columns(top_display, ["Uplift_Pct", "Promo_ROI"])

    st.dataframe(
        top_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Uplift_Pct": st.column_config.NumberColumn("Uplift %", format="%.1f%%"),
            "Promo_ROI": st.column_config.NumberColumn("Promo ROI", format="%.1f%%"),
            "Incremental_Profit": st.column_config.NumberColumn(
                "Incremental Profit",
                format="$%.0f",
            ),
        },
    )

with col2:
    st.subheader("Campaigns to Adjust or Discontinue")

    adjust_display = adjust_campaigns[
        [
            "Campaign_ID",
            "Product",
            "Category",
            "Region",
            "Account",
            "Promo_Type",
            "Uplift_Pct",
            "Promo_ROI",
            "Incremental_Profit",
            "Recommendation",
        ]
    ].copy()

    adjust_display = display_percent_columns(adjust_display, ["Uplift_Pct", "Promo_ROI"])

    st.dataframe(
        adjust_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Uplift_Pct": st.column_config.NumberColumn("Uplift %", format="%.1f%%"),
            "Promo_ROI": st.column_config.NumberColumn("Promo ROI", format="%.1f%%"),
            "Incremental_Profit": st.column_config.NumberColumn(
                "Incremental Profit",
                format="$%.0f",
            ),
        },
    )

st.divider()

st.subheader("High Uplift but Low Commercial Return")

uplift_threshold = campaigns["Uplift_Pct"].quantile(0.75)

high_uplift_low_profit = (
    campaigns[
        (campaigns["Uplift_Pct"] >= uplift_threshold)
        & (campaigns["Incremental_Profit"] <= 0)
    ]
    .sort_values(["Uplift_Pct", "Incremental_Profit"], ascending=[False, True])
    .copy()
)

if high_uplift_low_profit.empty:
    st.success("No high-uplift, low-profit campaigns found under the selected filters.")
else:
    high_uplift_display = high_uplift_low_profit[
        [
            "Campaign_ID",
            "Product",
            "Category",
            "Region",
            "Account",
            "Promo_Type",
            "Uplift_Pct",
            "Promo_ROI",
            "Promo_Cost",
            "Incremental_Profit",
            "Recommendation",
        ]
    ].copy()

    high_uplift_display = display_percent_columns(
        high_uplift_display,
        ["Uplift_Pct", "Promo_ROI"],
    )

    st.dataframe(
        high_uplift_display.head(25),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Uplift_Pct": st.column_config.NumberColumn("Uplift %", format="%.1f%%"),
            "Promo_ROI": st.column_config.NumberColumn("Promo ROI", format="%.1f%%"),
            "Promo_Cost": st.column_config.NumberColumn("Promo Cost", format="$%.0f"),
            "Incremental_Profit": st.column_config.NumberColumn(
                "Incremental Profit",
                format="$%.0f",
            ),
        },
    )

    csv = high_uplift_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download high uplift / low return campaigns",
        data=csv,
        file_name="high_uplift_low_return_campaigns.csv",
        mime="text/csv",
    )
