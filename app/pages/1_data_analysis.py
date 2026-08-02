"""数据分析交互页(US-2)。

数据加载失败时给出明确错误提示,不崩溃;图表随交互控件即时更新。
"""

import plotly.express as px
import streamlit as st

from banksys.analysis import (
    category_counts,
    numeric_summary,
    subscription_rate_by,
    target_distribution,
)
from banksys.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, TARGET
from banksys.data import load_train

st.set_page_config(page_title="数据分析", page_icon="📊", layout="wide")
st.title("📊 数据分析")

try:
    df = load_train()
except Exception as exc:  # noqa: BLE001 — 页面边界,统一展示错误
    st.error(f"数据加载失败:{exc}")
    st.stop()

# ---- 交互筛选:年龄范围 ----
age_min, age_max = int(df["age"].min()), int(df["age"].max())
age_lo, age_hi = st.sidebar.slider(
    "年龄范围", min_value=age_min, max_value=age_max, value=(age_min, age_max)
)
df = df[df["age"].between(age_lo, age_hi)]
st.sidebar.caption(f"筛选后样本数:{len(df):,}")

# ---- 数据概览 ----
st.header("数据概览")
row = st.columns(4)
row[0].metric("样本数", f"{len(df):,}")
row[1].metric("字段数", f"{df.shape[1]}")
row[2].metric("缺失值", f"{int(df.isna().sum().sum()):,}")
row[3].metric("重复行", f"{int(df.duplicated().sum()):,}")
with st.expander("查看原始数据(前 1000 行)"):
    st.dataframe(df.head(1000), width="stretch")

# ---- 目标分布 ----
st.subheader(f"目标分布:是否认购(按年龄 {age_lo}–{age_hi})")
dist = target_distribution(df)
fig_target = px.bar(
    dist,
    x=TARGET,
    y="count",
    color=TARGET,
    text="count",
    color_discrete_map={"yes": "#2E86AB", "no": "#A2D6F9"},
    labels={"count": "样本数"},
)
fig_target.update_layout(showlegend=False, height=360)
st.plotly_chart(fig_target, width="stretch")

# ---- 数值字段分析 ----
st.header("数值字段分析")
num_col = st.selectbox("选择数值字段查看分布与统计", NUMERIC_FEATURES)
summary = numeric_summary(df, [num_col])
st.dataframe(summary.round(2), width="stretch")
fig_hist = px.histogram(df, x=num_col, nbins=40, color_discrete_sequence=["#2E86AB"])
fig_hist.update_layout(height=360, bargap=0.02, yaxis_title="样本数")
st.plotly_chart(fig_hist, width="stretch")

st.subheader("数值字段相关性")
corr = df[NUMERIC_FEATURES].corr()
fig_corr = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    aspect="auto",
)
fig_corr.update_layout(height=560)
st.plotly_chart(fig_corr, width="stretch")

# ---- 分类字段分析 ----
st.header("分类字段分析")
cat_col = st.selectbox("选择分类字段查看分布与认购率", CATEGORICAL_FEATURES)
counts = category_counts(df, cat_col)
rate = subscription_rate_by(df, cat_col)

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"**{cat_col} 取值分布**")
    fig_bar = px.bar(counts, x=cat_col, y="count", color=cat_col, text="count")
    fig_bar.update_layout(showlegend=False, height=380, yaxis_title="样本数")
    st.plotly_chart(fig_bar, width="stretch")
with c2:
    st.markdown(f"**{cat_col} 各取值认购率**")
    fig_rate = px.bar(
        rate,
        x=cat_col,
        y="subscribe_rate",
        color="subscribe_rate",
        text=rate["subscribe_rate"].map(lambda v: f"{v:.1%}"),
        color_continuous_scale="Blues",
    )
    fig_rate.update_layout(
        showlegend=False, height=380, yaxis_title="认购率", yaxis_tickformat="0%"
    )
    st.plotly_chart(fig_rate, width="stretch")
