# 00 · 项目上下文 〔本项目活记忆 · AI 维护〕

> **作用**:这是项目的“身份档案”。AI 接管项目时先读这里,了解项目目标、技术栈、目录、部署取值。
> **更新时机**:架构、技术栈、目录结构、端口、部署目录、重要约束变化时更新。
> **填写方式**:把 `<...>` 替换成真实内容;用不到的行删掉。

---

## 1. 项目是什么

- **项目名称**:`banksys_sy_lijunke`
- **一句话目标**:基于银行营销数据,构建一个 Web 应用,既能做数据分析,也能离线训练模型后提供在线认购预测。
- **使用者/受益者**:银行营销人员(用于筛选高意向客户)、数据分析学习者(用于 EDA 学习)。
- **核心功能**:
  - 数据分析交互页面:数据概览、字段分布、目标占比、特征与认购率关系、可交互筛选。
  - 在线预测系统:离线训练二分类模型,用户在网页点选/输入客户特征,返回「是否认购」及概率。
- **输入/数据**:`data/` 下的 UCI Bank Marketing 公开数据集(非敏感)。
  - `train.csv`:22500 行 × 22 列,含目标列 `subscribe`(yes/no),用于 EDA 与训练。
  - `test.csv`:7500 行 × 21 列,无目标列,用于演示/批量预测。
  - **是否进 Git**:进(公开教学数据,CI 干净 runner 上也能拿到,符合 `05` §7)。

## 2. 技术栈

| 层 | 选型 | 理由 |
|---|---|---|
| 语言/运行时 | Python 3.11 | 课程标准、生态成熟 |
| Web/API 框架 | Streamlit | 交互式数据分析 + 表单式预测一体,开发快 |
| 机器学习 | scikit-learn(管道 + LogisticRegression/RandomForest 等) | 传统表格二分类标准库,离线可复现 |
| 测试 | pytest + pytest-cov | 单测 + 覆盖率门禁 |
| 格式/静态检查 | ruff format + ruff check | 统一格式、简单快 |
| 打包/运行 | Docker(容器内端口固定 8888) | 可复现部署 |
| CI/CD | GitHub Actions | 通用、可视化、适合教学 |

## 3. 目录地图

```text
banksys_sy_lijunke/
├── standards/                 # AI 项目记忆与通用规范(本文档所在)
├── data/                      # 公开教学数据(train.csv / test.csv,进 Git)
├── src/banksys/               # 核心逻辑(纯函数优先,便于测试)
│   ├── __init__.py
│   ├── config.py              # 路径、常量、特征清单
│   ├── data.py                # 数据加载/校验/清洗
│   ├── features.py            # 特征工程(编码、Sklearn 管道)
│   └── model.py               # 训练/评估/保存/加载/预测封装
├── app/                       # Streamlit 应用
│   ├── main.py                # 入口,加载模型+校验,渲染导航
│   └── pages/
│       ├── 1_data_analysis.py # 数据分析交互页
│       └── 2_predict.py       # 在线预测页(点选输入)
├── scripts/
│   └── train.py               # 离线训练 CLI:加载→清洗→训练→评估→存模型
├── models/                    # 模型产物(训练生成,**不进 Git**)
├── tests/                     # pytest 测试
├── requirements.txt           # 生产运行依赖
├── requirements-dev.txt       # 本地/CI 检查依赖
├── Dockerfile                 # 容器内固定 8888
├── .dockerignore
├── .gitignore                 # 忽略 models/、__pycache__ 等
├── .github/workflows/
│   ├── ci.yml                 # PR/push:ruff+pytest+覆盖率+构建
│   └── cd.yml                 # main 合并:SSH→部署→健康检查
└── README.md
```

> 新增目录前先更新本节,避免项目越做越散。

## 4. 质量门槛

| 类型 | 本项目标准 |
|---|---|
| 格式检查 | `ruff format --check .` |
| 静态检查 | `ruff check .` |
| 单元测试 | `pytest` |
| 覆盖率 | `pytest --cov --cov-fail-under=80`(核心代码 ≥80%) |
| 构建 | `docker build` 成功(CI runner,本地不强制) |
| 业务/模型指标 | 验证集 **AUC ≥ 0.75**;并报告 F1、准确率。训练脚本不达标即失败退出 |

> 技术备注:建模时需评估 `duration`(通话时长)带来的目标泄漏风险,`00`/`01` 记录该决策;若最终用全特征,AUC 门槛再讨论。

## 5. 不变约束

- 密钥、密码、私钥、Token **绝不写进代码或文档**,只进 GitHub Secrets / 环境变量。
- 数据:公开教学数据,进 Git(`data/`)。
- 模型产物 `models/`:默认不进 Git;由训练脚本生成,并在构建/部署阶段打包进镜像。
- `main` 分支受保护,日常开发必须走 feature 分支 + PR;AI 不自行合并。
- CI 红灯不合并。
- 仓库与 Docker 容器名均为 `banksys_sy_lijunke`;仓库为**开源(public)**。
- 端口:容器内固定 **8888**;主机端口优先 8888,被占用时在 8888–8892 自动回退。

## 6. 部署/CI 占位符取值

> `guides/` 和 workflow 里的通用占位符,在本项目里的真实值只写这里。

| 占位符 | 本项目取值 | 说明 |
|---|---|---|
| `<APP>` | `banksys_sy_lijunke` | 镜像名/容器名 |
| `<DEPLOY_DIR>` | `/opt/banksys_sy_lijunke` | 服务器部署目录 |
| `<PORT>` | `8888` | 服务端口(主机优先) |
| `<PORT_MAX>` | `8892` | 主机端口回退区间上限 |
| `容器内端口` | `8888` | Docker 内固定,Streamlit `--server.port=8888` |
| `<PYVER>` | `3.11` | Python 版本 |
| `<HEALTHCHECK>` | `/_stcore/health` | Streamlit 内置健康检查,返回 `ok` |
| `<SSH_USER>` | `<待配 Secret:SSH_USER>` | 部署用户 |
| `<SSH_HOST>` | `<待配 Secret:SSH_HOST>` | 服务器公网 IP/域名 |
