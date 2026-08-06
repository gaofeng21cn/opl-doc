# 决策

Owner: `One Person Lab`
Purpose: `decisions`
State: `active_truth`
Machine boundary: 本文是人读决策记录；行为以源码和测试为准。

## 保留 OPL-native taxonomy

OpenArc、OpenSpec、Spec Kit、Agent OS 等项目作为参考，不作为本仓或 OPL series 的文件布局 owner。原因是 OPL series 已有 active/history/tombstone、contracts/read-model 和跨 repo owner boundary。

## Doctor 先只读

文档生命周期治理容易误删历史或制造第二真相源。第一版 doctor 只报告 findings，由 Codex skill 或人工 operator 决定是否修改目标 repo。

## Repo-native 只读识别

OPL Doc 的 repo-native 能力由外置 skill / CLI 读取目标 repo 自己已有的 `AGENTS.md`、`TASTE.md`、canonical docs、machine truth surface 和验证入口。目标 repo 不需要安装本仓 CLI，也不需要生成 `.opl-doc/` 目录。

## Repo-native profile 只写同步声明

`native-sync --apply` 可以在目标 repo 写入 `contracts/opl-native-profile.json`。这是唯一允许的目标仓写入面，作用是让 OPL Flow / OPL Doc 能检查 repo 使用的 profile、Active Truth owner、canonical docs、taxonomy dirs、machine truth surfaces、repo-owned paths 和验证入口是否漂移。

验证入口分为两类：OPL Doc 从 `scripts/verify.sh`、受支持的 `package.json` scripts 与 pytest 约定重算可发现入口；目标 repo 在同一 `verification_commands` 字段显式声明的其它命令按 repo truth 保留并去重。同步不得解析自由文本 `AGENTS.md` 猜测命令，也不得保留已经失去真实文件或 package script 的可发现入口。

对 Git checkout，repo identity、canonical docs/taxonomy、machine-truth surface、验证入口和 Markdown 扫描只读取当前 index 中实际存在的 tracked path。Ignored/untracked cache、生成站点、临时 `package.json` 或空目录不是 active repo truth；非 Git 输入仍按当前文件系统检查。

该文件不持有 domain truth、runtime truth、artifact authority、quality verdict、owner receipt 或生产 ready 证据；这些仍由目标 repo 的 contracts、source、tests、runtime ledger、owner receipt 和 repo-native verification 持有。

## Family plan 只生成 workflow，不定义 truth owner 集合

`family-plan` 内置 OPL、App、Native Workbench、OPL Flow、OPL Doc、MAS、MAG、RCA、OMA、BookForge 和 MAS Scholar Skills 这 11 仓 workflow baseline。传入 `--workspace-root` 后，它从真实 Git 根仓、repo-local owner 标识与 canonical GitHub owner 保守形成本轮 governed repo map，并通过 `live_workspace_inventory` 输出发现依据、support extension 和排除计数；`--repo` 保留为非标准布局或新纳入仓库的显式覆盖。已退役或不存在的仓库不构成缺失项，外部仓库不进入 scope，`opl-aion-shell` 等 upstream shell repo 通过 `support_repo_policy` 保持 explicit extension/read-only fork boundary。该输出只证明 scope discovery，不持有 repo truth、runtime truth、domain truth、artifact authority、quality verdict、owner receipt、production readiness 或 Foundry Agent truth set。
