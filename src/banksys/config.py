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

# ---- 建模特征 ----
# 排除 duration(通话时长):在线预测时刻未知,且与目标强关联存在泄漏风险。
# 实验记录见 PROGRESS ADR:含 duration AUC=0.89 vs 不含 AUC=0.82,均过 0.75 门槛。
EXCLUDED_FEATURES = ["duration"]
MODEL_NUMERIC_FEATURES = [f for f in NUMERIC_FEATURES if f not in EXCLUDED_FEATURES]
MODEL_CATEGORICAL_FEATURES = [f for f in CATEGORICAL_FEATURES if f not in EXCLUDED_FEATURES]
MODEL_FEATURES = MODEL_NUMERIC_FEATURES + MODEL_CATEGORICAL_FEATURES

# ---- 模型训练相关 ----
DEFAULT_MODEL_PATH = MODELS_DIR / "pipeline.joblib"
RANDOM_STATE = 42
VALIDATION_SPLIT = 0.2
MIN_AUC = 0.75
