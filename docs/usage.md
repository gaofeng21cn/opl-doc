# 使用说明

Owner: `One Person Lab`
Purpose: `usage`
State: `active_reference`
Machine boundary: 本文是人读使用说明；可执行命令入口以 `skills/` 和 `scripts/opl_doc_doctor.py` 为准，import API 以 `scripts/opl_doc_doctor_parts/` 为准。

## 它是什么

这是一个 Codex plugin / skill repo，同时带一个只读 CLI doctor 和 repo-native profile 同步面。使用形态接近 OpenArc：通过 skill 触发工作流，通过 CLI 产生诊断证据和插件同步声明。区别是本仓只服务 OPL-native 文档生命周期，不要求迁移到外部固定文件框架。

它也支持 OpenSpec-like repo-native 用法：skill 和 CLI 保持外置，进入目标 repo 后读取目标 repo 自己已有的 `AGENTS.md`、`TASTE.md`、`README*`、`docs/**`、contracts、source、tests 和 repo-local verify 入口。

## 常用调用

审计单仓：

```text
使用 OPL Doc 审计当前 repo 的 docs 生命周期，指出 stale active docs、history/tombstone 候选和 canonical doc 漂移。
```

执行OPL series治理：

```text
使用 OPL Doc 治理 OPL series 的开发文档生命周期。
```

对 OPL series、多仓、长周期或会修改文档的请求，skill 会让代理主动创建或延续 `/goal`；短单仓只读审计先跑 doctor，不强制 goal。

生成可执行工作流：

```bash
opl-doc-doctor family-plan --format markdown
```

`family-plan` 只生成治理 workflow 和 coverage discipline。默认 governed repo set 是 OPL、MAS、MAG、RCA、OMA、App 六个核心 repo；`opl-doc`、`opl-aion-shell` 等 support repo 只作为 explicit extension 出现在 `support_repo_policy`，不是默认 Foundry Agent truth set。

日常文档治理使用同一条核心路径：先按语义主题确定 Single Source of Truth，再对 peer docs 做内容级分类和合并。重复内容删除或收薄成指针；更细的内容纳入 owner 体系或标成 support reference；冲突或 stale 内容改写、归档或删除；历史增量长清单压缩成 current summary、remaining blocker、next owner 和 history pointer。

机器可读 goal objective：

```bash
opl-doc-doctor family-plan --format json
```

审计仓库：

```bash
opl-doc-doctor doctor /path/to/one-person-lab
```

检查或生成 repo-native profile：

```bash
opl-doc-doctor native-check /path/to/repo
opl-doc-doctor native-sync /path/to/repo
opl-doc-doctor native-sync /path/to/repo --apply
```

`native-sync` 默认只输出 dry-run 计划。带 `--apply` 时只写
`contracts/opl-native-profile.json`，把目标 repo 的 `repo_profile`、
`flow_profile`、`doc_profile`、Active Truth owner、canonical docs、taxonomy
dirs、machine truth surfaces、repo-owned paths 和验证入口固定成可检查声明。
这让 OPL Flow / OPL Doc 后续能做版本化升级和 drift 检查，同时不把目标
repo 的 domain truth、runtime truth、artifact authority、quality verdict 或
owner receipt 上收到插件。它也不持有 repo truth、production readiness 或
Foundry Agent truth set。

安装为本地 Codex plugin：

```bash
git clone git@github.com:gaofeng21cn/opl-doc.git
cd opl-doc
python3 scripts/install_local_plugin.py
python3 scripts/install_local_plugin.py --verify-only
```

安装脚本按 Codex personal plugin 标准复制到 `~/plugins/opl-doc`，更新 `~/.agents/plugins/marketplace.json`，并在 `~/.local/bin` 下创建 `opl-doc-doctor` 命令。它只提供 `opl-doc` canonical 入口；已退役旧名只保留在 history provenance。目标 repo 不需要安装本仓 CLI。

然后重启 Codex，在任意 OPL series repo 里直接提：

```text
使用 OPL Doc 审计这里的开发文档生命周期。
```

doctor 的 JSON 会报告目标 repo 已有的 agent guidance、canonical docs、machine truth surface 和验证入口，并提示明显结构风险。文档内容是否符合 Active Truth / SSOT，由 Codex 按 skill 读取 ideal-state reference、active plan、live code/contracts/tests/read-model 后判断和修改。

doctor 不能作为治理任务清单。正式治理必须先做 live truth 语义审计：逐段核对 active plan、核心文档和重要支撑文档中的实质 claim，读取 source、contracts、tests、CLI/read-model、runtime ledger、receipt 和 blocker 后，再决定更新、合并、归档、tombstone 或删除。

profile sync 不能作为 truth sync。`native-sync --apply` 的写入面只有 `contracts/opl-native-profile.json`，它声明 OPL Doc / OPL Flow 如何识别目标仓；目标仓当前事实仍归目标仓 canonical docs、contracts、source、tests、runtime ledger、receipt 和 blocker。

治理范围默认覆盖整个文档组合，而不是只覆盖 gap 文档。代理需要逐个审计 `README*` 和 `docs/**/*.md`，确认每个文档的唯一任务和定位；同一文档内混合 current truth、active plan、支撑参考、执行记录和历史时，应把内容移入各自 canonical owner，并归档、tombstone 或删除重复/过时材料。

已经过时的模块、接口、测试、文档、workflow 或入口，只要 replacement 和 no-active-caller 证据成立，就按当前理想态直接退役清理。不要为了兼容旧叙述新增 alias、facade、wrapper 或“旧入口仍可用”的 prose。

## Active Truth Plan 模板

[active-truth-plan.md](../templates/active-truth-plan.md) 是 single Active Truth plan 的推荐形状。目标 repo 已经有 canonical active plan 时，不新增第二份计划文档；把模板中的 `Ideal-State Reference`、`Active Owner Discovery`、`Current Completion Progress`、`Current-State vs Ideal-State Gaps`、`Next-Round Agent Prompt` 和 `History / Tombstone Foldback` 映射进现有 owner 文档即可。下一轮 Agent prompt 必须能直接作为 `/goal` 或长线 Codex prompt 使用。

## README 叙事口径

OPL series 根层 `README*` 是面向使用者的入口，应先回答“解决什么问题、为什么有用、怎么开始、能带来什么结果”。新概念进入 README 时，需要被翻译成用户能直觉理解的产品价值；`executor-first`、stage、route、receipt、typed blocker、Tool Affordance Boundary、domain truth、quality verdict 等技术边界只在折叠的 Agent / 开发者 / operator 区，或 `docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md` 等 canonical 技术文档中展开。

治理 README 时不要为了同步技术概念而硬插术语。若某个技术概念必须出现在入口页，先写用户问题和效果，再把机制细节放进折叠区；中英文 README 需同步这个叙事层级。

推荐写法：`认知计算让 AI 在一个可见阶段里读资料、比较方案、根据审阅修订，并产出下一版可检查成果。` 避免写法：`Route 保持 owner、receipt、typed blocker 和 route-back 证据，stage attempt 承载认知计算内核。` 后者属于 architecture、operator 或开发者折叠区。

## `/goal` 模板

skill 会优先主动创建或延续 `/goal`；[goal-opl-family-doc-lifecycle.md](../templates/goal-opl-family-doc-lifecycle.md) 是人工查看和外部复制用模板。该模板已经整合原先不定期手动执行的 OPL series 文档治理提示，包括按 repo 读取 ideal-state reference 与 single Active Truth plan、自动重写完成进度/差距/下一轮 Agent prompt、逐条评估 README/docs、清理归档、唯一任务定位、长清单折叠、直接退役旧模块/接口/测试、并行 worktree/subagent、吸收 main 和清理。

## Change Packet 模板

可复制 [templates/change-packet](../templates/change-packet/) 到目标 repo 的 `docs/active/changes/<change-id>/`。短期 change 完成后，必须把当前事实 fold back 到 canonical docs，把过程材料移入 history，并清理 active packet。
