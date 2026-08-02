"""数据加载与校验。

仅依赖 pandas,不包含任何页面/UI 逻辑,便于单元测试(AAA 写法)。
"""

from pathlib import Path

import pandas as pd

from banksys.config import FEATURES, TARGET, TEST_PATH, TRAIN_PATH

VALID_TARGET_VALUES = {"yes", "no"}


def load_csv(path: str | Path) -> pd.DataFrame:
    """读取 CSV;文件不存在时报 FileNotFoundError。"""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"数据文件不存在: {path}")
    return pd.read_csv(path)


def load_train(path: str | Path = TRAIN_PATH) -> pd.DataFrame:
    """加载训练数据,校验必需列与目标取值。"""
    df = load_csv(path)
    _require_columns(df, FEATURES + [TARGET], Path(path))
    _validate_target(df, Path(path))
    return df


def load_test(path: str | Path = TEST_PATH) -> pd.DataFrame:
    """加载测试数据,校验必需特征列(不含目标列)。"""
    df = load_csv(path)
    _require_columns(df, FEATURES, Path(path))
    return df


def _require_columns(df: pd.DataFrame, required: list[str], path: Path) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{path} 缺少必需列: {missing}")


def _validate_target(df: pd.DataFrame, path: Path) -> None:
    bad = sorted(set(df[TARGET].dropna().unique()) - VALID_TARGET_VALUES)
    if bad:
        raise ValueError(f"{path} 目标列 {TARGET!r} 含非法取值: {bad}")
