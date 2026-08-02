"""在线预测页(US-4):点选/输入客户特征,预测是否认购定期存款。

分类字段下拉点选,数值字段数字输入;提交后复用训练管道预测,保证与
离线训练结果一致。模型缺失或输入非法时给出明确提示,不崩溃。
"""

import streamlit as st

from banksys.config import DEFAULT_MODEL_PATH
from banksys.inputs import NUMERIC_INPUT_SPEC, validate_numeric_inputs
from banksys.model import (
    get_categorical_options,
    load_model,
    predict_from_inputs,
)

st.set_page_config(page_title="在线预测", page_icon="🔮", layout="wide")
st.title("🔮 在线预测:是否认购定期存款")

try:
    pipeline = load_model()
except FileNotFoundError:
    st.warning(
        "⚠️ 模型未就绪。请先在项目目录运行 `python scripts/train.py` 生成模型,"
        f"产物应位于 `{DEFAULT_MODEL_PATH}`,生成后刷新本页。"
    )
    st.stop()

options = get_categorical_options(pipeline)
spec = NUMERIC_INPUT_SPEC

st.markdown("填写客户信息(分类字段点击选择,数值字段输入),提交后即时预测。")
with st.form("predict_form"):
    st.subheader("客户基本信息")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input(
            "年龄",
            min_value=spec["age"]["min"],
            max_value=spec["age"]["max"],
            value=spec["age"]["default"],
            step=1.0,
        )
        job = st.selectbox("职业", options["job"])
        marital = st.selectbox("婚姻状况", options["marital"])
        education = st.selectbox("教育程度", options["education"])
    with col2:
        default = st.selectbox("是否信用违约", options["default"])
        housing = st.selectbox("是否有房贷", options["housing"])
        loan = st.selectbox("是否有个人贷款", options["loan"])
        contact = st.selectbox("联系渠道", options["contact"])
    with col3:
        month = st.selectbox("联系月份", options["month"])
        day_of_week = st.selectbox("星期几", options["day_of_week"])
        poutcome = st.selectbox("上次活动结果", options["poutcome"])
        campaign = st.number_input(
            "本次联系次数",
            min_value=spec["campaign"]["min"],
            max_value=spec["campaign"]["max"],
            value=spec["campaign"]["default"],
            step=1.0,
        )

    st.subheader("历史与宏观指标")
    col4, col5, col6 = st.columns(3)
    with col4:
        pdays = st.number_input(
            "距上次联系天数(999 = 从未联系)",
            min_value=spec["pdays"]["min"],
            max_value=spec["pdays"]["max"],
            value=spec["pdays"]["default"],
            step=1.0,
        )
        previous = st.number_input(
            "此前联系次数",
            min_value=spec["previous"]["min"],
            max_value=spec["previous"]["max"],
            value=spec["previous"]["default"],
            step=1.0,
        )
    with col5:
        emp_var_rate = st.number_input(
            "就业变动率",
            min_value=spec["emp_var_rate"]["min"],
            max_value=spec["emp_var_rate"]["max"],
            value=spec["emp_var_rate"]["default"],
            step=0.1,
            format="%.1f",
        )
        cons_price_index = st.number_input(
            "消费价格指数",
            min_value=spec["cons_price_index"]["min"],
            max_value=spec["cons_price_index"]["max"],
            value=spec["cons_price_index"]["default"],
            step=0.1,
            format="%.1f",
        )
    with col6:
        cons_conf_index = st.number_input(
            "消费信心指数",
            min_value=spec["cons_conf_index"]["min"],
            max_value=spec["cons_conf_index"]["max"],
            value=spec["cons_conf_index"]["default"],
            step=0.1,
            format="%.1f",
        )
        lending_rate3m = st.number_input(
            "3 个月贷款利率",
            min_value=spec["lending_rate3m"]["min"],
            max_value=spec["lending_rate3m"]["max"],
            value=spec["lending_rate3m"]["default"],
            step=0.1,
            format="%.2f",
        )
        nr_employed = st.number_input(
            "就业人数(千)",
            min_value=spec["nr_employed"]["min"],
            max_value=spec["nr_employed"]["max"],
            value=spec["nr_employed"]["default"],
            step=1.0,
            format="%.1f",
        )

    submitted = st.form_submit_button("提交预测", type="primary")

if submitted:
    inputs = {
        "age": age,
        "job": job,
        "marital": marital,
        "education": education,
        "default": default,
        "housing": housing,
        "loan": loan,
        "contact": contact,
        "month": month,
        "day_of_week": day_of_week,
        "poutcome": poutcome,
        "campaign": campaign,
        "pdays": pdays,
        "previous": previous,
        "emp_var_rate": emp_var_rate,
        "cons_price_index": cons_price_index,
        "cons_conf_index": cons_conf_index,
        "lending_rate3m": lending_rate3m,
        "nr_employed": nr_employed,
    }

    errors = validate_numeric_inputs(inputs)
    if errors:
        for message in errors:
            st.error(message)
    else:
        pred, proba = predict_from_inputs(pipeline, inputs)
        if pred == "yes":
            st.success(f"🎯 预测结果:**认购** · 认购概率 **{proba:.1%}**")
        else:
            st.info(f"📌 预测结果:**不认购** · 认购概率 **{proba:.1%}**")
        st.caption("注:认购概率为模型给出 yes 的概率;≥50% 判为认购。")
        st.markdown("**本次输入摘要:**")
        st.json({key: str(value) for key, value in inputs.items()})
