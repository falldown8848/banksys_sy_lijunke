"""项目配置:路径、特征清单与常量。

特征清单与数据列保持一致,训练、预测、页面共用同一份定义,避免多处漂移。
"""

from pathlib import Path

# ---- 路径(以本文件位置推算,兼容源码目录与容器内 /app 布局) ----
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
TRAIN_PATH = DATA_DIR / "train.csv"
TEST_PATH = DATA_DIR / "test.csv"

# ---- 目标与标识列 ----
TARGET = "subscribe"
ID_COL = "id"

# ---- 特征清单 ----
NUMERIC_FEATURES = [
    "age",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
]

CATEGORICAL_FEATURES = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
