# 当前状态

Owner: `One Person Lab`
Purpose: `status`
State: `active_truth`
Machine boundary: 本文是人读状态；当前行为以测试和 CLI 输出为准。

当前已落地：

- `skills/opl-doc/SKILL.md`：canonical Codex 使用入口。
- `skills/opl-doc-governance/SKILL.md`：兼容 Codex 使用入口，继续支持既有直接调用。
- `scripts/opl_doc_doctor.py doctor`：单仓文档生命周期只读诊断，并报告目标 repo 自己已有的 agent guidance、canonical docs、machine truth surface 和验证入口。
- `scripts/opl_doc_doctor.py doctor`：保持轻量，只报告 missing canonical docs、lifecycle header、legacy active wording、长清单风险和 repo-native verification surface；Active Truth 语义判断由 Codex 按 skill 读取 live repo truth 后执行。
- skill 现在明确禁止 doctor-driven 治理：doctor 只做预检风险地图；文档内容必须由 Codex 读取 source/contracts/tests/CLI-read-model/runtime ledger/receipt/blocker 和 docs 后逐段语义审计并重写。
- skill 现在要求治理整个文档组合：逐个审计 `README*` 与 `docs/**/*.md`，根据 live repo truth 判断每个 section 是当前事实、active gap、支撑参考、过程历史、退役 tombstone 还是 stale pollution。
- skill 现在把一文一责作为 closeout 门槛：每份长期文档只能保留一个任务和定位；混合职责内容必须移动到 canonical owner、history/tombstone，或直接删除。
- `scripts/opl_doc_doctor.py family-plan`：OPL series 治理工作流生成，默认覆盖 `one-person-lab`、`med-autoscience`、`med-autogrant`、`redcube-ai`、`opl-meta-agent`、`one-person-lab-app`，并可通过 `--repo ID=PATH` 扩展到其他 OPL-compatible repo。
- `scripts/opl_doc_doctor.py native-check|native-sync`：目标 repo 的 plugin-native profile 检查/同步入口；`native-sync --apply` 只写 `contracts/opl-native-profile.json`，用于声明 repo profile、OPL Flow / OPL Doc profile、Active Truth owner、canonical docs、taxonomy dirs、machine truth surfaces、repo-owned paths 和验证入口。
- `scripts/install_local_plugin.py --verify-only`：新机器安装后的本地插件、marketplace、`opl-doc` 短入口和 `opl-doc-doctor` 命令验证入口。
- `family-plan` 默认把 6 个 repo 的 ideal-state reference 与 single Active Truth plan 作为 12 个主参考文档；旧的 5 仓/10 文档范围只在用户显式排除 App repo 时使用。
- `family-plan` 的完成门槛包含每个治理 repo 都要从 live repo truth 重写当前完成进度、现状与理想态差距、下一轮 Agent prompt。
- `family-plan` 明确区分 tranche closeout 和全局 `/goal` 完成：单轮 verified / absorbed 不能关闭全局目标，除非 coverage ledger 已覆盖所有 `README*` 与 `docs/**/*.md` 且剩余项已清空或折进下一轮 prompt。
- `templates/active-truth-plan.md`：single Active Truth plan 推荐形状；用于缺少稳定 active owner 的 repo，不替代已有 canonical active plan，并要求下一轮 prompt 可直接作为 `/goal` 或长线 Codex prompt 使用。
- skill 已明确 active owner 发现顺序、章节路由表和 foldback closeout 检查，避免把完成过程包、closed gap 或 stale wording 留在 active path。
- skill 已明确过时模块、接口、测试、文档、workflow 和入口在 replacement 与 no-active-caller 证据成立后直接退役，不新增 compatibility alias、facade、wrapper 或旧入口仍可用叙述。
- `goal_mode`：OPL series、多仓、长周期或会修改文档的治理请求会主动创建或延续 `/goal`，不要求用户额外记忆长提示词。
- `tests/test_opl_doc_doctor.py`：profile、repo-native surface 检测、legacy 词、history 例外、family workflow 测试。

当前不能声明：

- 不能把 doctor 无 warning 写成 repo 已生产 ready。
- 不能把文档完整性写成 contracts/tests/read-model 已一致。
- 不能用本仓替代 OPL series 各 repo 的 canonical docs。
- 不能把 `contracts/opl-native-profile.json` 写成 domain truth、runtime truth、artifact authority、quality verdict、owner receipt 或生产 ready 证据；它只是插件同步和 drift 检查声明。
