from __future__ import annotations

import pandas as pd
import streamlit as st


FILTER_COLUMNS = [
    "Quarter",
    "Week_Number",
    "Category",
    "Product",
    "Brand",
    "Region",
    "Account",
    "Promo_Type",
    "Recommendation",
]


def render_sidebar_filters(df: pd.DataFrame) -> dict[str, list]:
    st.sidebar.header("Filters")

    filters: dict[str, list] = {}

    for column in FILTER_COLUMNS:
        if column not in df.columns:
            continue

        values = sorted(df[column].dropna().unique().tolist())

        selected = st.sidebar.multiselect(
            label=column.replace("_", " "),
            options=values,
            default=[],
            key=f"filter_{column}",
        )

        filters[column] = selected

    st.sidebar.divider()
    st.sidebar.caption(
        "Synthetic FMCG promotional dataset. Filters apply to all pages where relevant."
    )

    return filters


def apply_filters(df: pd.DataFrame, filters: dict[str, list]) -> pd.DataFrame:
    filtered = df.copy()

    for column, selected_values in filters.items():
        if selected_values:
            filtered = filtered[filtered[column].isin(selected_values)]

    return filtered