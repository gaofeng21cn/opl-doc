# 当前状态

Owner: `One Person Lab`
Purpose: `status`
State: `active_truth`
Machine boundary: 本文是人读状态；当前行为以测试和 CLI 输出为准。

当前已落地：

- `skills/opl-doc-governance/SKILL.md`：Codex 使用入口。
- `scripts/opl_doc_doctor.py doctor`：单仓文档生命周期只读诊断，并报告目标 repo 自己已有的 agent guidance、canonical docs、machine truth surface 和验证入口。
- `scripts/opl_doc_doctor.py doctor`：保持轻量，只报告 missing canonical docs、lifecycle header、legacy active wording、长清单风险和 repo-native verification surface；Active Truth 语义判断由 Codex 按 skill 读取 live repo truth 后执行。
- `scripts/opl_doc_doctor.py family-plan`：OPL series 治理工作流生成，默认覆盖 `one-person-lab`、`med-autoscience`、`med-autogrant`、`redcube-ai`、`opl-meta-agent`，并可通过 `--repo ID=PATH` 扩展到其他 OPL-compatible repo。
- `family-plan` 的完成门槛包含每个治理 repo 都要从 live repo truth 重写当前完成进度、现状与理想态差距、下一轮 Agent prompt。
- `templates/active-truth-plan.md`：single Active Truth plan 推荐形状；用于缺少稳定 active owner 的 repo，不替代已有 canonical active plan，并要求下一轮 prompt 可直接作为 `/goal` 或长线 Codex prompt 使用。
- skill 已明确 active owner 发现顺序、章节路由表和 foldback closeout 检查，避免把完成过程包、closed gap 或 stale wording 留在 active path。
- `goal_mode`：OPL series、多仓、长周期或会修改文档的治理请求会主动创建或延续 `/goal`，不要求用户额外记忆长提示词。
- `tests/test_opl_doc_doctor.py`：profile、repo-native surface 检测、legacy 词、history 例外、family workflow 测试。

当前不能声明：

- 不能把 doctor 无 warning 写成 repo 已生产 ready。
- 不能把文档完整性写成 contracts/tests/read-model 已一致。
- 不能用本仓替代 OPL series 各 repo 的 canonical docs。
