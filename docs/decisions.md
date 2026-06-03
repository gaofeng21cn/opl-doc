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

该文件不持有 domain truth、runtime truth、artifact authority、quality verdict、owner receipt 或生产 ready 证据；这些仍由目标 repo 的 contracts、source、tests、runtime ledger、owner receipt 和 repo-native verification 持有。

## Family plan 只生成 workflow，不定义 truth owner 集合

`family-plan` 的默认 governed repo set 保持 OPL、MAS、MAG、RCA、OMA 和 App 六仓，输出的是治理 workflow、coverage discipline 和 `/goal` objective。`opl-doc`、`opl-aion-shell` 等 support repo 通过 `support_repo_policy` 标成 explicit extension，只在用户显式要求或当前任务触及 workflow / shell carrier / support docs 时纳入。该输出不持有 repo truth、runtime truth、domain truth、artifact authority、quality verdict、owner receipt、production readiness 或 Foundry Agent truth set。
