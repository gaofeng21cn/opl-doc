# 项目概览

Owner: `One Person Lab`
Purpose: `project`
State: `active_truth`
Machine boundary: 本文是人读项目定位；机器真相以 `.codex-plugin/plugin.json`、`skills/opl-doc/SKILL.md`、`scripts/opl_doc_doctor.py` 命令 bootstrap、`scripts/opl_doc_doctor_parts/` import API 和测试为准。

`opl-doc` 是 OPL-native 开发文档生命周期治理工具。它的目标是让 AI 在长时间自主软件开发中稳定维护当前唯一 Active Truth：理想目标由用户维护，当前状态摘要、现状与理想态差距、下一轮 Agent prompt、文档分层、退役规则、验证闭环和归档策略由治理流程根据 live repo truth 刷新。

本仓提供：

- Codex plugin manifest。
- `opl-doc` canonical skill。
- 只读 CLI doctor。
- OPL series 文档治理 workflow，默认覆盖 11 个可维护 repo：OPL、App、Native Workbench、OPL Flow、OPL Doc、MAS、MAG、RCA、OMA、BookForge 和 MAS Scholar Skills，并可扩展到其他 OPL-compatible repo。
- 自动开发文档回路：用户维护理想态，治理流程根据 live repo truth 自动刷新当前状态摘要、差距和下一轮 Agent prompt。
- 全量文档组合审计：逐个评估 `README*` 与 `docs/**/*.md`，让每份长期文档只有唯一任务和定位，并清理、归档或 tombstone stale pollution。
- Active Truth plan 推荐模板：当目标 repo 没有稳定 active owner 时，给当前状态摘要、功能/结构差距、测试/证据差距、下一轮 Agent prompt 和 foldback target 一个最小形状。
- 轻量 doctor guard：只提示结构风险；Active Truth 内容治理由 Codex 按 skill 和 live repo truth 主动判断。
- no-second-truth 边界：doctor、native profile 和 family-plan 都是 workflow / lightweight risk map / profile sync，不是 repo truth、runtime truth、domain truth、artifact authority、quality verdict、owner receipt、production readiness 或 Foundry Agent truth set。
- support / fork boundary 规则：`opl-doc` 是默认文档治理范围内的 workflow support repo，但不是 Foundry Agent truth owner。`opl-aion-shell`、`opl-hermes-shell` 和 embedded upstream shell body 仍是显式 extension 或 read-only fork-boundary surface，只有任务明确触及 shell carrier / fork inventory 时才纳入。
- 测试覆盖。

本仓不持有 OPL series 的 domain truth、runtime truth、quality verdict、artifact authority 或 owner receipt。
