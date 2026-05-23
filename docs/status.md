# 当前状态

Owner: `One Person Lab`
Purpose: `status`
State: `active_truth`
Machine boundary: 本文是人读状态；当前行为以测试和 CLI 输出为准。

当前已落地：

- `skills/opl-doc-governance/SKILL.md`：Codex 使用入口。
- `scripts/opl_doc_doctor.py doctor`：单仓文档生命周期只读诊断。
- `scripts/opl_doc_doctor.py init-repo`：在目标 repo 写入 `.opl-doc-governance/` 本地治理入口，让后续 agent 可从 repo 内发现文档生命周期规则。
- `scripts/opl_doc_doctor.py family-plan`：OPL series 治理工作流生成，默认覆盖 `one-person-lab`、`med-autoscience`、`med-autogrant`、`redcube-ai`、`opl-meta-agent`，并可通过 `--repo ID=PATH` 扩展到其他 OPL-compatible repo。
- `goal_mode`：OPL series、多仓、长周期或会修改文档的治理请求会主动创建或延续 `/goal`，不要求用户额外记忆长提示词。
- `tests/test_opl_doc_doctor.py`：profile、repo-native init、legacy 词、history 例外、family workflow 测试。

当前不能声明：

- 不能把 doctor 无 warning 写成 repo 已生产 ready。
- 不能把文档完整性写成 contracts/tests/read-model 已一致。
- 不能用本仓替代 OPL series 各 repo 的 canonical docs。
