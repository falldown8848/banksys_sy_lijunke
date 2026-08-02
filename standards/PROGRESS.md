# PROGRESS · banksys_sy_lijunke 〔本项目活记忆 · 状态机〕

> **作用**:项目的“存档点”。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-08-02 · by Claude)

- **阶段**:`初始化(六步流程第②步,开 feature 分支,待确认开发)`
- **上一步完成**:✋确认门 1 通过 — 三个 Secrets(`SSH_PRIVATE_KEY`/`SSH_HOST`/`SSH_USER`)已由人类配置并经 `gh secret list` 核对。
- **下一步 (TODO 第一条)**:✋确认门 2 — 确认分支名 `feature/1-init-engineering` 后进入第③步模块化开发(模块 A)。
- **阻塞项**:本地 `python` 指向 WindowsApps 占位,开发前需确认真 Python 3.11(conda/venv)。

---

## 待办清单 (TODO,按优先级)

- [x] 填写项目上下文:`00-project-context.md`
- [x] 确认需求与验收标准:`01-requirements.md`
- [x] **第①步建仓**:`gh auth login` 重新认证 → 已建开源仓库 `falldown8848/banksys_sy_lijunke` 并推送 main
- [x] 提示人类在 GitHub 配置 `SSH_PRIVATE_KEY`/`SSH_HOST`/`SSH_USER`(✋确认门 1,`gh secret list` 核对后继续)
- [ ] **第②步**:从 `main` 开 `feature/1-init-engineering` 分支(✋确认门 2)
- [ ] **模块 A**:工程骨架(目录、`.gitignore`、requirements、README)+ 数据层 `src/banksys/data.py` + 测试
- [ ] **模块 B**:离线训练 `scripts/train.py` + `src/banksys/features.py`/`model.py` + 评估指标 + 测试(✋每个模块汇报)
- [ ] **模块 C**:Streamlit 数据分析页 `app/pages/1_data_analysis.py`
- [ ] **模块 D**:在线预测页 `app/pages/2_predict.py`(点选输入 + 概率输出)
- [ ] **模块 E**:Dockerfile(端口 8888,支持 PIP_INDEX_URL)+ `ci.yml` + `cd.yml`
- [ ] **第④步本地自检**:`ruff format --check .` + `ruff check .` + `pytest --cov --cov-fail-under=80`(✋确认门 4)
- [ ] **第⑤步**:push feature 分支 + `gh pr create` + CI 复检(✋确认门 5)
- [ ] **第⑥步**:人工 Review + 人工合并 → CD 自动部署 → 健康检查 `/_stcore/health`(✋确认门 6,报最终端口)
- [ ] 会话结束前更新本文件

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-08-02 | 端口:容器内固定 8888,主机优先 8888、区间 8888–8892 自动回退 | 遵循 `05` §4 端口标准;Streamlit 以 `--server.port=8888` 启动 |
| 2026-08-02 | 健康检查用 `/_stcore/health`(返回 `ok`) | Streamlit 内置端点,无需额外服务 |
| 2026-08-02 | 数据 `data/*.csv` 进 Git;模型产物 `models/` 不进 Git | 公开教学数据可入库(`05` §7);模型由训练脚本生成并打包进镜像 |
| 2026-08-02 | 模型门槛:验证集 AUC ≥ 0.75,不达标训练脚本非零退出 | 二分类核心指标;需评估 `duration` 泄漏风险后再定最终门槛 |
| 2026-08-02 | 模型/特征处理放 `src/banksys`,页面只做 UI 层,预测复用同一管道 | 保证页面与离线预测一致(US-4 AC5),且核心逻辑可单测 |

---

## 已知坑 (GOTCHAS)

- **`gh` token 失效**:`gh auth status` 显示 falldown8848 的 token invalid;解决:先 `gh auth login -h github.com` 重新认证;验证:`gh auth status`。
- **WindowsApps 占位 python**:`which python` 指向 WindowsApps 占位(可能打不开);解决:用 conda 建 `python=3.11` 环境(默认,`05` §6);验证:`python -V` 显示 3.11.x。
- **`duration` 泄漏风险**:该字段对 `subscribe` 有极强关联,可能高估 AUC;解决:建模时对比「含/不含 duration」两版,决策写回本表;验证:复现指标并记录到 ADR。

---

## 里程碑 (DONE)

- [x] 完成 `standards/00`、`01`、本文件初始化(2026-08-02)
- [x] 建仓:开源仓库 `falldown8848/banksys_sy_lijunke` 已创建,main 引导提交已推送(2026-08-02)
- [ ] Secrets 就绪(`SSH_PRIVATE_KEY`/`SSH_HOST`/`SSH_USER`)
- [ ] feature 分支开发完成
- [ ] 本地自检全绿
- [ ] PR + CI 通过
- [ ] 合并 main → CD 部署成功,`/_stcore/health` 返回 ok

> 反臃肿:里程碑超过 15 条时,把更早内容合并成一行摘要,保持本文件可快速阅读。
