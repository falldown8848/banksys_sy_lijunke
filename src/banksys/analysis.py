"""数据分析辅助纯函数:供数据分析页复用,便于单元测试。"""

import pandas as pd

from banksys.config import TARGET


def numeric_summary(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """数值字段统计摘要,行索引为字段名。"""
    return df[columns].describe().T


def category_counts(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """分类字段取值计数,按计数降序。返回 [column, count]。"""
    counts = df[column].value_counts()
    return pd.DataFrame({"count": counts}).reset_index().rename(columns={"index": column})


def subscription_rate_by(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """各分类取值的样本数与认购率(yes 占比),按样本数降序。"""
    encoded = (df[TARGET] == "yes").astype(int)
    rate = encoded.groupby(df[column]).mean().rename("subscribe_rate")
    counts = df[column].value_counts().rename("count")
    table = pd.DataFrame({"count": counts, "subscribe_rate": rate})
    return (
        table.reset_index().rename(columns={"index": column}).sort_values("count", ascending=False)
    )


def target_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """目标列取值计数。返回 [TARGET, count]。"""
    counts = df[TARGET].value_counts()
    return counts.rename("count").rename_axis(TARGET).reset_index()


def missing_counts(df: pd.DataFrame) -> pd.Series:
    """每列缺失值个数。"""
    return df.isna().sum()
