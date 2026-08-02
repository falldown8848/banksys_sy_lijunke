"""features 模块单元测试。"""

import numpy as np
import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer

from banksys.config import CATEGORICAL_FEATURES, FEATURES, NUMERIC_FEATURES
from banksys.features import make_preprocessor


@pytest.fixture
def sample_df() -> pd.DataFrame:
    rng = np.random.default_rng(7)
    data = {col: rng.normal(size=50) for col in NUMERIC_FEATURES}
    data.update({col: rng.choice(["a", "b", "c"], size=50) for col in CATEGORICAL_FEATURES})
    return pd.DataFrame(data)


def test_make_preprocessor_returns_column_transformer():
    prep = make_preprocessor()
    assert isinstance(prep, ColumnTransformer)


def test_preprocessor_fit_transform_produces_numeric_output(sample_df):
    # Arrange
    prep = make_preprocessor()
    X = sample_df[FEATURES]

    # Act
    out = prep.fit_transform(X)

    # Assert
    assert out.shape[0] == len(X)
    assert np.issubdtype(out.dtype, np.number)


def test_preprocessor_ignores_unseen_category(sample_df):
    # Arrange:训练后,预测出现新分类值不应崩溃
    prep = make_preprocessor()
    prep.fit(sample_df[FEATURES])
    unseen = sample_df.copy()
    unseen["job"] = "brand_new_job"

    # Act
    out = prep.transform(unseen[FEATURES])

    # Assert
    assert out.shape[0] == len(unseen)
