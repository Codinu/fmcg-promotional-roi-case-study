from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "fmcg_promo_roi_synthetic_dataset_v2.csv"
)


REQUIRED_COLUMNS = {
    "Week_Start",
    "Week_Number",
    "Month",
    "Quarter",
    "Campaign_ID",
    "Product",
    "Category",
    "Brand",
    "Region",
    "Account",
    "Store_Count",
    "Promo_Flag",
    "Promo_Type",
    "Baseline_Units",
    "Actual_Units",
    "Uplift_Units",
    "Uplift_Pct",
    "Regular_Price",
    "Promo_Price",
    "Discount_Pct",
    "Unit_Cost",
    "Selling_Price",
    "Baseline_Revenue",
    "Actual_Revenue",
    "Incremental_Revenue_From_Uplift",
    "Promo_Cost",
    "Incremental_Profit_After_Promo_Cost",
    "Promo_ROI",
    "Margin_Impact_pp",
    "Rate_of_Sale_Units_per_Store_per_Week",
    "Cannibalisation_Rate_Estimate",
    "Cannibalised_Units_Estimate",
    "Cannibalisation_Risk",
    "Recommendation",
}


def validate_columns(df: pd.DataFrame) -> None:
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        raise ValueError(
            "Dataset is missing required columns: " + ", ".join(missing)
        )


@st.cache_data(show_spinner="Loading FMCG promotional ROI dataset...")
def load_data(path: str | Path = DATA_PATH) -> pd.DataFrame:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {path}. "
            "Expected file: data/fmcg_promo_roi_synthetic_dataset_v2.csv"
        )

    df = pd.read_csv(path)
    validate_columns(df)

    df["Week_Start"] = pd.to_datetime(df["Week_Start"], errors="coerce")
    df["Promo_Flag"] = df["Promo_Flag"].astype(int)
    df["Is_Promo"] = df["Promo_Flag"] == 1
    df["Positive_ROI"] = df["Promo_ROI"] > 0

    df["Profit_Status"] = pd.cut(
        df["Incremental_Profit_After_Promo_Cost"],
        bins=[float("-inf"), 0, 500, 1500, float("inf")],
        labels=["Negative", "Low positive", "Medium positive", "High positive"],
    )

    return df