"""data 模块单元测试:正常值、边界值、异常值。"""

import pandas as pd
import pytest

from banksys.config import FEATURES, TARGET, TEST_PATH, TRAIN_PATH
from banksys.data import load_csv, load_test, load_train


# ---- 正常值 ----
def test_load_train_has_all_expected_columns():
    # Arrange / Act
    df = load_train(TRAIN_PATH)

    # Assert
    assert set(FEATURES + [TARGET]) <= set(df.columns)
    assert not df.empty


def test_load_train_target_only_yes_no():
    # Arrange / Act
    df = load_train(TRAIN_PATH)

    # Assert
    assert set(df[TARGET].unique()) <= {"yes", "no"}


def test_load_test_has_features_but_no_target():
    # Arrange / Act
    df = load_test(TEST_PATH)

    # Assert
    assert set(FEATURES) <= set(df.columns)
    assert TARGET not in df.columns
    assert not df.empty


# ---- 异常值 ----
def test_load_csv_missing_file_raises():
    with pytest.raises(FileNotFoundError, match="数据文件不存在"):
        load_csv("D:/no_such_file_xyz.csv")


def test_load_train_missing_column_raises(tmp_path):
    # Arrange:只有一列,缺大部分必需列
    bad = pd.DataFrame({"age": [30, 45]})
    path = tmp_path / "bad.csv"
    bad.to_csv(path, index=False)

    # Act / Assert
    with pytest.raises(ValueError, match="缺少必需列"):
        load_train(path)


def test_load_train_invalid_target_raises(tmp_path):
    # Arrange:列齐全但目标取值非法
    df = pd.DataFrame({col: ["x"] * 2 for col in FEATURES})
    df[TARGET] = ["maybe", "sometimes"]
    path = tmp_path / "bad_target.csv"
    df.to_csv(path, index=False)

    # Act / Assert
    with pytest.raises(ValueError, match="非法取值"):
        load_train(path)
