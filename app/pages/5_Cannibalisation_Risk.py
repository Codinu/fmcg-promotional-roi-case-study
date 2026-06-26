from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.filters import apply_filters, render_sidebar_filters
from app.utils.charts import (
    cannibalised_units_by_category,
    promo_events_by_cannibalisation_risk,
    uplift_vs_cannibalisation_scatter,
)
from app.utils.data_loader import load_data
from app.utils.display import display_percent_columns
from app.utils.formatting import format_currency, format_number, format_percent
from app.utils.transformations import aggregate_campaigns, calculate_summary_metrics


st.set_page_config(
    page_title="Cannibalisation Risk | FMCG Promo ROI",
    page_icon="⚠️",
    layout="wide",
)

st.title("Cannibalisation Risk")
st.caption(
    "Identifying promotions where uplift may be offset by category switching or margin pressure."
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

metrics = calculate_summary_metrics(filtered_df)

kpi_cols = st.columns(4)
kpi_cols[0].metric(
    "High Risk Events",
    format_number(metrics["high_cannibalisation_events"]),
)
kpi_cols[1].metric(
    "Cannibalised Units",
    format_number(metrics["total_cannibalised_units"]),
)
kpi_cols[2].metric(
    "Avg Cannibalisation Rate",
    format_percent(metrics["avg_cannibalisation_rate"]),
)
kpi_cols[3].metric(
    "Incremental Profit",
    format_currency(metrics["total_incremental_profit"]),
)

st.divider()

left, right = st.columns(2)

with left:
    st.plotly_chart(
        cannibalised_units_by_category(campaigns),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        promo_events_by_cannibalisation_risk(campaigns),
        use_container_width=True,
    )

left, right = st.columns([1.1, 1])

with left:
    st.plotly_chart(
        uplift_vs_cannibalisation_scatter(campaigns),
        use_container_width=True,
    )

with right:
    st.subheader("Business Interpretation")
    st.markdown(
        """
Cannibalisation risk estimates whether promotional uplift may have come from shoppers 
switching within the same category rather than creating true incremental demand.

Cannibalisation risk does not automatically mean a promotion failed. It means the uplift 
should be reviewed with category context before repeating the campaign.
"""
    )
    st.info(
        "Commercial takeaway: high-uplift campaigns with high cannibalisation risk should be reviewed "
        "before repeat planning, especially if ROI or incremental profit is weak."
    )

st.divider()

st.subheader("High Cannibalisation Risk Campaigns")

high_risk = (
    campaigns[campaigns["Cannibalisation_Risk"] == "High"]
    .sort_values("Cannibalisation_Rate", ascending=False)
    .copy()
)

if high_risk.empty:
    st.success("No high cannibalisation risk campaigns under the selected filters.")
else:
    display_cols = [
        "Campaign_ID",
        "Product",
        "Category",
        "Region",
        "Account",
        "Promo_Type",
        "Uplift_Units",
        "Cannibalisation_Rate",
        "Cannibalised_Units",
        "Promo_ROI",
        "Incremental_Profit",
        "Recommendation",
    ]

    table = high_risk[display_cols].copy()
    table = display_percent_columns(table, ["Cannibalisation_Rate", "Promo_ROI"])

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Uplift_Units": st.column_config.NumberColumn(
                "Uplift Units",
                format="%.0f",
            ),
            "Cannibalisation_Rate": st.column_config.NumberColumn(
                "Cannibalisation Rate",
                format="%.1f%%",
            ),
            "Cannibalised_Units": st.column_config.NumberColumn(
                "Cannibalised Units",
                format="%.0f",
            ),
            "Promo_ROI": st.column_config.NumberColumn(
                "Promo ROI",
                format="%.1f%%",
            ),
            "Incremental_Profit": st.column_config.NumberColumn(
                "Incremental Profit",
                format="$%.0f",
            ),
        },
    )

    csv = table.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download high cannibalisation risk campaigns",
        data=csv,
        file_name="high_cannibalisation_risk_campaigns.csv",
        mime="text/csv",
    )
