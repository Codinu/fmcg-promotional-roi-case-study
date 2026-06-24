# Data Dictionary

This dataset represents weekly FMCG promotional performance at product-account-region level. It is synthetic and designed for commercial analytics practice, including promotional ROI, uplift analysis, margin impact, rate of sale, and cannibalisation risk.

| Field | Description |
|---|---|
| Week_Start | Start date of the sales week |
| Week_Number | Week number in the analysis period |
| Campaign_ID | Unique campaign identifier for promotional events |
| Product | Product or SKU name |
| Category | FMCG product category |
| Brand | Product brand |
| Region | Australian sales region or state |
| Account | Retail account or customer group |
| Store_Count | Number of stores covered by the account-region combination |
| Promo_Flag | Indicates whether the product was on promotion |
| Promo_Type | Promotional mechanic, such as price discount, multi-buy, catalogue feature, display + discount, or bundle |
| Baseline_Units | Expected units sold without promotion |
| Actual_Units | Actual units sold |
| Uplift_Units | Difference between actual units and baseline units |
| Uplift_Pct | Uplift units divided by baseline units |
| Regular_Price | Standard selling price |
| Promo_Price | Promotional selling price |
| Discount_Pct | Discount percentage compared with regular price |
| Unit_Cost | Cost per unit |
| Selling_Price | Actual selling price used for revenue calculation |
| Baseline_Revenue | Expected revenue without promotion |
| Actual_Revenue | Actual revenue during the analysis period |
| Incremental_Revenue_From_Uplift | Revenue generated from incremental units |
| Revenue_Impact_vs_Baseline | Actual revenue minus baseline revenue |
| Baseline_Gross_Profit | Expected gross profit without promotion |
| Gross_Profit_Before_Promo_Cost | Gross profit before promotional cost |
| Incremental_Gross_Profit_Before_Cost | Promotional gross profit minus baseline gross profit |
| Promo_Cost | Promotional investment or trade spend |
| Incremental_Profit_After_Promo_Cost | Incremental gross profit after subtracting promo cost |
| Promo_ROI | Incremental profit after promo cost divided by promo cost |
| Baseline_Gross_Margin_Pct | Gross margin percentage at regular price |
| Actual_Gross_Margin_Pct | Gross margin percentage at selling price |
| Margin_Impact_pp | Change in gross margin percentage points |
| Rate_of_Sale_Units_per_Store_per_Week | Actual units divided by store count |
| Cannibalisation_Rate_Estimate | Estimated percentage of uplift potentially taken from other products in the same category |
| Cannibalised_Units_Estimate | Estimated cannibalised units |
| Cannibalisation_Risk | Low, Medium, or High cannibalisation risk |
| Recommendation | Commercial recommendation based on ROI, margin impact, uplift, and cannibalisation risk |
