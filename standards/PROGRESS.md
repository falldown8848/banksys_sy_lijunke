# PROGRESS · banksys_sy_lijunke 〔本项目活记忆 · 状态机〕

> **作用**:项目的“存档点”。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-08-02 · by Claude)

- **阶段**:`已上线(六步流程全部完成:建仓→PR→CI→合并→CD 部署成功)`
- **上一步完成**:✋确认门 6 — **CD 部署成功**:镜像构建通过(AUC 0.8168),主机端口回退到 **8898**,容器运行,`/_stcore/health` 返回 **ok**。访问 `http://<SSH_HOST>:8898`。
- **下一步 (TODO 第一条)**:可选 — 确认服务器防火墙/安全组放行 8898;将文档分支合并收尾。
- **阻塞项**:无(部署已完成)。

---

## 待办清单 (TODO,按优先级)

- [x] 填写项目上下文:`00-project-context.md`
- [x] 确认需求与验收标准:`01-requirements.md`
- [x] **第①步建仓**:`gh auth login` 重新认证 → 已建开源仓库 `falldown8848/banksys_sy_lijunke` 并推送 main
- [x] 提示人类在 GitHub 配置 `SSH_PRIVATE_KEY`/`SSH_HOST`/`SSH_USER`(✋确认门 1,`gh secret list` 核对后继续)
- [x] **第②步**:从 `main` 开 `feature/1-init-engineering` 分支(✋确认门 2)
- [x] **模块 A**:工程骨架(目录、`.gitignore`、requirements、pyproject、README)+ 数据层 `src/banksys/data.py` + 测试(**ruff 通过,6 测试通过,覆盖率 100%**,提交 `8fdf5c2`)
- [x] **模块 B**:离线训练 `scripts/train.py` + `src/banksys/features.py`/`model.py` + 评估指标 + 测试(**AUC 0.8168 过 0.75 门槛,16 测试通过,覆盖率 100%**)
- [x] **模块 C**:Streamlit 数据分析页 `app/pages/1_data_analysis.py`(**24 测试通过,覆盖率 100%,`/health`=ok**)
- [x] **模块 D**:在线预测页 `app/pages/2_predict.py`(点选输入 + 概率输出,**31 测试通过,覆盖率 100%,端到端验证 OK**)
- [x] **模块 E**:Dockerfile(端口 8888,构建期训练,PIP_INDEX_URL)+ `deploy.sh` + `ci.yml` + `cd.yml`(**本地 31 测试/覆盖率 100%;docker 构建交 CI**)
- [x] **第④步本地自检**:`ruff format --check .` + `ruff check .` + `pytest --cov --cov-fail-under=80`(**全绿**:31 测试/覆盖率 100%)(✋确认门 4)
- [x] **第⑤步**:push feature 分支 + `gh pr create`(PR #2)+ CI 复检(**全绿**)(✋确认门 5)
- [x] **第⑥步**:人工 Review + 人工合并(PR #2/#3/#4/#5)→ CD 自动部署成功 → 健康检查 `/_stcore/health` 返回 ok,最终端口 **8898**(✋确认门 6)
- [x] 会话结束前更新本文件

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-08-02 | 端口:容器内固定 8888,主机优先 8888、区间 8888–8892 自动回退 | 遵循 `05` §4 端口标准;Streamlit 以 `--server.port=8888` 启动 |
| 2026-08-02 | 健康检查用 `/_stcore/health`(返回 `ok`) | Streamlit 内置端点,无需额外服务 |
| 2026-08-02 | 数据 `data/*.csv` 进 Git;模型产物 `models/` 不进 Git | 公开教学数据可入库(`05` §7);模型由训练脚本生成并打包进镜像 |
| 2026-08-02 | 模型门槛:验证集 AUC ≥ 0.75,不达标训练脚本非零退出 | 二分类核心指标;需评估 `duration` 泄漏风险后再定最终门槛 |
| 2026-08-02 | 模型/特征处理放 `src/banksys`,页面只做 UI 层,预测复用同一管道 | 保证页面与离线预测一致(US-4 AC5),且核心逻辑可单测 |
| 2026-08-02 | **本地开发用 Python 3.13**(本机无 conda/uv/3.11),运行时与 CI/CD 仍固定 3.11 | 本机仅装 3.13;代码避免 3.12+ 专属语法,保证 3.11 兼容 |
| 2026-08-02 | **建模排除 `duration`**:对比实验 含=0.89 vs 不含=0.82(AUC),均过门槛;取不含 | `duration` 为通话时长,预测时刻未知且强关联目标,存在泄漏;用 `MODEL_FEATURES` 区分数据集字段与建模字段 |
| 2026-08-02 | **模型门槛定为 AUC ≥ 0.75**(无 duration 实测 0.82) | 二分类标准指标,阈值无关、对不平衡稳健;margin 约 0.07 |
| 2026-08-02 | **预测页输入范围**以 `inputs.py` 单一来源定义;分类选项从 OneHotEncoder 提取 | 页面/校验/测试共用一份定义;分类取值以训练管道为准,避免与数据重复加载 |
| 2026-08-02 | **训练放 Docker 构建期**:`RUN python scripts/train.py` 生成模型入镜像 | `models/` 不进 Git;构建期训练保证镜像自包含,且 AUC 不达标构建即失败 |
| 2026-08-02 | **CI 双 job**:check(ruff/pytest/训练门禁)+ docker(构建+容器健康检查冒烟) | 快反馈 + 镜像可运行性分离;健康检查为项目特有门禁 |

---

## 已知坑 (GOTCHAS)

- **`gh` token 失效**:`gh auth status` 显示 falldown8848 的 token invalid;解决:先 `gh auth login -h github.com` 重新认证;验证:`gh auth status`。
- **本机无 conda/uv/3.11,仅 Python 3.13**:标准 `05` §6 优先 conda 但本机没有;解决:用 `py -3.13 -m venv .venv` 建本地环境,运行 pytest/ruff;验证:`.venv/Scripts/python.exe -V`。CI/CD 仍用 3.11。
- **Windows 控制台中文乱码**:脚本 print 中文在 GBK 控制台乱码;解决:运行前 `PYTHONIOENCODING=utf-8`,或改纯 ASCII;验证:本次 `train.py` 输出仍正常完成、`metrics.json` 为 UTF-8 无损。
- **joblib × numpy 2.5 DeprecationWarning**(83 条):`array.shape = self.shape` 已弃用;影响:仅警告不影响测试通过;解决:暂记录,后续可锁 numpy<2.5 或等 joblib 新版。
- **本机 Docker daemon 未运行**:`docker info` 拿不到 Server Version;影响:本地无法 `docker build`;解决:按 `05` §2 本地不强制 Docker,构建由 CI(ubuntu runner)验证;验证:PR 上 CI docker job 全绿。
- **CI 红灯:`No module named 'banksys'`**:`scripts/train.py` 直接运行需 `banksys` 包;CI 只 `pip install -r requirements-dev.txt`,未装 src 布局项目包;本地因手动 `pip install -e .` 掩盖了此问题。解决:CI 安装步骤追加 `pip install -e .`,README 同步;验证:复检 CI Lint & Tests job 全绿。
- **`duration` 泄漏风险**:该字段对 `subscribe` 有极强关联,可能高估 AUC;解决:建模时对比「含/不含 duration」两版,决策写回本表;验证:复现指标并记录到 ADR。

---

## 里程碑 (DONE)

- [x] 完成 `standards/00`、`01`、本文件初始化(2026-08-02)
- [x] 建仓:开源仓库 `falldown8848/banksys_sy_lijunke` 已创建,main 引导提交已推送(2026-08-02)
- [x] Secrets 就绪(`SSH_PRIVATE_KEY`/`SSH_HOST`/`SSH_USER`)
- [x] feature 分支开发完成(A~E 五模块,31 测试,覆盖率 100%,AUC 0.8168)
- [x] 本地自检全绿
- [x] PR #2 + CI 全绿(Lint & Tests + Docker Build & Smoke)
- [x] **合并 main → CD 部署成功:端口 8898,`/_stcore/health` 返回 ok(2026-08-02)**

> 反臃肿:里程碑超过 15 条时,把更早内容合并成一行摘要,保持本文件可快速阅读。
