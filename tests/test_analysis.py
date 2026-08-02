"""analysis 模块单元测试:纯函数,小样本合成数据。"""

import numpy as np
import pandas as pd
import pytest

from banksys.analysis import (
    category_counts,
    missing_counts,
    numeric_summary,
    subscription_rate_by,
    target_distribution,
)
from banksys.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, TARGET


@pytest.fixture
def sample_df() -> pd.DataFrame:
    rng = np.random.default_rng(1)
    n = 60
    data = {col: rng.normal(size=n) for col in NUMERIC_FEATURES}
    data.update({col: rng.choice(["a", "b"], size=n) for col in CATEGORICAL_FEATURES})
    data[TARGET] = rng.choice(["yes", "no"], size=n, p=[0.4, 0.6])
    df = pd.DataFrame(data)
    df.loc[0, "age"] = np.nan  # 人为制造一个缺失值
    return df


def test_numeric_summary_has_expected_rows(sample_df):
    # Act
    summary = numeric_summary(sample_df, ["age", "campaign"])

    # Assert
    assert set(summary.index) == {"age", "campaign"}
    assert {"mean", "min", "max", "count"} <= set(summary.columns)


def test_numeric_summary_reports_nan_count(sample_df):
    # Act
    summary = numeric_summary(sample_df, ["age"])

    # Assert:60 行,1 个 NaN,count=59
    assert summary.loc["age", "count"] == 59


def test_category_counts_sorted_desc(sample_df):
    # Act
    counts = category_counts(sample_df, "job")

    # Assert
    assert list(counts.columns) == ["job", "count"]
    assert counts["count"].is_monotonic_decreasing
    assert counts["count"].sum() == len(sample_df)


def test_subscription_rate_by_in_range(sample_df):
    # Act
    table = subscription_rate_by(sample_df, "job")

    # Assert
    assert set(table.columns) == {"job", "count", "subscribe_rate"}
    assert table["subscribe_rate"].between(0, 1).all()
    assert table["count"].sum() == len(sample_df)


def test_target_distribution(sample_df):
    # Act
    dist = target_distribution(sample_df)

    # Assert
    assert set(dist[TARGET]) == {"yes", "no"}
    assert dist["count"].sum() == len(sample_df)


def test_missing_counts_detects_nan(sample_df):
    # Act
    missing = missing_counts(sample_df)

    # Assert
    assert missing["age"] == 1
    assert missing["campaign"] == 0
