# 使用说明

Owner: `One Person Lab`
Purpose: `usage`
State: `active_reference`
Machine boundary: 本文是人读使用说明；可执行入口以 `skills/` 和 `scripts/opl_doc_doctor.py` 为准。

## 它是什么

这是一个 Codex plugin / skill repo，同时带一个只读 CLI doctor。使用形态接近 OpenArc：通过 skill 触发工作流，通过 CLI 产生诊断证据。区别是本仓只服务 OPL-native 文档生命周期，不要求迁移到外部固定文件框架。

它也支持 OpenSpec-like repo-native 用法：skill 和 CLI 保持外置，进入目标 repo 后读取目标 repo 自己已有的 `AGENTS.md`、`TASTE.md`、`README*`、`docs/**`、contracts、source、tests 和 repo-local verify 入口。

## 常用调用

审计单仓：

```text
使用 OPL Doc Governance 审计当前 repo 的 docs 生命周期，指出 stale active docs、history/tombstone 候选和 canonical doc 漂移。
```

执行OPL series治理：

```text
使用 OPL Doc Governance 治理 OPL series 的开发文档生命周期。
```

对 OPL series、多仓、长周期或会修改文档的请求，skill 会让代理主动创建或延续 `/goal`；短单仓只读审计先跑 doctor，不强制 goal。

生成可执行工作流：

```bash
opl-doc-doctor family-plan --format markdown
```

机器可读 goal objective：

```bash
opl-doc-doctor family-plan --format json
```

审计仓库：

```bash
opl-doc-doctor doctor /path/to/one-person-lab
```

安装为本地 Codex plugin：

```bash
python3 scripts/install_local_plugin.py
```

安装脚本按 Codex personal plugin 标准复制到 `~/plugins/opl-doc-governance`，更新 `~/.agents/plugins/marketplace.json`，并在 `~/.local/bin` 下创建 `opl-doc-doctor` 命令。目标 repo 不需要安装本仓 CLI。

然后重启 Codex，在任意 OPL series repo 里直接提：

```text
使用 OPL Doc Governance 审计这里的开发文档生命周期。
```

doctor 的 JSON 会报告目标 repo 已有的 agent guidance、canonical docs、machine truth surface 和验证入口，并提示明显结构风险。文档内容是否符合 Active Truth / SSOT，由 Codex 按 skill 读取 ideal-state reference、active plan、live code/contracts/tests/read-model 后判断和修改。

## Active Truth Plan 模板

[active-truth-plan.md](../templates/active-truth-plan.md) 是 single Active Truth plan 的推荐形状。目标 repo 已经有 canonical active plan 时，不新增第二份计划文档；把模板中的 `Ideal-State Reference`、`Active Owner Discovery`、`Current Completion Progress`、`Current-State vs Ideal-State Gaps`、`Next-Round Agent Prompt` 和 `History / Tombstone Foldback` 映射进现有 owner 文档即可。下一轮 Agent prompt 必须能直接作为 `/goal` 或长线 Codex prompt 使用。

## `/goal` 模板

skill 会优先主动创建或延续 `/goal`；[goal-opl-family-doc-lifecycle.md](../templates/goal-opl-family-doc-lifecycle.md) 是人工查看和外部复制用模板。该模板已经整合原先不定期手动执行的 OPL series 文档治理提示，包括按 repo 读取 ideal-state reference 与 single Active Truth plan、自动重写完成进度/差距/下一轮 Agent prompt、逐条评估 README/docs、清理归档、唯一任务定位、长清单折叠、直接退役旧模块/接口/测试、并行 worktree/subagent、吸收 main 和清理。

## Change Packet 模板

可复制 [templates/change-packet](../templates/change-packet/) 到目标 repo 的 `docs/active/changes/<change-id>/`。短期 change 完成后，必须把当前事实 fold back 到 canonical docs，把过程材料移入 history，并清理 active packet。
