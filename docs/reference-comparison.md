# 外部参考对比

Owner: `One Person Lab`
Purpose: `reference_comparison`
State: `active_reference`
Machine boundary: 本文是人读参考对比；本仓行为以 skill、CLI doctor 和测试为准。

## OpenArc

相似点：plugin、skill、scan/doctor、repo governance、profile-aware 缺口报告。

差异：OpenArc 面向通用 AI-built repo，使用 `PROJECT_BRIEF`、`CHANGELOG_AI`、`SPEC`、`archive` 等固定治理面。本仓面向 OPL series，保留 OPL 当前 docs taxonomy、contracts/read-model 和 tombstone 规则。

分工：OpenArc-like 价值在外置 plugin/doctor 形态；OPL Doc 不让 CLI 接管文档语义，只让 Codex skill 根据 live repo truth 重写 Active Truth。

## OpenSpec

可吸收：repo-native project context、agent instructions、change proposal、spec delta、archive foldback。

已吸收：doctor 报告目标 repo 自己已有的 agent guidance、canonical docs、machine truth surface 和验证入口；skill 按这些原生入口启动治理。

不吸收：外部固定 spec 目录结构作为 OPL truth owner。

分工：OpenSpec-like 价值在 change proposal 与 archive foldback；OPL Doc 的长期主面是 single Active Truth plan，用户维护 ideal-state，Codex 派生当前进度、差距和下一轮 Agent prompt。

## GitHub Spec Kit

可吸收：Spec -> Plan -> Tasks -> Implement 的工程闭环、constitution / checklist / preset 思路。

不吸收：默认命令和文件布局。OPL 的 constitution 对应当前 `TASTE.md`、`AGENTS.md`、docs/invariants 和 contracts。

## Agent OS

可吸收：Standards / Product / Specs 的长期上下文分层。

OPL 映射：`AGENTS/TASTE` 是协作和 taste；`project/status/architecture/invariants` 是当前产品和架构真相；`docs/active` 是当前差距和执行包。

## Superpowers / ADD

可吸收：worktree、subagent、验证、finish branch、长时间自治时的 scope/decision/return briefing。

OPL 映射：用于执行纪律，不作为文件 taxonomy owner。
