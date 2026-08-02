"""模型:训练、评估、保存、加载与预测。

核心逻辑为纯函数 + Pipeline,页面与离线脚本复用同一入口,保证结果一致。
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from banksys.config import (
    DEFAULT_MODEL_PATH,
    ID_COL,
    RANDOM_STATE,
    TARGET,
    VALIDATION_SPLIT,
)
from banksys.features import make_preprocessor

METRIC_KEYS = ("auc", "f1", "accuracy")


def train_model(
    X: pd.DataFrame,
    y: pd.Series,
    seed: int = RANDOM_STATE,
    n_estimators: int = 200,
) -> Pipeline:
    """训练「预处理 + 随机森林」管道,返回已拟合的 Pipeline。"""
    pipeline = Pipeline(
        steps=[
            ("prep", make_preprocessor()),
            (
                "clf",
                RandomForestClassifier(n_estimators=n_estimators, random_state=seed, n_jobs=-1),
            ),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def evaluate_model(pipeline: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict:
    """在给定数据上计算 AUC / F1 / 准确率。

    目标为二元类别 'yes'/'no';predict_proba 第二列对应 'yes'(类名排序后)。
    """
    y_true = np.asarray(y)
    proba = pipeline.predict_proba(X)[:, 1]
    pred = pipeline.predict(X)
    return {
        "auc": float(roc_auc_score(y_true, proba)),
        "f1": float(f1_score(y_true, pred, pos_label="yes")),
        "accuracy": float(accuracy_score(y_true, pred)),
    }


def train_and_evaluate(
    df: pd.DataFrame, seed: int = RANDOM_STATE
) -> tuple[Pipeline, dict, pd.DataFrame, pd.Series]:
    """切分训练/验证集 → 训练 → 评估,一步到位。

    返回 (pipeline, metrics, X_val, y_val),供训练脚本与测试使用。
    """
    X = df.drop(columns=[TARGET, ID_COL], errors="ignore")
    y = df[TARGET]
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=VALIDATION_SPLIT, random_state=seed, stratify=y
    )
    pipeline = train_model(X_train, y_train, seed=seed)
    metrics = evaluate_model(pipeline, X_val, y_val)
    return pipeline, metrics, X_val, y_val


def save_model(pipeline: Pipeline, path: str | Path = DEFAULT_MODEL_PATH) -> Path:
    """保存模型;自动创建父目录。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, path)
    return path


def load_model(path: str | Path = DEFAULT_MODEL_PATH) -> Pipeline:
    """加载模型;文件不存在时报清晰错误。"""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"模型文件不存在: {path}")
    return joblib.load(path)


def predict(pipeline: Pipeline, X: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """返回 (预测标签, 认购概率)。"""
    proba = pipeline.predict_proba(X)[:, 1]
    pred = pipeline.predict(X)
    return pred, proba


def meets_gate(metrics: dict, min_auc: float) -> bool:
    """验证集 AUC 是否达到门槛。"""
    return metrics["auc"] >= min_auc
