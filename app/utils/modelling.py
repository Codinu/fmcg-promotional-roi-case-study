from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


CATEGORICAL_FEATURES = [
    "Product",
    "Category",
    "Brand",
    "Region",
    "Account",
    "Quarter",
    "Promo_Type",
]

NUMERIC_FEATURES = [
    "Week_Number",
    "Promo_Flag",
    "Discount_Pct",
    "Regular_Price",
    "Promo_Price",
    "Store_Count",
]


@dataclass
class RegressionResult:
    model_name: str
    mae: float
    rmse: float
    r2: float
    predictions: pd.DataFrame
    feature_importance: pd.DataFrame


@dataclass
class ClassificationResult:
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float | None
    confusion: np.ndarray
    predictions: pd.DataFrame
    feature_importance: pd.DataFrame


def _available_features(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    categorical = [col for col in CATEGORICAL_FEATURES if col in df.columns]
    numeric = [col for col in NUMERIC_FEATURES if col in df.columns]
    return categorical, numeric


def build_preprocessor(df: pd.DataFrame) -> ColumnTransformer:
    categorical, numeric = _available_features(df)

    return ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("numeric", StandardScaler(), numeric),
        ]
    )


def prepare_feature_matrix(df: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.Series]:
    categorical, numeric = _available_features(df)
    features = categorical + numeric

    missing = [col for col in features + [target] if col not in df.columns]
    if missing:
        raise ValueError("Missing required modelling columns: " + ", ".join(missing))

    modelling_df = df[features + [target]].dropna().copy()
    X = modelling_df[features]
    y = modelling_df[target]

    return X, y


def _get_feature_names(model: Pipeline, X: pd.DataFrame) -> list[str]:
    preprocessor = model.named_steps["preprocessor"]
    categorical, numeric = _available_features(X)

    try:
        encoded_names = (
            preprocessor.named_transformers_["categorical"]
            .get_feature_names_out(categorical)
            .tolist()
        )
    except Exception:
        encoded_names = categorical

    return encoded_names + numeric


def _linear_feature_importance(model: Pipeline, X: pd.DataFrame) -> pd.DataFrame:
    estimator = model.named_steps["model"]
    feature_names = _get_feature_names(model, X)
    coefs = np.ravel(estimator.coef_)

    return (
        pd.DataFrame({"Feature": feature_names, "Importance": np.abs(coefs)})
        .sort_values("Importance", ascending=False)
        .head(20)
    )


def _tree_feature_importance(model: Pipeline, X: pd.DataFrame) -> pd.DataFrame:
    estimator = model.named_steps["model"]
    feature_names = _get_feature_names(model, X)
    importances = estimator.feature_importances_

    return (
        pd.DataFrame({"Feature": feature_names, "Importance": importances})
        .sort_values("Importance", ascending=False)
        .head(20)
    )


def run_baseline_regression(
    df: pd.DataFrame,
    model_name: str = "Random Forest",
    target: str = "Baseline_Units",
) -> RegressionResult:
    X, y = prepare_feature_matrix(df, target)

    if len(X) < 100:
        raise ValueError("Not enough rows for regression demo after filtering.")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
    )

    if model_name == "Ridge Regression":
        estimator = Ridge(alpha=1.0)
    elif model_name == "Random Forest":
        estimator = RandomForestRegressor(
            n_estimators=120,
            max_depth=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        )
    else:
        raise ValueError(f"Unsupported regression model: {model_name}")

    model = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(df)),
            ("model", estimator),
        ]
    )

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    predictions = pd.DataFrame(
        {
            "Actual": y_test.to_numpy(),
            "Predicted": pred,
            "Residual": y_test.to_numpy() - pred,
        }
    )

    rmse = float(np.sqrt(mean_squared_error(y_test, pred)))

    if model_name == "Random Forest":
        importance = _tree_feature_importance(model, X)
    else:
        importance = _linear_feature_importance(model, X)

    return RegressionResult(
        model_name=model_name,
        mae=float(mean_absolute_error(y_test, pred)),
        rmse=rmse,
        r2=float(r2_score(y_test, pred)),
        predictions=predictions,
        feature_importance=importance,
    )


def run_positive_roi_classifier(
    df: pd.DataFrame,
    model_name: str = "Random Forest",
) -> ClassificationResult:
    promo_df = df[df["Promo_Flag"] == 1].copy()
    promo_df["Positive_ROI_Target"] = promo_df["Promo_ROI"] > 0

    X, y = prepare_feature_matrix(promo_df, "Positive_ROI_Target")

    if len(X) < 100:
        raise ValueError("Not enough promotional rows for classification demo after filtering.")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    if model_name == "Logistic Regression":
        estimator = LogisticRegression(max_iter=1000)
    elif model_name == "Random Forest":
        estimator = RandomForestClassifier(
            n_estimators=120,
            max_depth=8,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        )
    else:
        raise ValueError(f"Unsupported classification model: {model_name}")

    model = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(promo_df)),
            ("model", estimator),
        ]
    )

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    if hasattr(model.named_steps["model"], "predict_proba"):
        proba = model.predict_proba(X_test)[:, 1]
        roc_auc = float(roc_auc_score(y_test, proba))
    else:
        proba = None
        roc_auc = None

    predictions = pd.DataFrame(
        {
            "Actual": y_test.to_numpy(),
            "Predicted": pred,
            "Positive_ROI_Probability": proba if proba is not None else np.nan,
        }
    )

    if model_name == "Random Forest":
        importance = _tree_feature_importance(model, X)
    else:
        importance = _linear_feature_importance(model, X)

    return ClassificationResult(
        model_name=model_name,
        accuracy=float(accuracy_score(y_test, pred)),
        precision=float(precision_score(y_test, pred, zero_division=0)),
        recall=float(recall_score(y_test, pred, zero_division=0)),
        f1=float(f1_score(y_test, pred, zero_division=0)),
        roc_auc=roc_auc,
        confusion=confusion_matrix(y_test, pred),
        predictions=predictions,
        feature_importance=importance,
    )
