from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def empty_figure(message: str = "No data available") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16),
    )
    fig.update_layout(
        height=380,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def apply_standard_layout(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        height=height,
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=40),
        legend_title_text="",
    )
    return fig


def bar_profit_by_recommendation(summary_df: pd.DataFrame) -> go.Figure:
    if summary_df.empty:
        return empty_figure()

    fig = px.bar(
        summary_df.sort_values("Incremental_Profit", ascending=False),
        x="Recommendation",
        y="Incremental_Profit",
        text_auto=".2s",
        title="Profit Impact by Recommendation",
    )
    fig.update_layout(
        xaxis_title="Recommendation",
        yaxis_title="Incremental Profit",
    )
    return apply_standard_layout(fig)


def bar_roi_by_promo_type(summary_df: pd.DataFrame) -> go.Figure:
    if summary_df.empty:
        return empty_figure()

    fig = px.bar(
        summary_df.sort_values("Promo_ROI", ascending=False),
        x="Promo_Type",
        y="Promo_ROI",
        text_auto=".1%",
        title="Promo ROI by Mechanic",
    )
    fig.update_layout(
        xaxis_title="Promo Mechanic",
        yaxis_title="Promo ROI",
        yaxis_tickformat=".0%",
    )
    return apply_standard_layout(fig)


def bar_event_count_by_recommendation(summary_df: pd.DataFrame) -> go.Figure:
    if summary_df.empty:
        return empty_figure()

    fig = px.bar(
        summary_df.sort_values("Promo_Events", ascending=False),
        x="Recommendation",
        y="Promo_Events",
        text_auto=True,
        title="Promo Event Count by Recommendation",
    )
    fig.update_layout(
        xaxis_title="Recommendation",
        yaxis_title="Promo Events",
    )
    return apply_standard_layout(fig)


def campaign_uplift_roi_scatter(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    plot_df = campaigns.copy()
    plot_df["Bubble_Size"] = plot_df["Incremental_Profit"].abs().clip(lower=50)

    fig = px.scatter(
        plot_df,
        x="Uplift_Pct",
        y="Promo_ROI",
        size="Bubble_Size",
        color="Recommendation",
        hover_data=[
            "Campaign_ID",
            "Product",
            "Category",
            "Region",
            "Account",
            "Promo_Type",
            "Incremental_Profit",
            "Promo_Cost",
        ],
        title="Uplift % vs Promo ROI by Campaign",
    )
    fig.add_hline(y=0, line_dash="dash")
    fig.update_layout(
        xaxis_title="Uplift %",
        yaxis_title="Promo ROI",
        xaxis_tickformat=".0%",
        yaxis_tickformat=".0%",
    )
    return apply_standard_layout(fig, height=520)


def discount_vs_uplift_scatter(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    plot_df = campaigns.copy()
    plot_df["Bubble_Size"] = plot_df["Incremental_Profit"].abs().clip(lower=50)

    fig = px.scatter(
        plot_df,
        x="Discount_Pct",
        y="Uplift_Pct",
        size="Bubble_Size",
        color="Promo_Type",
        hover_data=[
            "Campaign_ID",
            "Product",
            "Category",
            "Region",
            "Account",
            "Promo_ROI",
            "Incremental_Profit",
            "Margin_Impact_pp",
        ],
        title="Discount Depth vs Uplift %",
    )
    fig.update_layout(
        xaxis_title="Average Discount %",
        yaxis_title="Average Uplift %",
        xaxis_tickformat=".0%",
        yaxis_tickformat=".0%",
    )
    return apply_standard_layout(fig, height=480)


def discount_vs_margin_scatter(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    plot_df = campaigns.copy()
    plot_df["Bubble_Size"] = plot_df["Promo_Cost"].abs().clip(lower=50)

    fig = px.scatter(
        plot_df,
        x="Discount_Pct",
        y="Margin_Impact_pp",
        size="Bubble_Size",
        color="Promo_Type",
        hover_data=[
            "Campaign_ID",
            "Product",
            "Category",
            "Region",
            "Account",
            "Promo_ROI",
            "Incremental_Profit",
            "Uplift_Pct",
        ],
        title="Discount Depth vs Margin Impact",
    )
    fig.add_hline(y=0, line_dash="dash")
    fig.update_layout(
        xaxis_title="Average Discount %",
        yaxis_title="Margin Impact pp",
        xaxis_tickformat=".0%",
    )
    return apply_standard_layout(fig, height=480)


def margin_pressure_by_promo_type(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    summary = (
        campaigns.groupby("Promo_Type", dropna=False)
        .agg(
            Avg_Margin_Impact_pp=("Margin_Impact_pp", "mean"),
            Campaigns=("Campaign_ID", "count"),
        )
        .reset_index()
        .sort_values("Avg_Margin_Impact_pp")
    )

    fig = px.bar(
        summary,
        x="Promo_Type",
        y="Avg_Margin_Impact_pp",
        text_auto=".1f",
        title="Margin Pressure by Promo Mechanic",
    )
    fig.add_hline(y=0, line_dash="dash")
    fig.update_layout(
        xaxis_title="Promo Mechanic",
        yaxis_title="Average Margin Impact pp",
    )
    return apply_standard_layout(fig, height=420)


def incremental_profit_by_category(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    summary = (
        campaigns.groupby("Category", dropna=False)
        .agg(Incremental_Profit=("Incremental_Profit", "sum"))
        .reset_index()
        .sort_values("Incremental_Profit", ascending=False)
    )

    fig = px.bar(
        summary,
        x="Category",
        y="Incremental_Profit",
        text_auto=".2s",
        title="Incremental Profit by Category",
    )
    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Incremental Profit",
    )
    return apply_standard_layout(fig, height=420)


def promo_roi_by_region(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    summary = (
        campaigns.groupby("Region", dropna=False)
        .agg(
            Incremental_Profit=("Incremental_Profit", "sum"),
            Promo_Cost=("Promo_Cost", "sum"),
        )
        .reset_index()
    )
    summary["Promo_ROI"] = summary["Incremental_Profit"] / summary["Promo_Cost"].replace(0, pd.NA)

    fig = px.bar(
        summary.sort_values("Promo_ROI", ascending=False),
        x="Region",
        y="Promo_ROI",
        text_auto=".1%",
        title="Promo ROI by Region",
    )
    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Promo ROI",
        yaxis_tickformat=".0%",
    )
    return apply_standard_layout(fig, height=420)


def rate_of_sale_by_account(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    summary = (
        campaigns.groupby("Account", dropna=False)
        .agg(Rate_of_Sale=("Rate_of_Sale", "mean"))
        .reset_index()
        .sort_values("Rate_of_Sale", ascending=False)
    )

    fig = px.bar(
        summary,
        x="Account",
        y="Rate_of_Sale",
        text_auto=".1f",
        title="Rate of Sale by Account",
    )
    fig.update_layout(
        xaxis_title="Account",
        yaxis_title="Units per Store per Week",
    )
    return apply_standard_layout(fig, height=420)


def category_region_profit_heatmap(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    matrix = (
        campaigns.groupby(["Category", "Region"], dropna=False)
        .agg(Incremental_Profit=("Incremental_Profit", "sum"))
        .reset_index()
    )

    pivot = matrix.pivot(
        index="Category",
        columns="Region",
        values="Incremental_Profit",
    ).fillna(0)

    fig = px.imshow(
        pivot,
        text_auto=".2s",
        aspect="auto",
        title="Category x Region Profit Heatmap",
        labels=dict(x="Region", y="Category", color="Incremental Profit"),
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=40),
        template="plotly_white",
        height=420,
    )
    return fig

def cannibalised_units_by_category(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    summary = (
        campaigns.groupby("Category", dropna=False)
        .agg(Cannibalised_Units=("Cannibalised_Units", "sum"))
        .reset_index()
        .sort_values("Cannibalised_Units", ascending=False)
    )

    fig = px.bar(
        summary,
        x="Category",
        y="Cannibalised_Units",
        text_auto=".2s",
        title="Estimated Cannibalised Units by Category",
    )
    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Estimated Cannibalised Units",
    )
    return apply_standard_layout(fig, height=420)


def promo_events_by_cannibalisation_risk(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    summary = (
        campaigns.groupby("Cannibalisation_Risk", dropna=False)
        .agg(Promo_Events=("Campaign_ID", "count"))
        .reset_index()
    )

    risk_order = ["Low", "Medium", "High"]
    summary["Risk_Order"] = summary["Cannibalisation_Risk"].map(
        {risk: idx for idx, risk in enumerate(risk_order)}
    )
    summary = summary.sort_values("Risk_Order")

    fig = px.bar(
        summary,
        x="Cannibalisation_Risk",
        y="Promo_Events",
        text_auto=True,
        title="Promotional Events by Cannibalisation Risk",
    )
    fig.update_layout(
        xaxis_title="Cannibalisation Risk",
        yaxis_title="Promo Events",
    )
    return apply_standard_layout(fig, height=420)


def uplift_vs_cannibalisation_scatter(campaigns: pd.DataFrame) -> go.Figure:
    if campaigns.empty:
        return empty_figure()

    plot_df = campaigns.copy()
    plot_df["Bubble_Size"] = plot_df["Incremental_Profit"].abs().clip(lower=50)

    fig = px.scatter(
        plot_df,
        x="Uplift_Units",
        y="Cannibalisation_Rate",
        size="Bubble_Size",
        color="Recommendation",
        hover_data=[
            "Campaign_ID",
            "Product",
            "Category",
            "Region",
            "Account",
            "Promo_Type",
            "Promo_ROI",
            "Incremental_Profit",
            "Cannibalised_Units",
            "Cannibalisation_Risk",
        ],
        title="Uplift Units vs Cannibalisation Risk",
    )
    fig.update_layout(
        xaxis_title="Uplift Units",
        yaxis_title="Average Cannibalisation Rate",
        yaxis_tickformat=".0%",
    )
    return apply_standard_layout(fig, height=480)
