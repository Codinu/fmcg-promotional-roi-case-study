from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.filters import apply_filters, render_sidebar_filters
from app.utils.charts import (
    classification_probability_histogram,
    confusion_matrix_heatmap,
    feature_importance_bar,
    regression_actual_vs_predicted,
    residual_histogram,
)
from app.utils.data_loader import load_data
from app.utils.formatting import format_number, format_percent
from app.utils.modelling import (
    run_baseline_regression,
    run_positive_roi_classifier,
)


st.set_page_config(
    page_title="Data Science Lab | FMCG Promo ROI",
    page_icon="🧪",
    layout="wide",
)

st.title("Data Science Lab")
st.caption(
    "Python-based modelling demos for baseline estimation and positive ROI prediction."
)

st.warning(
    "Synthetic data caveat: these models are demonstration only. "
    "They show how historical promotion data could support commercial analytics, "
    "not production forecasting."
)

try:
    df = load_data()
except Exception as exc:
    st.error(f"Failed to load dataset: {exc}")
    st.stop()

filters = render_sidebar_filters(df)
filtered_df = apply_filters(df, filters)

if filtered_df.empty:
    st.warning("No rows match the selected filters. Please adjust the sidebar filters.")
    st.stop()


@st.cache_data(show_spinner="Training regression model...")
def cached_regression(data, model_name: str, target: str):
    return run_baseline_regression(data, model_name=model_name, target=target)


@st.cache_data(show_spinner="Training classification model...")
def cached_classifier(data, model_name: str):
    return run_positive_roi_classifier(data, model_name=model_name)


tab_regression, tab_classification = st.tabs(
    [
        "Baseline Modelling Demo",
        "Positive ROI Classification Demo",
    ]
)

with tab_regression:
    st.subheader("Baseline Modelling Demo")

    st.markdown(
        """
In real promotional analytics, baseline sales are often estimated from historical trading data.  
This demo shows how a regression model could be used to estimate expected units before measuring uplift.

The current dataset is synthetic, so the purpose is to demonstrate modelling workflow rather than claim production accuracy.
"""
    )

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        regression_model = st.selectbox(
            "Regression model",
            ["Random Forest", "Ridge Regression"],
            key="regression_model",
        )

    with col2:
        regression_target = st.selectbox(
            "Prediction target",
            ["Baseline_Units", "Actual_Units"],
            key="regression_target",
        )

    with col3:
        st.info(
            "Features include product, category, brand, region, account, week, quarter, promo type, "
            "discount depth, price and store count."
        )

    run_regression = st.checkbox(
        "Run regression demo",
        value=False,
        key="run_regression_demo",
    )

    if run_regression:
        try:
            result = cached_regression(
                filtered_df,
                regression_model,
                regression_target,
            )
        except Exception as exc:
            st.error(f"Regression demo failed: {exc}")
            st.stop()

        metric_cols = st.columns(3)
        metric_cols[0].metric("MAE", format_number(result.mae, decimals=1))
        metric_cols[1].metric("RMSE", format_number(result.rmse, decimals=1))
        metric_cols[2].metric("R2", f"{result.r2:.3f}")

        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                regression_actual_vs_predicted(result.predictions),
                use_container_width=True,
            )

        with right:
            st.plotly_chart(
                residual_histogram(result.predictions),
                use_container_width=True,
            )

        st.plotly_chart(
            feature_importance_bar(
                result.feature_importance,
                title=f"{result.model_name} Feature Importance",
            ),
            use_container_width=True,
        )

        with st.expander("Show regression prediction sample"):
            st.dataframe(
                result.predictions.head(50),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.info("Tick 'Run regression demo' to train and evaluate the regression model.")


with tab_classification:
    st.subheader("Positive ROI Classification Demo")

    st.markdown(
        """
This demo predicts whether a promotion is likely to generate positive ROI.

Target definition:

`Positive_ROI = Promo_ROI > 0`

This is useful as a prioritisation concept: historical campaign data could help account teams 
screen future promotional proposals before committing trade spend.
"""
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        classifier_model = st.selectbox(
            "Classification model",
            ["Random Forest", "Logistic Regression"],
            key="classifier_model",
        )

    with col2:
        st.info(
            "This demo uses promotional rows only. Features include product, category, brand, region, "
            "account, week, quarter, promo type, discount depth, price and store count."
        )

    run_classifier = st.checkbox(
        "Run classification demo",
        value=False,
        key="run_classification_demo",
    )

    if run_classifier:
        try:
            result = cached_classifier(filtered_df, classifier_model)
        except Exception as exc:
            st.error(f"Classification demo failed: {exc}")
            st.stop()

        metric_cols = st.columns(5)
        metric_cols[0].metric("Accuracy", format_percent(result.accuracy))
        metric_cols[1].metric("Precision", format_percent(result.precision))
        metric_cols[2].metric("Recall", format_percent(result.recall))
        metric_cols[3].metric("F1", format_percent(result.f1))
        metric_cols[4].metric(
            "ROC-AUC",
            "N/A" if result.roc_auc is None else f"{result.roc_auc:.3f}",
        )

        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                confusion_matrix_heatmap(result.confusion),
                use_container_width=True,
            )

        with right:
            st.plotly_chart(
                classification_probability_histogram(result.predictions),
                use_container_width=True,
            )

        st.plotly_chart(
            feature_importance_bar(
                result.feature_importance,
                title=f"{result.model_name} Feature Importance",
            ),
            use_container_width=True,
        )

        with st.expander("Show classification prediction sample"):
            st.dataframe(
                result.predictions.head(50),
                use_container_width=True,
                hide_index=True,
            )

        st.warning(
            "Model limitation: this is trained on synthetic promotional data. "
            "In a real business setting, predictions should be validated against future campaign outcomes "
            "and reviewed with commercial stakeholders."
        )
    else:
        st.info("Tick 'Run classification demo' to train and evaluate the classification model.")
