# 使用说明

Owner: `One Person Lab`
Purpose: `usage`
State: `active_reference`
Machine boundary: 本文是人读使用说明；可执行入口以 `skills/` 和 `scripts/opl_doc_doctor.py` 为准。

## 它是什么

这是一个 Codex plugin / skill repo，同时带一个只读 CLI doctor。使用形态接近 OpenArc：通过 skill 触发工作流，通过 CLI 产生诊断证据。区别是本仓只服务 OPL-native 文档生命周期，不要求迁移到外部固定文件框架。

它也支持 OpenSpec-like repo-native 用法：目标 repo 可以携带 `.opl-doc-governance/`，让后续代理进入仓库后先读取本地治理入口，再按本仓 skill 和 doctor 工作。

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
python3 scripts/opl_doc_doctor.py family-plan --format markdown
```

机器可读 goal objective：

```bash
python3 scripts/opl_doc_doctor.py family-plan --format json
```

审计仓库：

```bash
python3 scripts/opl_doc_doctor.py doctor /path/to/one-person-lab
```

初始化目标 repo 的本地治理入口：

```bash
python3 scripts/opl_doc_doctor.py init-repo /path/to/repo --dry-run --format json
python3 scripts/opl_doc_doctor.py init-repo /path/to/repo --format json
```

`init-repo` 会写入 `.opl-doc-governance/config.json`、`.opl-doc-governance/agent-entry.md` 和 `.opl-doc-governance/README.md`。默认不覆盖已有文件，需要有意识刷新时使用 `--force`。

安装为本地 Codex plugin：

```bash
python3 scripts/install_local_plugin.py
```

然后重启 Codex，在任意 OPL series repo 里直接提：

```text
使用 OPL Doc Governance 审计这里的开发文档生命周期。
```

如果该 repo 已初始化 `.opl-doc-governance/agent-entry.md`，代理应先读取本地入口；这就是面向自动开发的 repo-native 能力。

## `/goal` 模板

skill 会优先主动创建或延续 `/goal`；[goal-opl-family-doc-lifecycle.md](../templates/goal-opl-family-doc-lifecycle.md) 是人工查看和外部复制用模板。该模板已经整合原先不定期手动执行的 OPL series 文档治理提示，包括按 repo 读取 ideal-state reference 与 active gap plan、逐条评估 README/docs、清理归档、唯一任务定位、长清单折叠、直接退役旧模块/接口/测试、并行 worktree/subagent、吸收 main 和清理。

## Change Packet 模板

可复制 [templates/change-packet](../templates/change-packet/) 到目标 repo 的 `docs/active/changes/<change-id>/`。短期 change 完成后，必须把当前事实 fold back 到 canonical docs，把过程材料移入 history，并清理 active packet。
