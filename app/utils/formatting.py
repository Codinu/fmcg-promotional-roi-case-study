from __future__ import annotations

import pandas as pd


def format_currency(value: float | int | None, decimals: int = 0) -> str:
    if value is None or pd.isna(value):
        return "$0"

    abs_value = abs(value)
    sign = "-" if value < 0 else ""

    if abs_value >= 1_000_000:
        return f"{sign}${abs_value / 1_000_000:.{decimals}f}M"
    if abs_value >= 1_000:
        return f"{sign}${abs_value / 1_000:.{decimals}f}K"

    return f"{sign}${abs_value:,.{decimals}f}"


def format_number(value: float | int | None, decimals: int = 0) -> str:
    if value is None or pd.isna(value):
        return "0"

    abs_value = abs(value)
    sign = "-" if value < 0 else ""

    if abs_value >= 1_000_000:
        return f"{sign}{abs_value / 1_000_000:.{decimals}f}M"
    if abs_value >= 1_000:
        return f"{sign}{abs_value / 1_000:.{decimals}f}K"

    return f"{sign}{abs_value:,.{decimals}f}"


def format_percent(value: float | int | None, decimals: int = 1) -> str:
    if value is None or pd.isna(value):
        return "0.0%"
    return f"{value * 100:.{decimals}f}%"


def format_pp(value: float | int | None, decimals: int = 1) -> str:
    if value is None or pd.isna(value):
        return "0.0 pp"
    return f"{value:.{decimals}f} pp"