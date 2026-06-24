# Data Dictionary

This dataset represents weekly FMCG promotional performance at product-account-region level.

It is synthetic and designed for commercial analytics practice, including promotional ROI, sales uplift, margin impact, rate of sale, cannibalisation risk, and account-manager-facing recommendations.

The v2 dataset is the primary dataset used for analysis.

Primary file:

`data/fmcg_promo_roi_synthetic_dataset_v2.csv`

---

## Dataset Grain

Each row represents weekly performance for one product, in one region, under one retail account.

In business terms:

`Week × Product × Region × Account`

This structure supports analysis across:

* Weekly trading performance
* Product and category performance
* Retail account comparison
* Regional performance
* Promotional mechanic effectiveness
* Account-manager-facing promotional recommendations

---

## Field Definitions

| Field                                 | Description                                                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Week_Start                            | Start date of the sales week                                                                                                   |
| Week_Number                           | Week number in the analysis year                                                                                               |
| Month                                 | Month label used for monthly reporting                                                                                         |
| Quarter                               | Quarter label used for quarterly reporting                                                                                     |
| Campaign_ID                           | Unique campaign identifier for promotional events; non-promotional rows are labelled as No Promo                               |
| Product                               | Product or SKU name                                                                                                            |
| Category                              | FMCG product category                                                                                                          |
| Brand                                 | Product brand                                                                                                                  |
| Region                                | Australian sales region or state                                                                                               |
| Account                               | Retail account or customer group                                                                                               |
| Store_Count                           | Number of stores covered by the account-region combination                                                                     |
| Promo_Flag                            | Indicates whether the product was on promotion; 1 = promotion, 0 = no promotion                                                |
| Promo_Type                            | Promotional mechanic, such as price discount, multi-buy, catalogue feature, display + discount, or bundle                      |
| Promo_Depth_Band                      | Discount depth grouping, such as 10-15%, 20-25%, 30%+, or No Promo                                                             |
| Promo_Objective                       | Commercial objective of the promotion, such as drive volume, defend share, support trial, clear stock, or increase basket size |
| Retailer_Support                      | Type of retailer or in-store support, such as catalogue, display, shelf price ticket, or bundle execution                      |
| Baseline_Units                        | Expected units sold without promotion                                                                                          |
| Actual_Units                          | Actual units sold during the week                                                                                              |
| Uplift_Units                          | Difference between actual units and baseline units                                                                             |
| Uplift_Pct                            | Uplift units divided by baseline units                                                                                         |
| Regular_Price                         | Standard selling price                                                                                                         |
| Promo_Price                           | Promotional selling price                                                                                                      |
| Discount_Pct                          | Discount percentage compared with regular price                                                                                |
| Unit_Cost                             | Cost per unit                                                                                                                  |
| Selling_Price                         | Actual selling price used for revenue and profit calculations                                                                  |
| Baseline_Revenue                      | Expected revenue without promotion                                                                                             |
| Actual_Revenue                        | Actual revenue during the analysis period                                                                                      |
| Incremental_Revenue_From_Uplift       | Revenue generated from incremental units sold above baseline                                                                   |
| Revenue_Impact_vs_Baseline            | Actual revenue minus baseline revenue                                                                                          |
| Baseline_Gross_Profit                 | Expected gross profit without promotion                                                                                        |
| Gross_Profit_Before_Promo_Cost        | Gross profit during the week before promotional cost                                                                           |
| Incremental_Gross_Profit_Before_Cost  | Promotional gross profit minus baseline gross profit                                                                           |
| Promo_Cost                            | Promotional investment or trade spend                                                                                          |
| Incremental_Profit_After_Promo_Cost   | Incremental gross profit after subtracting promotional cost                                                                    |
| Promo_ROI                             | Incremental profit after promotional cost divided by promotional cost                                                          |
| Baseline_Gross_Margin_Pct             | Gross margin percentage at regular price                                                                                       |
| Actual_Gross_Margin_Pct               | Gross margin percentage at actual selling price                                                                                |
| Margin_Impact_pp                      | Change in gross margin percentage points compared with baseline                                                                |
| Rate_of_Sale_Units_per_Store_per_Week | Actual units divided by store count                                                                                            |
| Cannibalisation_Rate_Estimate         | Estimated percentage of uplift potentially taken from other products in the same category                                      |
| Cannibalised_Units_Estimate           | Estimated cannibalised units                                                                                                   |
| Cannibalisation_Risk                  | Low, Medium, or High cannibalisation risk for promotional rows                                                                 |
| Recommendation                        | Commercial recommendation based on ROI, margin impact, uplift, and cannibalisation risk                                        |
| Sales_Action                          | Suggested next action for the sales or account team                                                                            |
| Buyer_Message                         | Short commercial message that could support buyer or account discussion                                                        |

---

## Recommendation Values

| Recommendation        | Business Meaning                                                                                  |
| --------------------- | ------------------------------------------------------------------------------------------------- |
| Repeat                | Promotion delivered strong ROI, positive incremental profit, and manageable cannibalisation risk  |
| Targeted repeat       | Promotion performed well but should be repeated selectively by product, account, or region        |
| Adjust depth/mechanic | Promotion generated volume response but profit was weakened by discount depth or promotional cost |
| Review                | Promotion had mixed performance and should be reviewed with additional commercial context         |
| Discontinue           | Promotion did not generate sufficient commercial return                                           |
| Baseline              | Non-promotional trading period                                                                    |

---

## Example Account-Manager-Facing Fields

The following fields are designed to make the dataset useful beyond technical analysis.

| Field                                 | Why It Matters                                                                          |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| Promo_Objective                       | Helps separate strategic promotions from purely volume-driven promotions                |
| Retailer_Support                      | Helps compare whether catalogue, display, shelf, or bundle support improved performance |
| Rate_of_Sale_Units_per_Store_per_Week | Helps compare regions and accounts with different store counts                          |
| Cannibalisation_Risk                  | Helps identify whether uplift may have shifted volume within the category               |
| Sales_Action                          | Converts analysis into a practical next step for the account or field team              |
| Buyer_Message                         | Translates the result into a short commercial message suitable for buyer discussion     |

---

## Notes

This dataset is synthetic and created for portfolio demonstration purposes.

It does not contain confidential, proprietary, or real company sales data.
