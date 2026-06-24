# FMCG Promotional ROI synthetic dataset generator
# Run: python generate_fmcg_promo_roi_dataset.py
# Outputs: fmcg_promo_roi_synthetic_dataset.csv and fmcg_promo_roi_summary_tables.csv

import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

output_dir = Path(".")
csv_path = output_dir / "fmcg_promo_roi_synthetic_dataset.csv"
summary_path = output_dir / "fmcg_promo_roi_summary_tables.csv"

weeks = pd.date_range("2025-01-06", periods=52, freq="W-MON")

products = [
    {"Product": "Sparkling Water 1L", "Category": "Beverages", "Brand": "FreshFizz", "Regular_Price": 3.20, "Unit_Cost": 1.45, "Base_Demand": 850, "Promo_Sensitivity": 1.15},
    {"Product": "Cola 1.25L", "Category": "Beverages", "Brand": "FizzCo", "Regular_Price": 4.00, "Unit_Cost": 1.80, "Base_Demand": 1050, "Promo_Sensitivity": 1.35},
    {"Product": "Energy Drink 4pk", "Category": "Beverages", "Brand": "VoltMax", "Regular_Price": 9.50, "Unit_Cost": 5.10, "Base_Demand": 420, "Promo_Sensitivity": 0.95},
    {"Product": "Potato Chips 175g", "Category": "Snacks", "Brand": "CrunchyCo", "Regular_Price": 4.50, "Unit_Cost": 2.05, "Base_Demand": 930, "Promo_Sensitivity": 1.45},
    {"Product": "Chocolate Block 180g", "Category": "Snacks", "Brand": "SweetPeak", "Regular_Price": 5.20, "Unit_Cost": 2.40, "Base_Demand": 780, "Promo_Sensitivity": 1.30},
    {"Product": "Protein Bar 5pk", "Category": "Snacks", "Brand": "FitBite", "Regular_Price": 8.80, "Unit_Cost": 4.70, "Base_Demand": 360, "Promo_Sensitivity": 0.85},
    {"Product": "Laundry Liquid 2L", "Category": "Household", "Brand": "CleanWave", "Regular_Price": 13.00, "Unit_Cost": 6.80, "Base_Demand": 330, "Promo_Sensitivity": 1.05},
    {"Product": "Dishwashing Tablets 30pk", "Category": "Household", "Brand": "SparkHome", "Regular_Price": 18.00, "Unit_Cost": 9.50, "Base_Demand": 260, "Promo_Sensitivity": 1.10},
    {"Product": "Shampoo 400ml", "Category": "Personal Care", "Brand": "GlowLab", "Regular_Price": 7.50, "Unit_Cost": 3.60, "Base_Demand": 390, "Promo_Sensitivity": 1.00},
    {"Product": "Toothpaste 120g", "Category": "Personal Care", "Brand": "BrightSmile", "Regular_Price": 5.80, "Unit_Cost": 2.50, "Base_Demand": 520, "Promo_Sensitivity": 1.20},
    {"Product": "Pasta Sauce 500g", "Category": "Pantry", "Brand": "CasaBella", "Regular_Price": 4.20, "Unit_Cost": 1.90, "Base_Demand": 700, "Promo_Sensitivity": 1.25},
    {"Product": "Cereal 600g", "Category": "Pantry", "Brand": "MorningFarm", "Regular_Price": 6.80, "Unit_Cost": 3.20, "Base_Demand": 610, "Promo_Sensitivity": 1.15},
]

regions = {
    "NSW": {"Region_Factor": 1.20, "Store_Count_Factor": 1.25},
    "VIC": {"Region_Factor": 1.05, "Store_Count_Factor": 1.10},
    "QLD": {"Region_Factor": 0.95, "Store_Count_Factor": 0.95},
    "WA": {"Region_Factor": 0.72, "Store_Count_Factor": 0.75},
    "SA": {"Region_Factor": 0.55, "Store_Count_Factor": 0.60},
}

accounts = {
    "Woolworths": {"Account_Factor": 1.15, "Store_Count_Base": 90},
    "Coles": {"Account_Factor": 1.08, "Store_Count_Base": 85},
    "Independent": {"Account_Factor": 0.58, "Store_Count_Base": 55},
}

promo_types = {
    "Price Discount": {"Lift_Factor": 1.00, "Fixed_Cost": 400},
    "Multi-buy": {"Lift_Factor": 0.85, "Fixed_Cost": 300},
    "Catalogue Feature": {"Lift_Factor": 0.70, "Fixed_Cost": 750},
    "Display + Discount": {"Lift_Factor": 1.25, "Fixed_Cost": 1150},
    "Bundle": {"Lift_Factor": 0.60, "Fixed_Cost": 250},
}

category_cannibalisation = {
    "Beverages": 0.12,
    "Snacks": 0.16,
    "Household": 0.07,
    "Personal Care": 0.06,
    "Pantry": 0.10,
}

rows = []
campaign_counter = 1000

for week_idx, week in enumerate(weeks, start=1):
    month = week.month
    is_summer = month in [1, 2, 12]
    is_winter = month in [6, 7, 8]
    school_holiday = month in [1, 4, 7, 9, 12]

    for p in products:
        for region, rf in regions.items():
            for account, af in accounts.items():
                base = p["Base_Demand"] * rf["Region_Factor"] * af["Account_Factor"] * np.random.normal(1.0, 0.08)
                category = p["Category"]
                if category in ["Beverages", "Snacks"] and is_summer:
                    base *= 1.12
                if category == "Household" and is_winter:
                    base *= 1.08
                if category == "Pantry" and school_holiday:
                    base *= 1.05
                trend = 1 + (week_idx - 1) * np.random.normal(0.0008, 0.0002)
                baseline_units = max(20, int(round(base * trend)))

                promo_probability = 0.16
                if account in ["Woolworths", "Coles"]:
                    promo_probability += 0.05
                if category in ["Snacks", "Beverages"]:
                    promo_probability += 0.03
                promo_flag = np.random.rand() < promo_probability

                regular_price = p["Regular_Price"]
                unit_cost = p["Unit_Cost"]

                if promo_flag:
                    promo_type = np.random.choice(list(promo_types.keys()), p=[0.36, 0.20, 0.16, 0.20, 0.08])
                    discount_pct = np.random.choice([0.10, 0.15, 0.20, 0.25, 0.30, 0.35], p=[0.10, 0.20, 0.26, 0.22, 0.16, 0.06])
                    promo_price = round(regular_price * (1 - discount_pct), 2)
                    type_effect = promo_types[promo_type]["Lift_Factor"]
                    price_depth_effect = 0.45 * discount_pct / 0.10
                    uplift_pct_expected = p["Promo_Sensitivity"] * type_effect * price_depth_effect
                    uplift_pct_expected *= np.random.normal(1.0, 0.18)
                    uplift_pct_expected = np.clip(uplift_pct_expected, 0.05, 1.60)
                    actual_units = int(round(baseline_units * (1 + uplift_pct_expected)))
                    campaign_id = f"PR-{campaign_counter}"
                    campaign_counter += 1
                    funding_per_unit = max(0.03, regular_price - promo_price) * np.random.uniform(0.35, 0.65)
                    promo_cost = promo_types[promo_type]["Fixed_Cost"] + funding_per_unit * actual_units
                    cannibalisation_rate = category_cannibalisation[category]
                    cannibalisation_rate += 0.04 if discount_pct >= 0.30 else 0
                    cannibalisation_rate += 0.03 if promo_type == "Display + Discount" else 0
                    cannibalisation_rate *= np.random.normal(1.0, 0.12)
                    cannibalisation_rate = float(np.clip(cannibalisation_rate, 0.02, 0.35))
                else:
                    promo_type = "No Promo"
                    discount_pct = 0.0
                    promo_price = regular_price
                    actual_units = int(round(baseline_units * np.random.normal(1.0, 0.05)))
                    campaign_id = "No Promo"
                    promo_cost = 0.0
                    cannibalisation_rate = 0.0

                selling_price = promo_price if promo_flag else regular_price
                baseline_revenue = baseline_units * regular_price
                actual_revenue = actual_units * selling_price
                uplift_units = actual_units - baseline_units
                uplift_pct = uplift_units / baseline_units if baseline_units else 0
                baseline_gross_profit = baseline_units * (regular_price - unit_cost)
                promo_gross_profit_before_cost = actual_units * (selling_price - unit_cost)
                incremental_revenue_from_uplift = max(0, uplift_units) * selling_price
                revenue_impact_vs_baseline = actual_revenue - baseline_revenue
                incremental_gross_profit_before_cost = promo_gross_profit_before_cost - baseline_gross_profit
                incremental_profit_after_promo_cost = incremental_gross_profit_before_cost - promo_cost
                roi = (incremental_profit_after_promo_cost / promo_cost) if promo_cost > 0 else np.nan
                margin_pct_baseline = (regular_price - unit_cost) / regular_price
                margin_pct_actual = (selling_price - unit_cost) / selling_price if selling_price else 0
                margin_impact_pp = (margin_pct_actual - margin_pct_baseline) * 100
                store_count = int(round(af["Store_Count_Base"] * rf["Store_Count_Factor"] * np.random.normal(1.0, 0.04)))
                rate_of_sale = actual_units / store_count if store_count else np.nan
                cannibalised_units = max(0, uplift_units) * cannibalisation_rate
                cannibalisation_risk = "High" if cannibalisation_rate >= 0.18 and promo_flag else "Medium" if cannibalisation_rate >= 0.10 and promo_flag else "Low" if promo_flag else "N/A"

                if not promo_flag:
                    recommendation = "Baseline"
                elif roi >= 0.60 and incremental_profit_after_promo_cost > 0 and cannibalisation_risk != "High":
                    recommendation = "Repeat"
                elif uplift_pct > 0.25 and incremental_profit_after_promo_cost > 0 and roi >= 0:
                    recommendation = "Targeted repeat"
                elif uplift_pct > 0.20 and incremental_profit_after_promo_cost <= 0:
                    recommendation = "Adjust depth/mechanic"
                elif roi < 0:
                    recommendation = "Discontinue"
                else:
                    recommendation = "Review"

                rows.append({
                    "Week_Start": week.date(),
                    "Week_Number": week_idx,
                    "Campaign_ID": campaign_id,
                    "Product": p["Product"],
                    "Category": category,
                    "Brand": p["Brand"],
                    "Region": region,
                    "Account": account,
                    "Store_Count": store_count,
                    "Promo_Flag": int(promo_flag),
                    "Promo_Type": promo_type,
                    "Baseline_Units": baseline_units,
                    "Actual_Units": actual_units,
                    "Uplift_Units": uplift_units,
                    "Uplift_Pct": uplift_pct,
                    "Regular_Price": regular_price,
                    "Promo_Price": promo_price,
                    "Discount_Pct": discount_pct,
                    "Unit_Cost": unit_cost,
                    "Selling_Price": selling_price,
                    "Baseline_Revenue": baseline_revenue,
                    "Actual_Revenue": actual_revenue,
                    "Incremental_Revenue_From_Uplift": incremental_revenue_from_uplift,
                    "Revenue_Impact_vs_Baseline": revenue_impact_vs_baseline,
                    "Baseline_Gross_Profit": baseline_gross_profit,
                    "Gross_Profit_Before_Promo_Cost": promo_gross_profit_before_cost,
                    "Incremental_Gross_Profit_Before_Cost": incremental_gross_profit_before_cost,
                    "Promo_Cost": promo_cost,
                    "Incremental_Profit_After_Promo_Cost": incremental_profit_after_promo_cost,
                    "Promo_ROI": roi,
                    "Baseline_Gross_Margin_Pct": margin_pct_baseline,
                    "Actual_Gross_Margin_Pct": margin_pct_actual,
                    "Margin_Impact_pp": margin_impact_pp,
                    "Rate_of_Sale_Units_per_Store_per_Week": rate_of_sale,
                    "Cannibalisation_Rate_Estimate": cannibalisation_rate,
                    "Cannibalised_Units_Estimate": cannibalised_units,
                    "Cannibalisation_Risk": cannibalisation_risk,
                    "Recommendation": recommendation,
                })

df = pd.DataFrame(rows)
round_cols = [
    "Uplift_Pct", "Discount_Pct", "Baseline_Revenue", "Actual_Revenue",
    "Incremental_Revenue_From_Uplift", "Revenue_Impact_vs_Baseline",
    "Baseline_Gross_Profit", "Gross_Profit_Before_Promo_Cost",
    "Incremental_Gross_Profit_Before_Cost", "Promo_Cost",
    "Incremental_Profit_After_Promo_Cost", "Promo_ROI",
    "Baseline_Gross_Margin_Pct", "Actual_Gross_Margin_Pct",
    "Margin_Impact_pp", "Rate_of_Sale_Units_per_Store_per_Week",
    "Cannibalisation_Rate_Estimate", "Cannibalised_Units_Estimate"
]
for col in round_cols:
    df[col] = df[col].round(4)
df.to_csv(csv_path, index=False)

promo_df = df[df["Promo_Flag"] == 1].copy()
summary = (
    promo_df.groupby(["Category", "Promo_Type", "Recommendation"], dropna=False)
    .agg(
        Promo_Events=("Campaign_ID", "count"),
        Baseline_Units=("Baseline_Units", "sum"),
        Actual_Units=("Actual_Units", "sum"),
        Uplift_Units=("Uplift_Units", "sum"),
        Actual_Revenue=("Actual_Revenue", "sum"),
        Promo_Cost=("Promo_Cost", "sum"),
        Incremental_Profit_After_Promo_Cost=("Incremental_Profit_After_Promo_Cost", "sum"),
        Median_ROI=("Promo_ROI", "median"),
        Avg_Uplift_Pct=("Uplift_Pct", "mean"),
    )
    .reset_index()
    .sort_values(["Incremental_Profit_After_Promo_Cost"], ascending=False)
)
summary.to_csv(summary_path, index=False)
print(f"Generated {len(df):,} rows")
print(f"Promo rows: {len(promo_df):,}")
print(f"CSV: {csv_path}")
print(f"Summary: {summary_path}")
