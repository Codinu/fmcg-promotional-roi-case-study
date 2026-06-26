from __future__ import annotations

import pandas as pd


def display_percent_columns(
    df: pd.DataFrame,
    columns: list[str],
    multiplier: float = 100.0,
) -> pd.DataFrame:
    output = df.copy()

    for column in columns:
        if column in output.columns:
            output[column] = output[column] * multiplier

    return output
