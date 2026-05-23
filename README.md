# OPL Doc Governance

Owner: `One Person Lab`
Purpose: `developer_document_lifecycle_governance`
State: `active_tooling`
Machine boundary: 本仓提供 Codex skill、CLI doctor、模板和测试，帮助治理开发相关文档生命周期。它不持有 OPL series 的项目真相、runtime truth、domain verdict、artifact authority 或 owner receipt。

`opl-doc-governance` 是 OPL-native 的文档生命周期管理与软件工程闭环工具。它吸收 OpenSpec、Spec Kit、Agent OS、OpenArc、Superpowers / ADD 等项目中有用的 repo-governance 思想，但文件 taxonomy、退役规则和机器边界使用 OPL series 现有约束。

## 使用方式

### 安装到本地 Codex

在本仓根目录执行：

```bash
python3 scripts/install_local_plugin.py
```

这会把当前仓库复制到 `~/plugins/opl-doc-governance`，并更新 `~/.agents/plugins/marketplace.json`。重启 Codex 后，`opl-doc-governance` skill 会出现在可用 skill/plugin 中。

### 作为 Codex skill

把本仓作为本地 plugin 安装或复制到 Codex 可发现的 plugin 目录后，直接对 Codex 说：

```text
使用 OPL Doc Governance 治理这个 repo 的开发文档生命周期。
```

如果请求是 OPL series、多仓、长周期、会修改文档、需要 worktree/subagent 或完成后吸收回 `main`，skill 会要求代理主动创建或延续 `/goal`，用户不需要额外记 prompt。

对 OPL series 执行长期治理时可以只说：

```text
使用 OPL Doc Governance 治理 OPL series 的开发文档生命周期。
```

它和 OpenArc 的相似点是：都是 repo governance plugin + skill + doctor。区别是 OpenArc 面向通用 AI-built repo，使用自己的固定治理文件；本仓面向 OPL series，保留 OPL 的 canonical docs、active/history/tombstone、contracts/read-model 边界。

### 作为 `/goal` 长线目标

本仓提供可复制模板：

```text
使用 OPL Doc Governance，以 OPL series 各 repo 的 ideal-state reference 和 active gap plan 为主要参考，逐条评估 README 与 docs 下其他文档，清理归档过时内容，折叠历史增量长清单，直接退役过时模块/接口/测试，不保留兼容面。可以用 subagent 并行开多个 worktree 推进；每条线完成后验证、吸收回 main、清理 worktree/branch，并更新对应 canonical docs/history/tombstone。
```

### 作为 CLI

```bash
python3 scripts/opl_doc_doctor.py doctor /path/to/repo
python3 scripts/opl_doc_doctor.py doctor /path/to/repo --format json
python3 scripts/opl_doc_doctor.py family-plan --format markdown
python3 scripts/opl_doc_doctor.py family-plan --format json
```

`doctor` 是只读诊断，不会修改目标仓库。它输出 repo profile、canonical docs 状态、machine-boundary header 状态、active/history/doc lifecycle 风险和建议动作。

`family-plan` 把 OPL series 长期文档治理提示固化成可执行工作流，并输出 `goal_mode.objective`，供 Codex 自动创建或延续 `/goal` 使用。

## 设计边界

- 开发文档服务 AI 长期理解目标、规划改动、验证闭环和归档历史。
- 当前事实进入 canonical docs；过程材料进入 history；还在推进的差距进入 active；机器真相进入 contracts / CLI / tests / ledger。
- 文档医生只报告风险，不把 Markdown 完整性当作生产 ready。
- 对 OPL series，清理原则是 direct retirement：已过时模块、接口、测试和文档入口在迁移条件成立后 delete/archive/tombstone，不新增兼容面。

## Change Packet

非平凡开发可以创建短期 active packet：

```text
docs/active/changes/<change-id>/
  intent.md
  design.md
  tasks.md
  verification.md
  foldback.md
```

完成后，当前事实折叠进 canonical docs；过程材料进入 `docs/history/process/`、`docs/history/plans/` 或 `docs/history/specs/`；已退役内容进入 tombstone/provenance。

## 验证

```bash
python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor .
python3 scripts/opl_doc_doctor.py family-plan --format markdown
```
