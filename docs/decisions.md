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
