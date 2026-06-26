from __future__ import annotations

import pandas as pd


def promo_only(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Promo_Flag"] == 1].copy()


def calculate_summary_metrics(df: pd.DataFrame) -> dict[str, float]:
    promo_df = promo_only(df)
    promo_event_count = len(promo_df)

    if promo_event_count == 0:
        return {
            "promo_event_count": 0,
            "positive_roi_rate": 0,
            "avg_promo_roi": 0,
            "median_promo_roi": 0,
            "total_incremental_profit": 0,
            "total_promo_cost": 0,
            "avg_uplift_pct": 0,
            "incremental_revenue": 0,
            "high_cannibalisation_events": 0,
            "total_cannibalised_units": 0,
            "avg_cannibalisation_rate": 0,
        }

    positive_roi_count = int((promo_df["Promo_ROI"] > 0).sum())

    return {
        "promo_event_count": promo_event_count,
        "positive_roi_rate": positive_roi_count / promo_event_count,
        "avg_promo_roi": promo_df["Promo_ROI"].mean(),
        "median_promo_roi": promo_df["Promo_ROI"].median(),
        "total_incremental_profit": promo_df[
            "Incremental_Profit_After_Promo_Cost"
        ].sum(),
        "total_promo_cost": promo_df["Promo_Cost"].sum(),
        "avg_uplift_pct": promo_df["Uplift_Pct"].mean(),
        "incremental_revenue": promo_df[
            "Incremental_Revenue_From_Uplift"
        ].sum(),
        "high_cannibalisation_events": int(
            (promo_df["Cannibalisation_Risk"] == "High").sum()
        ),
        "total_cannibalised_units": promo_df[
            "Cannibalised_Units_Estimate"
        ].sum(),
        "avg_cannibalisation_rate": promo_df[
            "Cannibalisation_Rate_Estimate"
        ].mean(),
    }


def aggregate_campaigns(df: pd.DataFrame) -> pd.DataFrame:
    promo_df = promo_only(df)

    if promo_df.empty:
        return pd.DataFrame()

    return (
        promo_df.groupby(
            [
                "Campaign_ID",
                "Product",
                "Category",
                "Brand",
                "Region",
                "Account",
                "Promo_Type",
                "Recommendation",
                "Cannibalisation_Risk",
            ],
            dropna=False,
        )
        .agg(
            Baseline_Units=("Baseline_Units", "sum"),
            Actual_Units=("Actual_Units", "sum"),
            Uplift_Units=("Uplift_Units", "sum"),
            Uplift_Pct=("Uplift_Pct", "mean"),
            Discount_Pct=("Discount_Pct", "mean"),
            Margin_Impact_pp=("Margin_Impact_pp", "mean"),
            Incremental_Revenue=("Incremental_Revenue_From_Uplift", "sum"),
            Promo_Cost=("Promo_Cost", "sum"),
            Incremental_Profit=("Incremental_Profit_After_Promo_Cost", "sum"),
            Promo_ROI=("Promo_ROI", "mean"),
            Rate_of_Sale=("Rate_of_Sale_Units_per_Store_per_Week", "mean"),
            Cannibalisation_Rate=("Cannibalisation_Rate_Estimate", "mean"),
            Cannibalised_Units=("Cannibalised_Units_Estimate", "sum"),
        )
        .reset_index()
    )


def recommendation_summary(df: pd.DataFrame) -> pd.DataFrame:
    promo_df = promo_only(df)

    if promo_df.empty:
        return pd.DataFrame()

    return (
        promo_df.groupby("Recommendation", dropna=False)
        .agg(
            Promo_Events=("Campaign_ID", "count"),
            Incremental_Profit=("Incremental_Profit_After_Promo_Cost", "sum"),
            Promo_Cost=("Promo_Cost", "sum"),
            Uplift_Units=("Uplift_Units", "sum"),
            Avg_Uplift_Pct=("Uplift_Pct", "mean"),
        )
        .reset_index()
        .assign(
            Promo_ROI=lambda x: x["Incremental_Profit"] / x["Promo_Cost"].replace(0, pd.NA)
        )
    )


def promo_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    promo_df = promo_only(df)

    if promo_df.empty:
        return pd.DataFrame()

    return (
        promo_df.groupby("Promo_Type", dropna=False)
        .agg(
            Promo_Events=("Campaign_ID", "count"),
            Incremental_Profit=("Incremental_Profit_After_Promo_Cost", "sum"),
            Promo_Cost=("Promo_Cost", "sum"),
            Avg_Uplift_Pct=("Uplift_Pct", "mean"),
        )
        .reset_index()
        .assign(
            Promo_ROI=lambda x: x["Incremental_Profit"] / x["Promo_Cost"].replace(0, pd.NA)
        )
    )