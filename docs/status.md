# 当前状态

Owner: `One Person Lab`
Purpose: `status`
State: `active_truth`
Machine boundary: 本文是人读状态；当前行为以测试和 CLI 输出为准。

当前已落地：

- Live Evidence 后置 / 功能结构优先是 `opl-doc` 治理工作读法。普通治理先关闭文档结构、SSOT owner、Active Truth owner、taxonomy、tombstone/no-resurrection、native profile drift、doctor risk-map、family-plan workflow 和 verification hygiene 这类功能/结构缺口。目标 repo 的 runtime evidence、owner receipts、production readiness、release readiness、domain readiness、App release、Brand L5、真实项目运行或 support repo live install evidence 仍归后置 evidence / owner lane；它们不能反向阻塞可独立完成的文档结构治理，也不能由 doctor clean、native-check pass、family-plan 输出、Markdown 完整或 profile synced 替代。

- `skills/opl-doc/SKILL.md`：canonical Codex 使用入口。
- `docs/active/opl-doc-active-truth-plan.md`：support repo Active Truth owner，持有当前状态摘要、现状与理想态差距、下一轮 Agent prompt，以及 support repo coverage / next-scope foldback。
- `docs/history/` 中的 retired previous skill-name tombstone：已退役旧入口的 provenance；旧名不再作为 active skill、UI entry 或 workflow 暴露；`tests/test_install_local_plugin.py` 还会扫描 active plugin / skill / script / template surfaces，防止旧入口在非 history tombstone 或 negative guard 语境中复活。
- `scripts/opl_doc_doctor.py doctor`：单仓文档生命周期只读诊断，并报告目标 repo 自己已有的 agent guidance、canonical docs、machine truth surface 和验证入口。
- `scripts/opl_doc_doctor.py`：现在只是仓内命令 bootstrap；doctor 实现和 import API 归 `scripts/opl_doc_doctor_parts/` 中的 profile discovery、invariant checks、plugin-native profile sync、family-plan generation、CLI parsing 和 report rendering 分层维护。
- `scripts/opl_doc_doctor.py doctor`：保持轻量，只报告 missing canonical docs、lifecycle header、legacy active wording、长清单风险和 repo-native verification surface；Active Truth 语义判断由 Codex 按 skill 读取 live repo truth 后执行。
- skill 现在明确禁止 doctor-driven 治理：doctor 只做预检风险地图；文档内容必须由 Codex 读取 source/contracts/tests/CLI-read-model/runtime ledger/receipt/blocker 和 docs 后逐段语义审计并重写。
- skill 现在要求治理整个文档组合：逐个审计 `README*` 与 `docs/**/*.md`，根据 live repo truth 判断每个 section 是当前事实、active gap、支撑参考、过程历史、退役 tombstone 还是 stale pollution。
- skill 现在把文档治理固定为 SSOT-first 内容级合并：每个语义主题先确定 Single Source of Truth，再让 peer docs 删除重复、收薄成指针、纳入细节、归档历史或清理 stale pollution；不能按文件名、目录或最近编辑时间机械合并。
- skill 现在把一文一责作为 closeout 门槛：每份长期文档只能保留一个任务和定位；混合职责内容必须移动到 canonical owner、history/tombstone，或直接删除。
- skill 现在把 gap 文档固定为 active tracker：理想态文档继续定义目标，active gap / active truth plan 只保留仍开放的当前 gap、后置 evidence 指针、forbidden claims 和下一轮 fresh-audit baton；功能/结构 gap 落地后删除或重写 active 条目，当前没有 gap 时保持薄 no-gap/current-state 读法，已完成过程进入 history/provenance。
- `scripts/opl_doc_doctor.py family-plan`：OPL series 治理工作流生成，默认覆盖 `one-person-lab`、`one-person-lab-app`、`opl-native-workbench`、`opl-flow`、`opl-doc`、`med-autoscience`、`med-autogrant`、`redcube-ai`、`opl-meta-agent`、`opl-bookforge`、`mas-scholar-skills`，并可通过 `--repo ID=PATH` 扩展到其他 OPL-compatible repo。
- `contracts/support-repo-policy.json`：upstream shell support extension-only 边界的 machine-readable policy。`family-plan` 的 `support_repo_policy` 从同一 source 生成，并带 no-resurrection guard，防止 `opl-aion-shell` 被误并入默认 11 仓 governed repo set 或 Foundry Agent truth set；该合同仍只声明 workflow/support 边界，不持有任何目标 repo truth、runtime truth、owner receipt 或 production readiness。
- `contracts/support-repo-policy.json` 是唯一 canonical support policy path；旧 underscore 形态 `contracts/support_repo_policy.json` 是 forbidden legacy ref，不创建 alias 文件。`family-plan` 的 `support_repo_policy` 和 `support_profile_guard` 均输出 canonical path、forbidden legacy ref 与 `legacy_contract_ref_alias_allowed=false`，防止 cross-repo backlog 或 support profile readback 把旧路径复活成第二合同真相。
- `scripts/opl_doc_doctor.py family-plan` 现在还输出 `support_profile_guard` 和 `support_profile_guard_audit`：guard 声明 materialized support profile 只允许 profile sync / workflow plan / no-resurrection guard 角色；audit 从 `contracts/opl-native-profile.json`、`contracts/support-repo-policy.json`、默认 governed repo set 和 filesystem legacy-ref absence 派生 7 项检查，确保 support repos 不进入默认 Foundry Agent truth set、旧 `contracts/support_repo_policy.json` 未复活、false-ready flags fail closed。它们都不能替代 repo/domain/runtime truth、创建第二 active backlog、声明 owner receipt / quality verdict / production readiness，或把 native-check / family-plan / doctor clean 包装成 ready。
- `scripts/opl_doc_doctor.py support-profile-check . --format json`：support profile / no-resurrection strict readback 入口，直接执行同一 `support_profile_guard_audit` 并在任一检查失败时非零退出。`scripts/verify.sh support-profile:strict` 调用该入口和 `git diff --check`，默认 `scripts/verify.sh` 也会执行该 readback。它只证明本 support repo 的 profile/workflow guard 未把 `opl-aion-shell` 或旧 underscore policy ref 复活成默认 Foundry Agent truth；不声明目标 repo truth、owner receipt、quality verdict、production readiness 或全局 goal complete。
- `scripts/opl_doc_doctor.py family-plan`：现在输出由 `contracts/support-repo-policy.json` 同源派生的 `support_repo_policy`，把 `opl-aion-shell` 标为 upstream shell explicit extension；默认 governed repo set 是 11 个可维护 repo / 22 个主参考文档，upstream shell repos 不进入默认 Foundry Agent truth set。
- `scripts/opl_doc_doctor.py native-check|native-sync`：目标 repo 的 plugin-native profile 检查/同步入口；`native-check --format json` 现在同时 materialize `support_repo_policy`、`support_profile_guard` 和 `support_profile_guard_audit`，让 profile drift 读面直接携带 support repo extension-only / no-resurrection guard；`native-sync --apply` 只写 `contracts/opl-native-profile.json`，用于声明 repo profile、OPL Flow / OPL Doc profile、Active Truth owner、canonical docs、taxonomy dirs、machine truth surfaces、repo-owned paths 和验证入口。
- `contracts/opl-native-profile.json`：本 support repo 已提交自己的 OPL-native profile declaration，默认验证使用 `native-check .` 防止 drift；该 profile 管理 `contracts/opl-native-profile.json` 与 `contracts/support-repo-policy.json`，只声明插件同步和 support-repo 边界，不成为 repo truth、Foundry Agent truth、runtime truth 或 production readiness。
- `doctor` / `native profile` / `family-plan` 现在共同投影 no-authority boundary：它们只做 lightweight risk map、profile sync / drift check、support/no-resurrection readback 和 workflow plan，不持有 repo truth、runtime truth、domain truth、artifact authority、quality verdict、owner receipt、production readiness 或 Foundry Agent truth set。
- `scripts/verify.sh`：默认验证现在把 Python bytecode、pytest cache 和临时产物导向仓库外部 `OPL_DOC_REPO_TEMP_ROOT`；`scripts/opl_doc_doctor.py` 在导入实现模块前禁用 bytecode 写入，`pyproject.toml` 禁用 pytest cache provider。单独运行 pytest 时仍应显式使用 `PYTHONDONTWRITEBYTECODE=1`，不能把裸 `python3 -m pytest` 当作不污染 checkout 的入口。
- `scripts/install_local_plugin.py --verify-only`：新机器安装后的本地插件、marketplace、`opl-doc` 短入口和 `opl-doc-doctor` 命令验证入口。
- `family-plan` 默认把 11 个可维护 repo 的 ideal-state reference 与 single Active Truth plan 作为 22 个主参考文档；旧的 7 仓/14 文档范围只在用户显式缩小到核心 agent set 时使用。
- `family-plan` 的完成门槛包含每个治理 repo 都要从 live repo truth 重写当前状态摘要、现状与理想态差距、下一轮 Agent prompt。
- `family-plan` 现在输出 SSOT-first semantic consolidation workflow：治理前必须确定语义主题、SSOT owner、peer docs 和 section 分类，完成门槛包含每个语义主题只有一个 documented SSOT owner。
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
- 不能把 `family-plan` 的默认 repo 列表写成 OPL family truth owner set；support repos 只是 extension，当前事实仍回各 repo canonical docs、contracts、tests、runtime ledger、receipt 和 blocker。
