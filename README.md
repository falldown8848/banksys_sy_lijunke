# banksys_sy_lijunke

基于银行营销数据的 Web 应用,包含两个核心功能:

1. **数据分析交互页面** — 数据概览、数值/分类字段分布、特征与认购率关系,侧边栏年龄筛选。
2. **在线预测系统** — 离线训练二分类模型,网页点选/输入客户特征,预测是否认购定期存款及概率。

技术栈:Python 3.11 · Streamlit · scikit-learn · pytest · ruff · Docker(端口 8888)· GitHub Actions(CI/CD)。

---

## 功能

| 页面 | 说明 |
|---|---|
| 📊 数据分析 | 数据概览指标、目标分布、数值分布+相关性热力图、分类分布与认购率 |
| 🔮 在线预测 | 10 个分类字段下拉点选 + 9 个数值字段输入,返回「认购/不认购」与概率 |

## 数据

公开数据集 UCI Bank Marketing(`data/train.csv` 22500 行含目标列 `subscribe`;`data/test.csv` 7500 行无目标)。公开教学数据,随仓库入库。

## 快速开始(本地)

```bash
# 1) 建环境(Python 3.11;本机如无,任意 3.11+ 亦可)
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .              # 安装项目自身(banksys 包,src 布局)

# 2) 训练模型(生成 models/pipeline.joblib + metrics.json)
python scripts/train.py            # 验证集 AUC < 0.75 会非零退出

# 3) 启动应用(端口 8888)
streamlit run app/main.py --server.port 8888
# 访问 http://localhost:8888  ;健康检查 http://localhost:8888/_stcore/health
```

国内网络可用镜像源:`pip install -r requirements-dev.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

## 质量门禁

```bash
ruff format --check .              # 格式
ruff check .                       # 静态检查
pytest --cov --cov-fail-under=80   # 单测 + 覆盖率 ≥80%
python scripts/train.py            # 训练门禁:AUC ≥ 0.75
```

## Docker 部署

镜像内固定端口 8888;`PIP_INDEX_URL` 构建参数可配置镜像源。

```bash
docker build -t banksys_sy_lijunke:latest .
docker run -d --name banksys_sy_lijunke --restart unless-stopped \
  -p 8888:8888 banksys_sy_lijunke:latest
curl -fsS http://localhost:8888/_stcore/health   # 期望输出 ok
```

构建阶段会执行训练并生成模型(模型产物不进 Git,进镜像);AUC 不达标构建失败。

## CI/CD

- **CI**(`.github/workflows/ci.yml`):PR 与 push main 触发 — ruff 格式+静态检查、pytest 覆盖率、训练门禁、Docker 构建 + 容器健康检查。红灯不允许合并。
- **CD**(`.github/workflows/cd.yml`):合并 main 自动触发 — SSH 同步代码到服务器 → `deploy.sh` 构建镜像、端口 8888–8892 自动回退、幂等重启、健康检查。

### 需要的 GitHub Secrets

| Secret | 含义 |
|---|---|
| `SSH_PRIVATE_KEY` | 部署服务器私钥全文(保留 BEGIN/END 与换行) |
| `SSH_HOST` | 服务器公网 IP 或域名 |
| `SSH_USER` | 部署用户,如 `root` 或 `deploy` |

> 密钥只进 Secrets,绝不进代码。服务器需预装 Docker,且 `SSH_USER` 有 docker 权限。

## 目录结构

```text
banksys_sy_lijunke/
├── standards/                 # AI 项目记忆与通用规范(00 上下文 / 01 需求 / PROGRESS 进度 / 02~06)
├── data/                      # 公开教学数据(进 Git)
├── src/banksys/               # 核心逻辑:config / data / features / model / analysis / inputs
├── app/                       # Streamlit 应用:main.py + pages/
├── scripts/train.py           # 离线训练 CLI
├── tests/                     # pytest 测试(含页面 AppTest 冒烟)
├── models/                    # 模型产物(构建时生成,不进 Git)
├── deploy.sh                  # CD 远程部署脚本
├── Dockerfile / .dockerignore
├── requirements.txt / requirements-dev.txt
├── pyproject.toml             # ruff / pytest / coverage 配置
└── .github/workflows/{ci,cd}.yml
```
