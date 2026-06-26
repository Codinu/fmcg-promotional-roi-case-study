from __future__ import annotations

import streamlit as st

from app.utils.formatting import format_currency, format_number, format_percent


def render_kpi_grid(metrics: dict[str, float]) -> None:
    row_1 = st.columns(4)

    row_1[0].metric("Promo Event Count", format_number(metrics["promo_event_count"]))
    row_1[1].metric("Positive ROI Rate", format_percent(metrics["positive_roi_rate"]))
    row_1[2].metric("Median Promo ROI", format_percent(metrics["median_promo_roi"]))
    row_1[3].metric(
        "Incremental Profit",
        format_currency(metrics["total_incremental_profit"]),
    )

    row_2 = st.columns(4)

    row_2[0].metric("Promo Cost", format_currency(metrics["total_promo_cost"]))
    row_2[1].metric("Average Uplift %", format_percent(metrics["avg_uplift_pct"]))
    row_2[2].metric("Incremental Revenue", format_currency(metrics["incremental_revenue"]))
    row_2[3].metric(
        "High Canni. Risk",
        format_number(metrics["high_cannibalisation_events"]),
    )