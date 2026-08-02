"""特征工程:统一预处理管道,训练、预测、页面共用同一份。"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from banksys.config import MODEL_CATEGORICAL_FEATURES, MODEL_NUMERIC_FEATURES


def make_preprocessor(
    numeric_features: list[str] | None = None,
    categorical_features: list[str] | None = None,
) -> ColumnTransformer:
    """构建「数值标准化 + 分类独热编码」预处理管道。

    默认使用建模特征(排除 duration);handle_unknown='ignore' 让预测时
    遇到训练中未见过的分类值归零而非抛异常,保证线上不因新取值崩溃。
    """
    numeric = numeric_features or MODEL_NUMERIC_FEATURES
    categorical = categorical_features or MODEL_CATEGORICAL_FEATURES
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical,
            ),
        ]
    )
