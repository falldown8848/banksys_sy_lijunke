"""Streamlit 应用入口:项目概览 + 模型状态检查。

数据分析页与在线预测页位于 app/pages/。运行:
    streamlit run app/main.py --server.port 8888
"""

from pathlib import Path

import streamlit as st

from banksys.config import DEFAULT_MODEL_PATH

st.set_page_config(
    page_title="banksys 银行营销认购预测",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 银行营销认购预测系统")
st.caption("banksys_sy_lijunke · 数据分析 + 在线认购预测")

st.markdown("本项目基于银行营销公开数据(UCI Bank Marketing)构建,包含两个功能:")
col1, col2 = st.columns(2)
with col1:
    st.info("📊 **数据分析** — 客户数据概览、字段分布、特征与认购率关系(左侧菜单进入)")
with col2:
    st.info("🔮 **在线预测** — 点选客户特征,预测是否认购定期存款(左侧菜单进入)")

model_path = Path(DEFAULT_MODEL_PATH)
if model_path.exists():
    st.success(f"✅ 模型已就绪:`{model_path}`")
else:
    st.warning("⚠️ 模型未就绪,请先运行 `python scripts/train.py` 后再使用预测功能。")
