# 设计

Owner: `One Person Lab`
Purpose: `design`
State: `active_reference`
Machine boundary: 本文说明设计；行为真相以 `skills/opl-doc-governance/SKILL.md`、`scripts/opl_doc_doctor.py` 和测试为准。

## 目标

本仓目标是让 AI 在长时间软件开发中理解当前目标、文档分层、退役策略和验证闭环。它治理开发相关文档，不治理 domain runtime 或交付物权威。

## 外部参考吸收

- OpenSpec：吸收 change proposal / spec delta / archive foldback 思路。
- OpenSpec：吸收 repo-native project context / agent instruction 的自描述形态。
- Spec Kit：吸收 spec-plan-tasks-implement 的闭环形态。
- Agent OS：吸收 standards / product / specs 的长期上下文分层。
- OpenArc：吸收 plugin / skill / doctor / profile-aware scan 产品形态。
- Superpowers / ADD：吸收 worktree、验证、finish branch、away/back、independent verification 的工程纪律。

不吸收外部固定路径。OPL series 继续使用当前 docs taxonomy 和 machine-readable truth。

## 核心对象

- `skill`: 给 Codex 读取的工作流与硬规则。
- `doctor`: 只读扫描器，输出 profile、canonical doc 状态和 lifecycle findings。
- `repo-native anchor`: `.opl-doc-governance/` 中的本地 config、agent entry 和说明，让目标 repo 自带治理入口。
- `family-plan`: 固化OPL series文档治理提示，变成可重复执行的工作流。
- `change packet`: 非平凡开发的短期 active 包，完成后 fold back。

## 完成口径

一个治理轮次完成时，必须满足：

- canonical docs 只表达当前事实。
- active docs 只保留当前计划、差距和 baton。
- history/tombstone 承接过程和退役语义。
- contracts/tests/read-model 不被 prose 文档矛盾。
- 最终 main checkout 上有新鲜验证。
