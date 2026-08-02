# 01 · 需求 / 活 PRD 〔本项目活记忆 · AI 维护〕

> **作用**:本项目唯一的需求文档。所有新功能、缺陷、技术债都追加到这里,不要另起多个 PRD 文件。
> **更新时机**:每次有新需求、需求变更、验收标准变化时更新。

---

## 1. 需求来源

| 类型 | 来源 | 进入方式 |
|---|---|---|
| 功能需求 Feature | 用户 / 老师 / 产品 / 客户 | 写成用户故事 |
| 缺陷 Bug | 测试 / 线上日志 / 用户反馈 | 写复现步骤和期望结果 |
| 技术债 Tech Debt | 开发 / Review / CI/CD 故障 | 写影响和修复目标 |

---

## 2. Issue 生命周期

| 阶段 | 状态 | 动作 |
|---|---|---|
| 提出 | Open | 写清场景、目标、验收标准 |
| 排期 | Backlog / Todo | 决定优先级和负责人 |
| 开发 | In Progress | 从 main 开 feature 分支 |
| 评审 | In Review | 提 PR,等待 CI 和 Review |
| 合并 | Done | PR 合并 main,自动关闭 Issue |
| 验收 | Verified | 按验收标准确认 |

**追踪规则**:分支名带 Issue 号,PR 描述写 `closes #<编号>`。

---

## 3. 用户故事模板

```text
### US-<编号> <一句话标题> · 状态: Backlog
作为 <角色>,
我想要 <能力>,
以便 <价值>。

验收标准:
- AC1: Given <前提>,When <动作>,Then <可验证结果>。
- AC2: <补充标准>

技术备注:
- <可选:约束、边界、风险>
```

---

## 4. 需求清单

> 优先级:P0 = 阻断交付;P1 = 核心功能;P2 = 增强。

### US-1 初始化项目工程化与 CI/CD · 状态: Backlog · P0

作为 **项目开发者**,
我想要 项目具备基础工程结构、测试、CI 与 CD,
以便 后续每次开发都能自动检查并自动部署。

验收标准:
- AC1: 创建开源仓库 `banksys_sy_lijunke`,`main` 只放最小引导提交,不直接 push 真实开发。
- AC2: 建仓后提醒配置 Secrets(`SSH_PRIVATE_KEY`/`SSH_HOST`/`SSH_USER`),核对无误才进下一步。
- AC3: 从 `main` 开 `feature/<issue>-<desc>` 分支完成开发,PR 触发 CI(ruff 格式+静态检查+pytest+覆盖率+`docker build`)。
- AC4: CI 全绿后由人工合并 main。
- AC5: 合并 main 自动触发 CD,部署后健康检查 `/_stcore/health` 返回 `ok`。
- AC6: 完成后更新 `standards/PROGRESS.md`。

技术备注:本地不强制 `docker build`,构建交给 CI 与服务器;见 `05` §2。

---

### US-2 数据分析交互页面 · 状态: Backlog · P0

作为 **银行营销分析师**,
我想要 在网页上交互式查看客户数据的概览、字段分布与认购规律,
以便 理解数据特征、发现高意向客户线索。

验收标准:
- AC1: Given 应用已启动,When 打开数据分析页,Then 展示数据来源、行数/列数、字段类型等概览。
- AC2: Given 页面加载 `data/train.csv`,When 查看数值字段,Then 展示统计摘要(均值/最值/缺失等)与分布图。
- AC3: When 查看分类字段,Then 展示取值分布,并可与目标列 `subscribe` 对比(认购率/占比)。
- AC4: When 使用交互控件(下拉/多选/滑块),Then 图表随选择即时更新,无需重启应用。
- AC5: Given 数据缺失或格式异常,When 页面加载,Then 给出明确错误提示,不崩溃。

技术备注:图表用 Streamlit 原生组件 + Plotly;加载逻辑放在 `src/banksys/data.py` 纯函数,便于测试。

---

### US-3 离线训练模型 · 状态: Backlog · P0

作为 **数据科学家/开发者**,
我想要 用 `data/train.csv` 离线训练二分类模型并评估、保存产物,
以便 供在线预测页复用同一套特征处理与模型。

验收标准:
- AC1: Given 命令行运行 `python scripts/train.py`,Then 加载并校验 `train.csv`,划分训练/验证集(固定随机种子,可复现)。
- AC2: When 训练完成,Then 输出验证集指标(AUC、F1、准确率)并保存模型+特征管道到 `models/`。
- AC3: Given 验证集 AUC < 0.75,When 训练脚本结束,Then 以非零退出码失败,不放行 CI/CD。
- AC4: When 模型已保存,Then 可用同一管道对新样本做预测(特征处理与训练时一致)。
- AC5: Given `train.csv` 缺失/字段异常,When 运行脚本,Then 报清晰错误并失败退出。

技术备注:
- `models/` 不进 Git;由 CD/镜像构建阶段生成或打包。
- 评估 `duration` 是否引入目标泄漏,决策记录到 PROGRESS ADR。
- 随机性:固定 `random_state`,保证测试可重复(见 `03` §3)。

---

### US-4 在线预测系统 · 状态: Backlog · P0

作为 **银行营销人员**,
我想要 在网页上以点选/输入方式填写客户信息,立刻得到「是否认购」的预测结果与概率,
以便 聚焦高意向客户、降低无效营销成本。

验收标准:
- AC1: Given 模型已训练并存在 `models/`,When 打开预测页,Then 展示完整特征输入表单(分类字段下拉点选、数值字段数字输入)。
- AC2: When 提交表单,Then 显示预测结论(认购/不认购)、认购概率及输入特征摘要。
- AC3: Given 输入校验失败(如年龄超范围、缺失必填),When 提交,Then 就地提示错误,不生成预测。
- AC4: Given 模型文件缺失或损坏,When 打开/提交预测页,Then 给出「模型未就绪」引导提示,不崩溃。
- AC5: When 提交任意合法输入,Then 预测结果与 `scripts/train.py` 的离线预测结果一致(同一管道)。

技术备注:预测逻辑复用 `src/banksys/model.py` 的 `predict`;避免在页面里重新实现特征处理。

---

### US-5 容器化与 8888 端口部署 · 状态: Backlog · P1

作为 **运维/项目负责人**,
我想要 应用能以 Docker 镜像运行,监听 8888 端口并提供健康检查,
以便 在服务器上一键部署、随时验证存活。

验收标准:
- AC1: `docker build` 成功;镜像内 Streamlit 以 `--server.port=8888` 启动(容器内固定 8888)。
- AC2: 主机端口优先 8888,被占用时在 8888–8892 自动回退,CD 日志打印最终端口。
- AC3: 容器启动后 `curl http://localhost:<port>/_stcore/health` 返回 `ok`。
- AC4: 部署脚本幂等(`docker rm -f <APP>` 停删自身旧容器),`set -e`,失败即停。
- AC5: `Dockerfile` 支持 `PIP_INDEX_URL` 镜像源参数,可配置国内源(见 `05` §4)。

技术备注:镜像构建时确保 `models/` 产物存在(训练步骤先于构建)。

---

### US-6 测试与质量门禁 · 状态: Backlog · P1

作为 **项目开发者**,
我想要 核心逻辑有单元测试并被 CI 强制检查,
以便 每次改动都有回归保障,CI 红灯可及时发现。

验收标准:
- AC1: 数据加载、特征处理、模型评估、预测等核心逻辑有单元测试(AAA 写法)。
- AC2: `ruff format --check .`、`ruff check .` 通过。
- AC3: `pytest --cov --cov-fail-under=80` 通过,覆盖率达标。
- AC4: 测试可重复、无外部网络依赖;涉及随机时固定种子。
- AC5: CI 在 PR 上执行以上门禁 + `docker build`;红灯不允许合并。

---

## 5. 非功能需求

- **安全**:密钥只进 Secrets,不进 Git;`.env.example` 可进仓库,真实值不进。
- **可维护**:一需求一分支一 PR;PR 尽量 < 400 行;Commit 用 Conventional Commits。
- **可测试**:核心逻辑必须有单测;测试用 AAA / Given-When-Then。
- **可部署**:CD 自动触发;部署后必须健康检查,失败即红灯。
- **可复现**:训练随机种子固定;Docker 构建参数可配镜像源。
- **公开性**:仓库为开源,README 写明启动、训练、预测、部署步骤,不写真实密钥。
