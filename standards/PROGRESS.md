# PROGRESS · banksys_sy_lijunke 〔本项目活记忆 · 状态机〕

> **作用**:项目的“存档点”。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-08-02 · by Claude)

- **阶段**:`开发中(六步流程第③步,模块 C 已完成,待确认)`
- **上一步完成**:**模块 C(数据分析页)** 已完成:`src/banksys/analysis.py`(分析纯函数)、`app/main.py`(入口)、`app/pages/1_data_analysis.py`;本地自检全绿(ruff+24 测试+覆盖率 100%);真实启动验证 `/_stcore/health`=ok。
- **下一步 (TODO 第一条)**:✋确认门 3(模块 C 汇报)— 确认后开发**模块 D:在线预测页 `app/pages/2_predict.py`**。
- **阻塞项**:无。

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
| 2026-08-02 | **本地开发用 Python 3.13**(本机无 conda/uv/3.11),运行时与 CI/CD 仍固定 3.11 | 本机仅装 3.13;代码避免 3.12+ 专属语法,保证 3.11 兼容 |
| 2026-08-02 | **建模排除 `duration`**:对比实验 含=0.89 vs 不含=0.82(AUC),均过门槛;取不含 | `duration` 为通话时长,预测时刻未知且强关联目标,存在泄漏;用 `MODEL_FEATURES` 区分数据集字段与建模字段 |
| 2026-08-02 | **模型门槛定为 AUC ≥ 0.75**(无 duration 实测 0.82) | 二分类标准指标,阈值无关、对不平衡稳健;margin 约 0.07 |

---

## 已知坑 (GOTCHAS)

- **`gh` token 失效**:`gh auth status` 显示 falldown8848 的 token invalid;解决:先 `gh auth login -h github.com` 重新认证;验证:`gh auth status`。
- **本机无 conda/uv/3.11,仅 Python 3.13**:标准 `05` §6 优先 conda 但本机没有;解决:用 `py -3.13 -m venv .venv` 建本地环境,运行 pytest/ruff;验证:`.venv/Scripts/python.exe -V`。CI/CD 仍用 3.11。
- **Windows 控制台中文乱码**:脚本 print 中文在 GBK 控制台乱码;解决:运行前 `PYTHONIOENCODING=utf-8`,或改纯 ASCII;验证:本次 `train.py` 输出仍正常完成、`metrics.json` 为 UTF-8 无损。
- **joblib × numpy 2.5 DeprecationWarning**(83 条):`array.shape = self.shape` 已弃用;影响:仅警告不影响测试通过;解决:暂记录,后续可锁 numpy<2.5 或等 joblib 新版。
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
