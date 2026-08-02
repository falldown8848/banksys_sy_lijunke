"""用户输入定义与校验,供在线预测页复用(可单测)。"""

from banksys.config import MODEL_NUMERIC_FEATURES

# 数值字段输入控件范围(取数据集域值,仅用于 UI 提示与校验)
NUMERIC_INPUT_SPEC: dict[str, dict[str, float]] = {
    "age": {"min": 17.0, "max": 98.0, "default": 35.0},
    "campaign": {"min": 1.0, "max": 60.0, "default": 1.0},
    "pdays": {"min": 0.0, "max": 999.0, "default": 999.0},
    "previous": {"min": 0.0, "max": 275.0, "default": 0.0},
    "emp_var_rate": {"min": -3.4, "max": 1.4, "default": -1.8},
    "cons_price_index": {"min": 90.0, "max": 95.0, "default": 92.4},
    "cons_conf_index": {"min": -50.0, "max": -25.0, "default": -35.5},
    "lending_rate3m": {"min": 0.6, "max": 5.0, "default": 2.7},
    "nr_employed": {"min": 4900.0, "max": 5228.0, "default": 5100.0},
}

# 数值输入控件必须覆盖的建模数值字段(缺任一字段页面即报错,便于尽早发现漂移)
REQUIRED_NUMERIC_FIELDS: list[str] = MODEL_NUMERIC_FEATURES


def validate_numeric_inputs(inputs: dict[str, float]) -> list[str]:
    """校验数值输入是否在允许范围内,返回错误信息列表(空列表 = 通过)。"""
    errors: list[str] = []
    for name, value in inputs.items():
        spec = NUMERIC_INPUT_SPEC.get(name)
        if spec is None:
            continue
        if value < spec["min"] or value > spec["max"]:
            errors.append(f"{name} 超出范围 [{spec['min']:g}, {spec['max']:g}]: {value:g}")
    return errors
