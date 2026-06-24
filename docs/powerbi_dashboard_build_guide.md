# Power BI Dashboard Build Guide

This document outlines the planned Power BI dashboard for the FMCG Promotional ROI Case Study.

The dashboard is designed for account managers, sales teams, category teams, buyers, and senior stakeholders who need to understand which promotions should be repeated, adjusted, reviewed, or discontinued.

---

## Dashboard Objective

The objective of the dashboard is to evaluate whether FMCG promotional campaigns generated profitable incremental growth.

The dashboard should help users answer:

* Which promotions generated profitable uplift?
* Which campaigns increased volume but reduced profit?
* Which promo mechanics performed best?
* Which products, categories, regions, and accounts responded best?
* Which campaigns had high cannibalisation risk?
* Which promotions should be repeated, adjusted, reviewed, or discontinued?

---

## Data Source

Primary dataset:

`data/fmcg_promo_roi_synthetic_dataset_v2.csv`

Primary notebook:

`notebooks/fmcg_promo_roi_analysis_v2.ipynb`

Dataset grain:

`Week × Product × Region × Account`

---

## Recommended Power BI Pages

The dashboard should contain five pages:

1. Executive Summary
2. Promo ROI by Campaign
3. Uplift vs Margin Impact
4. Category / Product / Region Analysis
5. Cannibalisation Risk

---

## Page 1: Executive Summary

### Purpose

Provide a high-level view of promotional performance for senior stakeholders and account managers.

### Recommended Slicers

* Month
* Quarter
* Category
* Brand
* Product
* Region
* Account
* Promo_Type
* Recommendation

### KPI Cards

* Total Actual Revenue
* Total Incremental Revenue
* Total Promo Cost
* Total Incremental Profit
* Median Promo ROI
* Average Uplift %
* Positive ROI Rate
* High Cannibalisation Risk Events

### Recommended Visuals

| Visual                                          | Purpose                                     |
| ----------------------------------------------- | ------------------------------------------- |
| KPI cards                                       | Show headline promotional performance       |
| Bar chart: Incremental Profit by Recommendation | Show commercial action split                |
| Bar chart: Median ROI by Promo Type             | Compare promotional mechanics               |
| Table: Top campaigns by Incremental Profit      | Identify campaigns to repeat                |
| Table: Bottom campaigns by ROI                  | Identify campaigns to adjust or discontinue |

### Key Business Message

This page should quickly show whether promotional investment generated profitable incremental growth.

---

## Page 2: Promo ROI by Campaign

### Purpose

Identify which campaigns performed best or worst at campaign level.

### Recommended Visuals

| Visual       | Fields                                                                                                                                                |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scatter plot | X = Uplift_Pct, Y = Promo_ROI, Size = Incremental_Revenue_From_Uplift, Legend = Recommendation                                                        |
| Bar chart    | Campaign_ID by Incremental_Profit_After_Promo_Cost                                                                                                    |
| Table        | Campaign_ID, Product, Category, Region, Account, Promo_Type, Discount_Pct, Uplift_Pct, Promo_ROI, Incremental_Profit_After_Promo_Cost, Recommendation |

### Key Business Message

A campaign should not be judged by uplift alone. Campaigns with strong volume uplift but weak ROI may need a lower discount depth, different promotional mechanic, or better retailer funding.

---

## Page 3: Uplift vs Margin Impact

### Purpose

Show the trade-off between promotional volume growth and margin erosion.

### Recommended Visuals

| Visual       | Fields                                                                                     |
| ------------ | ------------------------------------------------------------------------------------------ |
| Scatter plot | X = Discount_Pct, Y = Uplift_Pct, Legend = Promo_Type                                      |
| Scatter plot | X = Discount_Pct, Y = Margin_Impact_pp, Legend = Category                                  |
| Bar chart    | Promo_Type by average Margin_Impact_pp                                                     |
| Table        | Product, Promo_Type, Discount_Pct, Uplift_Pct, Margin_Impact_pp, Promo_ROI, Recommendation |

### Key Business Message

Some promotions may drive strong sales uplift but damage gross margin. These campaigns should be reviewed before being repeated.

---

## Page 4: Category / Product / Region Analysis

### Purpose

Compare promotional performance across categories, products, accounts, and regions.

### Recommended Visuals

| Visual    | Fields                                                                                  |
| --------- | --------------------------------------------------------------------------------------- |
| Bar chart | Category by Incremental_Profit_After_Promo_Cost                                         |
| Bar chart | Region by Promo_ROI                                                                     |
| Bar chart | Account by Rate_of_Sale_Units_per_Store_per_Week                                        |
| Matrix    | Category × Region with Promo_ROI or Incremental_Profit_After_Promo_Cost                 |
| Table     | Product, Category, Region, Account, Uplift_Pct, Promo_ROI, Rate_of_Sale, Recommendation |

### Key Business Message

Performance should be reviewed by category, account, and region. Some promotions may be suitable for targeted repeat rather than full national rollout.

---

## Page 5: Cannibalisation Risk

### Purpose

Identify promotions where uplift may have come from switching within the same category rather than true incremental demand.

### Recommended Visuals

| Visual       | Fields                                                                                                    |
| ------------ | --------------------------------------------------------------------------------------------------------- |
| Bar chart    | Category by Cannibalised_Units_Estimate                                                                   |
| Bar chart    | Cannibalisation_Risk by Promotional Event Count                                                           |
| Scatter plot | X = Uplift_Units, Y = Cannibalisation_Rate_Estimate, Legend = Recommendation                              |
| Table        | Campaign_ID, Product, Category, Promo_Type, Uplift_Units, Cannibalisation_Risk, Promo_ROI, Recommendation |

### Key Business Message

High cannibalisation risk campaigns should be reviewed with category context before being repeated, especially if ROI is weak.

---

## Recommended DAX Measures

### Revenue and Profit

Total Actual Revenue =
SUM('PromoData'[Actual_Revenue])

Total Baseline Revenue =
SUM('PromoData'[Baseline_Revenue])

Total Incremental Revenue =
SUM('PromoData'[Incremental_Revenue_From_Uplift])

Total Promo Cost =
SUM('PromoData'[Promo_Cost])

Total Incremental Profit =
SUM('PromoData'[Incremental_Profit_After_Promo_Cost])

Promo ROI =
DIVIDE(
[Total Incremental Profit],
[Total Promo Cost]
)

### Volume and Uplift

Total Baseline Units =
SUM('PromoData'[Baseline_Units])

Total Actual Units =
SUM('PromoData'[Actual_Units])

Total Uplift Units =
SUM('PromoData'[Uplift_Units])

Average Uplift % =
AVERAGE('PromoData'[Uplift_Pct])

### Margin

Average Baseline Gross Margin % =
AVERAGE('PromoData'[Baseline_Gross_Margin_Pct])

Average Actual Gross Margin % =
AVERAGE('PromoData'[Actual_Gross_Margin_Pct])

Average Margin Impact pp =
AVERAGE('PromoData'[Margin_Impact_pp])

### Promo Counts

Promo Event Count =
CALCULATE(
COUNTROWS('PromoData'),
'PromoData'[Promo_Flag] = 1
)

Positive ROI Promo Count =
CALCULATE(
COUNTROWS('PromoData'),
'PromoData'[Promo_Flag] = 1,
'PromoData'[Promo_ROI] > 0
)

Positive ROI Rate =
DIVIDE(
[Positive ROI Promo Count],
[Promo Event Count]
)

High Cannibalisation Risk Events =
CALCULATE(
COUNTROWS('PromoData'),
'PromoData'[Promo_Flag] = 1,
'PromoData'[Cannibalisation_Risk] = "High"
)

### Rate of Sale

Average Rate of Sale =
AVERAGE('PromoData'[Rate_of_Sale_Units_per_Store_per_Week])

---

## Recommended Dashboard Design Principles

* Use KPI cards for senior stakeholder headline metrics.
* Use slicers to allow account, category, region, and promo type filtering.
* Use scatter plots to show trade-offs between uplift, ROI, and margin.
* Use tables for account-manager-facing action lists.
* Use recommendation categories to make the dashboard action-oriented.
* Avoid judging promotion success by uplift alone.
* Prioritise commercial interpretation over visual complexity.

---

## Account Manager Use Case

An account manager could use this dashboard to prepare for a monthly promotional review or buyer discussion.

Example workflow:

1. Filter to a specific account or region.
2. Review total incremental profit and positive ROI rate.
3. Identify campaigns with strong ROI and manageable cannibalisation risk.
4. Identify campaigns with high uplift but weak profit.
5. Decide whether each campaign should be repeated, adjusted, reviewed, or discontinued.
6. Use Sales_Action and Buyer_Message fields to support next-step recommendations.

---

## Final Output Goal

The final Power BI dashboard should allow a commercial stakeholder to answer:

* What worked?
* What did not work?
* Why did it happen?
* What should we do next?
