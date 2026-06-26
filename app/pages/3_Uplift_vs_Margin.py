from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.filters import apply_filters, render_sidebar_filters
from app.utils.charts import (
    discount_vs_margin_scatter,
    discount_vs_uplift_scatter,
    margin_pressure_by_promo_type,
)
from app.utils.data_loader import load_data
from app.utils.display import display_percent_columns
from app.utils.transformations import aggregate_campaigns


st.set_page_config(
    page_title="Uplift vs Margin Impact | FMCG Promo ROI",
    page_icon="??",
    layout="wide",
)

st.title("Uplift vs Margin Impact")
st.caption(
    "Understanding the trade-off between discount depth, volume uplift and gross margin pressure."
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

left, right = st.columns(2)

with left:
    st.plotly_chart(
        discount_vs_uplift_scatter(campaigns),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        discount_vs_margin_scatter(campaigns),
        use_container_width=True,
    )

left, right = st.columns([1, 1])

with left:
    st.plotly_chart(
        margin_pressure_by_promo_type(campaigns),
        use_container_width=True,
    )

with right:
    st.subheader("Business Interpretation")
    st.markdown(
        """
This page separates **volume response** from **margin quality**.

A deeper discount may drive more units, but it can also reduce unit margin and weaken 
incremental profit. The best promotional mechanic is not necessarily the one with the highest uplift; 
it is the one that balances uplift, margin and promo cost.
"""
    )
    st.info(
        "Commercial takeaway: campaigns with strong uplift but heavy margin pressure should be adjusted "
        "through lower discount depth, different mechanics or improved retailer funding."
    )

st.divider()

st.subheader("High Uplift with Margin Pressure")

high_uplift_threshold = campaigns["Uplift_Pct"].quantile(0.75)

margin_pressure = (
    campaigns[
        (campaigns["Uplift_Pct"] >= high_uplift_threshold)
        & (campaigns["Margin_Impact_pp"] <= -10)
    ]
    .sort_values(["Uplift_Pct", "Margin_Impact_pp"], ascending=[False, True])
    .copy()
)

if margin_pressure.empty:
    st.success("No high-uplift campaigns with material margin pressure under the selected filters.")
else:
    display_cols = [
        "Campaign_ID",
        "Product",
        "Category",
        "Region",
        "Account",
        "Promo_Type",
        "Discount_Pct",
        "Uplift_Pct",
        "Margin_Impact_pp",
        "Promo_ROI",
        "Incremental_Profit",
        "Recommendation",
    ]

    table = margin_pressure[display_cols].head(25).copy()
    table = display_percent_columns(table, ["Discount_Pct", "Uplift_Pct", "Promo_ROI"])

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Discount_Pct": st.column_config.NumberColumn("Discount %", format="%.1f%%"),
            "Uplift_Pct": st.column_config.NumberColumn("Uplift %", format="%.1f%%"),
            "Promo_ROI": st.column_config.NumberColumn("Promo ROI", format="%.1f%%"),
            "Margin_Impact_pp": st.column_config.NumberColumn(
                "Margin Impact pp",
                format="%.1f",
            ),
            "Incremental_Profit": st.column_config.NumberColumn(
                "Incremental Profit",
                format="$%.0f",
            ),
        },
    )

    csv = table.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download margin pressure campaigns",
        data=csv,
        file_name="high_uplift_margin_pressure_campaigns.csv",
        mime="text/csv",
    )
