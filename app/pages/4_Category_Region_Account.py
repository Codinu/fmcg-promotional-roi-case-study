from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.filters import apply_filters, render_sidebar_filters
from app.utils.charts import (
    category_region_profit_heatmap,
    incremental_profit_by_category,
    promo_roi_by_region,
    rate_of_sale_by_account,
)
from app.utils.data_loader import load_data
from app.utils.display import display_percent_columns
from app.utils.transformations import aggregate_campaigns


st.set_page_config(
    page_title="Category / Region / Account | FMCG Promo ROI",
    page_icon="??",
    layout="wide",
)

st.title("Category / Region / Account Analysis")
st.caption(
    "Comparing promotional performance across categories, products, accounts and regions."
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

col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(
        incremental_profit_by_category(campaigns),
        use_container_width=True,
    )

with col2:
    st.plotly_chart(
        promo_roi_by_region(campaigns),
        use_container_width=True,
    )

with col3:
    st.plotly_chart(
        rate_of_sale_by_account(campaigns),
        use_container_width=True,
    )

left, right = st.columns([1.05, 1])

with left:
    st.plotly_chart(
        category_region_profit_heatmap(campaigns),
        use_container_width=True,
    )

with right:
    st.subheader("Business Interpretation")
    st.markdown(
        """
This page moves from individual campaign performance to **category, account and regional planning**.

A campaign that works well in one category, region or account may not deserve a full national rollout. 
This view helps identify where promotions should be repeated broadly, targeted selectively or reviewed 
with account-specific context.
"""
    )
    st.info(
        "Commercial takeaway: use category, region and account cuts to identify targeted repeat opportunities "
        "instead of assuming one national promotional strategy fits every market."
    )

st.divider()

st.subheader("Product Performance Detail")

product_detail = (
    campaigns.groupby(
        ["Product", "Category", "Account", "Region", "Recommendation"],
        dropna=False,
    )
    .agg(
        Total_Uplift_Units=("Uplift_Units", "sum"),
        Average_Uplift_Pct=("Uplift_Pct", "mean"),
        Promo_ROI=("Promo_ROI", "mean"),
        Incremental_Profit=("Incremental_Profit", "sum"),
        Rate_of_Sale=("Rate_of_Sale", "mean"),
    )
    .reset_index()
    .sort_values("Incremental_Profit", ascending=False)
)

display_cols = [
    "Product",
    "Category",
    "Account",
    "Region",
    "Total_Uplift_Units",
    "Average_Uplift_Pct",
    "Promo_ROI",
    "Incremental_Profit",
    "Rate_of_Sale",
    "Recommendation",
]

product_display = product_detail[display_cols].head(30).copy()
product_display = display_percent_columns(
    product_display,
    ["Average_Uplift_Pct", "Promo_ROI"],
)

st.dataframe(
    product_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Total_Uplift_Units": st.column_config.NumberColumn(
            "Uplift Units",
            format="%.0f",
        ),
        "Average_Uplift_Pct": st.column_config.NumberColumn(
            "Avg Uplift %",
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
        "Rate_of_Sale": st.column_config.NumberColumn(
            "Rate of Sale",
            format="%.1f",
        ),
    },
)

csv = product_display.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download product performance CSV",
    data=csv,
    file_name="product_performance_filtered.csv",
    mime="text/csv",
)
