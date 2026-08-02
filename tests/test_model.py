"""model 模块单元测试:小样本合成数据,保证快速稳定(03 §3)。"""

import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from banksys.config import CATEGORICAL_FEATURES, FEATURES, NUMERIC_FEATURES, TARGET
from banksys.model import (
    evaluate_model,
    load_model,
    meets_gate,
    predict,
    save_model,
    train_and_evaluate,
    train_model,
)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n = 160
    data = {col: rng.normal(size=n) for col in NUMERIC_FEATURES}
    data.update({col: rng.choice(["a", "b", "c"], size=n) for col in CATEGORICAL_FEATURES})
    data[TARGET] = rng.choice(["yes", "no"], size=n, p=[0.3, 0.7])
    return pd.DataFrame(data)


def test_train_model_returns_pipeline(sample_df):
    # Act
    pipeline = train_model(sample_df[FEATURES], sample_df[TARGET], n_estimators=20)

    # Assert
    assert isinstance(pipeline, Pipeline)


def test_evaluate_model_metrics_in_range(sample_df):
    # Arrange
    pipeline = train_model(sample_df[FEATURES], sample_df[TARGET], n_estimators=20)

    # Act
    metrics = evaluate_model(pipeline, sample_df[FEATURES], sample_df[TARGET])

    # Assert
    for key in ("auc", "f1", "accuracy"):
        assert 0.0 <= metrics[key] <= 1.0


def test_predict_returns_labels_and_probabilities(sample_df):
    # Arrange
    pipeline = train_model(sample_df[FEATURES], sample_df[TARGET], n_estimators=20)
    X_small = sample_df[FEATURES].head(5)

    # Act
    pred, proba = predict(pipeline, X_small)

    # Assert
    assert pred.shape == (5,)
    assert proba.shape == (5,)
    assert set(pred) <= {"yes", "no"}
    assert bool((proba >= 0).all() and (proba <= 1).all())


def test_save_and_load_roundtrip(tmp_path, sample_df):
    # Arrange
    pipeline = train_model(sample_df[FEATURES], sample_df[TARGET], n_estimators=20)
    path = tmp_path / "pipeline.joblib"

    # Act
    save_model(pipeline, path)
    loaded = load_model(path)

    # Assert:加载后的模型与原始模型预测一致
    pred_original, _ = predict(pipeline, sample_df[FEATURES].head(3))
    pred_loaded, _ = predict(loaded, sample_df[FEATURES].head(3))
    assert (pred_original == pred_loaded).all()


def test_load_model_missing_raises():
    with pytest.raises(FileNotFoundError, match="模型文件不存在"):
        load_model("D:/no_such_model.joblib")


def test_train_and_evaluate_returns_metrics(sample_df):
    # Act
    pipeline, metrics, x_val, y_val = train_and_evaluate(sample_df)

    # Assert
    assert set(metrics) == {"auc", "f1", "accuracy"}
    assert len(x_val) == len(y_val) > 0
    assert pipeline is not None


def test_meets_gate_boundaries():
    assert meets_gate({"auc": 0.80}, 0.75) is True
    assert meets_gate({"auc": 0.75}, 0.75) is True
    assert meets_gate({"auc": 0.74}, 0.75) is False
