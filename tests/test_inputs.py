"""inputs 模块单元测试。"""

from banksys.config import MODEL_NUMERIC_FEATURES
from banksys.inputs import (
    NUMERIC_INPUT_SPEC,
    REQUIRED_NUMERIC_FIELDS,
    validate_numeric_inputs,
)


def test_spec_covers_all_model_numeric_features():
    # Assert:输入控件定义必须覆盖所有建模数值字段,防止页面漏字段
    assert set(REQUIRED_NUMERIC_FIELDS) == set(MODEL_NUMERIC_FEATURES)


def test_validate_passes_in_range():
    # Arrange / Act
    inputs = {name: spec["default"] for name, spec in NUMERIC_INPUT_SPEC.items()}

    # Assert
    assert validate_numeric_inputs(inputs) == []


def test_validate_flags_out_of_range():
    # Arrange:age 超上限,campaign 低于下限,previous 合法
    inputs = {"age": 150, "campaign": 0, "previous": 3}

    # Act
    errors = validate_numeric_inputs(inputs)

    # Assert
    assert len(errors) == 2
    assert any("age" in error for error in errors)
    assert any("campaign" in error for error in errors)


def test_validate_ignores_unknown_field():
    assert validate_numeric_inputs({"not_a_feature": -999}) == []
