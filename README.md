# banksys_sy_lijunke

基于银行营销数据的 Web 应用,包含两个核心功能:

1. **数据分析交互页面** — 数据概览、字段分布、特征与认购率关系。
2. **在线预测系统** — 离线训练二分类模型,网页点选输入客户特征,预测是否认购定期存款。

技术栈:Python 3.11 · Streamlit · scikit-learn · pytest · ruff · Docker(端口 8888)。
CI/CD:GitHub Actions。

> 项目身份、需求与进度请见 `standards/`(00 项目上下文 · 01 需求 · PROGRESS 进度)。
> 详细启动步骤将在首个功能分支合并后补全。
