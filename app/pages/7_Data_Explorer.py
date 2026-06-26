from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.filters import apply_filters, render_sidebar_filters
from app.utils.data_loader import load_data
from app.utils.display import display_percent_columns
from app.utils.formatting import format_number
from app.utils.transformations import aggregate_campaigns, calculate_summary_metrics


st.set_page_config(
    page_title="Data Explorer | FMCG Promo ROI",
    page_icon="🔎",
    layout="wide",
)

st.title("Data Explorer")
st.caption(
    "Inspect raw data, campaign-level aggregates, metric definitions and filtered exports."
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
campaigns = aggregate_campaigns(filtered_df)

summary_cols = st.columns(4)
summary_cols[0].metric("Filtered Rows", format_number(len(filtered_df)))
summary_cols[1].metric("Promo Rows", format_number(metrics["promo_event_count"]))
summary_cols[2].metric("Campaign Rows", format_number(len(campaigns)))
summary_cols[3].metric("Columns", format_number(len(filtered_df.columns)))

st.divider()

tab_raw, tab_campaign, tab_metrics, tab_dictionary = st.tabs(
    [
        "Raw Data",
        "Campaign Aggregates",
        "Metric Definitions",
        "Data Dictionary",
    ]
)

with tab_raw:
    st.subheader("Filtered Raw Data")

    search_term = st.text_input(
        "Search product, category, brand, region, account, promo type or recommendation",
        value="",
        key="raw_search",
    )

    raw_display = filtered_df.copy()

    if search_term:
        search_columns = [
            "Product",
            "Category",
            "Brand",
            "Region",
            "Account",
            "Promo_Type",
            "Recommendation",
            "Campaign_ID",
        ]

        mask = pd.Series(False, index=raw_display.index)

        for column in search_columns:
            if column in raw_display.columns:
                mask = mask | raw_display[column].astype(str).str.contains(
                    search_term,
                    case=False,
                    na=False,
                )

        raw_display = raw_display[mask]

    default_cols = [
        "Week_Start",
        "Campaign_ID",
        "Product",
        "Category",
        "Brand",
        "Region",
        "Account",
        "Promo_Flag",
        "Promo_Type",
        "Baseline_Units",
        "Actual_Units",
        "Uplift_Units",
        "Uplift_Pct",
        "Discount_Pct",
        "Promo_ROI",
        "Incremental_Profit_After_Promo_Cost",
        "Cannibalisation_Risk",
        "Recommendation",
    ]

    available_default_cols = [col for col in default_cols if col in raw_display.columns]

    selected_columns = st.multiselect(
        "Columns to display",
        options=raw_display.columns.tolist(),
        default=available_default_cols,
        key="raw_columns",
    )

    raw_table = raw_display[selected_columns].copy() if selected_columns else raw_display.copy()

    percent_cols = [
        col
        for col in ["Uplift_Pct", "Discount_Pct", "Promo_ROI", "Cannibalisation_Rate_Estimate"]
        if col in raw_table.columns
    ]

    raw_table_display = display_percent_columns(raw_table, percent_cols)

    st.dataframe(
        raw_table_display,
        use_container_width=True,
        hide_index=True,
    )

    csv = raw_table.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered raw data CSV",
        data=csv,
        file_name="filtered_raw_fmcg_promo_roi_data.csv",
        mime="text/csv",
    )

with tab_campaign:
    st.subheader("Campaign-Level Aggregates")

    if campaigns.empty:
        st.info("No campaign aggregates available for the selected filters.")
    else:
        sort_metric = st.selectbox(
            "Sort campaigns by",
            [
                "Incremental_Profit",
                "Promo_ROI",
                "Uplift_Pct",
                "Promo_Cost",
                "Cannibalisation_Rate",
                "Rate_of_Sale",
            ],
            index=0,
        )

        sort_direction = st.radio(
            "Sort direction",
            ["Descending", "Ascending"],
            horizontal=True,
            index=0,
        )

        campaign_table = campaigns.sort_values(
            sort_metric,
            ascending=sort_direction == "Ascending",
        ).copy()

        display_cols = [
            "Campaign_ID",
            "Product",
            "Category",
            "Brand",
            "Region",
            "Account",
            "Promo_Type",
            "Baseline_Units",
            "Actual_Units",
            "Uplift_Units",
            "Uplift_Pct",
            "Discount_Pct",
            "Promo_ROI",
            "Promo_Cost",
            "Incremental_Profit",
            "Rate_of_Sale",
            "Cannibalisation_Rate",
            "Cannibalised_Units",
            "Cannibalisation_Risk",
            "Recommendation",
        ]

        display_cols = [col for col in display_cols if col in campaign_table.columns]
        campaign_table = campaign_table[display_cols]

        campaign_table_display = display_percent_columns(
            campaign_table,
            ["Uplift_Pct", "Discount_Pct", "Promo_ROI", "Cannibalisation_Rate"],
        )

        st.dataframe(
            campaign_table_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Uplift_Pct": st.column_config.NumberColumn("Uplift %", format="%.1f%%"),
                "Discount_Pct": st.column_config.NumberColumn("Discount %", format="%.1f%%"),
                "Promo_ROI": st.column_config.NumberColumn("Promo ROI", format="%.1f%%"),
                "Promo_Cost": st.column_config.NumberColumn("Promo Cost", format="$%.0f"),
                "Incremental_Profit": st.column_config.NumberColumn(
                    "Incremental Profit",
                    format="$%.0f",
                ),
                "Cannibalisation_Rate": st.column_config.NumberColumn(
                    "Cannibalisation Rate",
                    format="%.1f%%",
                ),
                "Rate_of_Sale": st.column_config.NumberColumn(
                    "Rate of Sale",
                    format="%.1f",
                ),
            },
        )

        csv = campaign_table.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download campaign aggregate CSV",
            data=csv,
            file_name="campaign_aggregates_filtered.csv",
            mime="text/csv",
        )

with tab_metrics:
    st.subheader("Metric Definitions")

    st.markdown(
        """
| Metric | Definition |
|---|---|
| Baseline Units | Expected sales units without promotion |
| Actual Units | Observed sales units during the period |
| Uplift Units | Actual Units - Baseline Units |
| Uplift % | Uplift Units / Baseline Units |
| Discount % | (Regular Price - Promo Price) / Regular Price |
| Incremental Revenue | Uplift Units x Promo Price |
| Promo Cost | Simulated trade spend or promotional investment |
| Incremental Profit | Incremental Gross Profit after promo cost |
| Promo ROI | Incremental Profit / Promo Cost |
| Positive ROI Rate | Share of promotional events with Promo ROI greater than 0 |
| Rate of Sale | Units sold per store per week |
| Margin Impact pp | Change in gross margin percentage points due to promotion |
| Cannibalisation Rate | Estimated share of uplift offset by category switching |
| Cannibalised Units | Uplift Units x Cannibalisation Rate |
| Recommendation | Commercial action group: Repeat, Targeted repeat, Adjust depth/mechanic or Discontinue |
"""
    )

    st.info(
        "The dataset is synthetic. Metric definitions are designed to mirror common FMCG promotional analytics logic."
    )

with tab_dictionary:
    st.subheader("Data Dictionary")

    dictionary_rows = [
        ("Week_Start", "Start date of the sales week"),
        ("Week_Number", "Week number in the simulated year"),
        ("Month", "Calendar month label"),
        ("Quarter", "Calendar quarter label"),
        ("Campaign_ID", "Promotion campaign identifier"),
        ("Product", "Product name"),
        ("Category", "FMCG product category"),
        ("Brand", "Brand name"),
        ("Region", "Australian state / sales region"),
        ("Account", "Retail account or store group"),
        ("Store_Count", "Number of stores in the simulated account-region combination"),
        ("Promo_Flag", "1 if promotion is active, otherwise 0"),
        ("Promo_Type", "Promotion mechanic"),
        ("Baseline_Units", "Expected units without promotion"),
        ("Actual_Units", "Observed units"),
        ("Uplift_Units", "Incremental units above baseline"),
        ("Uplift_Pct", "Percentage uplift vs baseline"),
        ("Regular_Price", "Non-promotional shelf price"),
        ("Promo_Price", "Promotional selling price"),
        ("Discount_Pct", "Discount depth"),
        ("Unit_Cost", "Simulated cost per unit"),
        ("Incremental_Revenue_From_Uplift", "Revenue from incremental units"),
        ("Promo_Cost", "Promotional investment / trade spend"),
        ("Incremental_Profit_After_Promo_Cost", "Incremental profit after promo cost"),
        ("Promo_ROI", "Return on promotional investment"),
        ("Margin_Impact_pp", "Gross margin impact in percentage points"),
        ("Rate_of_Sale_Units_per_Store_per_Week", "Sales velocity per store per week"),
        ("Cannibalisation_Rate_Estimate", "Estimated switching / cannibalisation rate"),
        ("Cannibalised_Units_Estimate", "Estimated cannibalised units"),
        ("Cannibalisation_Risk", "Low / Medium / High risk label"),
        ("Recommendation", "Commercial action recommendation"),
    ]

    dictionary_df = pd.DataFrame(
        dictionary_rows,
        columns=["Column", "Description"],
    )

    st.dataframe(
        dictionary_df,
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Data Explorer is designed for transparency: users can inspect both raw records and campaign-level aggregates."
)
