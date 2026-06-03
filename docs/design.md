# 设计

Owner: `One Person Lab`
Purpose: `design`
State: `active_reference`
Machine boundary: 本文说明设计；行为真相以 `skills/opl-doc/SKILL.md`、`scripts/opl_doc_doctor.py` 和测试为准。

## 目标

本仓目标是让 AI 在长时间软件开发中维护当前唯一 Active Truth：理想目标、当前完成进度、现状与理想态差距、下一轮 Agent prompt、文档分层、退役策略和验证闭环。它治理开发相关文档，不治理 domain runtime 或交付物权威。

## 外部参考吸收

- OpenSpec：吸收 repo-native project context、agent instruction、change proposal、spec delta、archive foldback 思路。
- Spec Kit：吸收 spec-plan-tasks-implement 的闭环形态。
- Agent OS：吸收 standards / product / specs 的长期上下文分层。
- OpenArc：吸收 plugin / skill / doctor / profile-aware scan 产品形态。
- Superpowers / ADD：吸收 worktree、验证、finish branch、away/back、independent verification 的工程纪律。

不吸收外部固定路径。OPL series 继续使用当前 docs taxonomy 和 machine-readable truth。

## 核心对象

- `skill`: 给 Codex 读取的工作流与硬规则。
- `doctor`: 只读扫描器，输出 profile、repo-native surfaces、canonical doc 状态和 lifecycle findings。
- `family-plan`: 固化 OPL series 文档治理提示，变成可重复执行的工作流；输出 support repo extension policy，但不定义 repo truth、runtime truth、domain truth、artifact authority、quality verdict、owner receipt 或 Foundry Agent truth set。
- `autonomous development loop`: 用户维护 ideal-state reference；治理流程根据 live repo truth 重写当前完成进度、当前差距和下一轮 Agent prompt。
- `active truth plan template`: 当目标 repo 缺少稳定 active owner 时，提供最小文档形状；语义判断仍由 Codex 按 live repo truth 完成。
- `doctor guard`: 轻量结构红旗；不替代 Codex 对 Active Truth 语义的判断。
- `change packet`: 非平凡开发的短期 active 包，完成后 fold back。

## 完成口径

一个治理 tranche closeout 时，必须满足：

- canonical docs 只表达当前事实。
- active docs 只保留当前完成进度、当前差距和下一轮 Agent prompt。
- active truth plan 已重写当前完成进度、现状与理想态差距和下一轮 Agent prompt。
- active docs 没有执行日志、时间线或长历史清单污染。
- history/tombstone 承接过程和退役语义。
- contracts/tests/read-model 不被 prose 文档矛盾。
- 最终 main checkout 上有新鲜验证。

全局 OPL series `/goal` 完成还必须满足默认 6 个 repo 的 12 个主参考文档已用于校准，且 coverage ledger 证明所有 `README*` 与 `docs/**/*.md` 已逐段覆盖，没有未覆盖文档、未折回 stale/retire 候选或未进入下一轮 Agent prompt 的剩余 gap。否则只能报告本轮 tranche 完成，并继续保留全局 goal。
