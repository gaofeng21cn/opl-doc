# 架构

Owner: `One Person Lab`
Purpose: `architecture`
State: `active_truth`
Machine boundary: 本文是人读架构；可执行命令行为以 `scripts/opl_doc_doctor.py` 和 skill 为准，doctor import API 以 `scripts/opl_doc_doctor_parts/` 为准。

## 分层

1. Skill 层
   - 给 Codex 提供文档生命周期工作流、OPL series治理规则和硬边界。
2. Doctor 层
   - 只读扫描 repo docs，输出 profile、repo-native surfaces、canonical docs 状态和轻量 findings。
3. Repo-native profile 层
   - 通过 `native-check` / `native-sync` 读取或写入目标 repo 的 `contracts/opl-native-profile.json`，让 repo 声明采用哪个 OPL Flow / OPL Doc profile、Active Truth owner、canonical docs、taxonomy dirs、machine truth surfaces 与验证入口。
   - 该 profile 只服务插件发现、同步和 drift 检查，不成为 repo truth、domain truth、runtime truth、artifact authority、quality verdict、owner receipt 或 production readiness。
4. Repo-native surface 层
   - 识别目标 repo 自己已有的 agent guidance、canonical docs、machine truth surface 和验证入口，不向目标 repo 安装治理工具。
5. Change packet 层
   - 为非平凡开发提供 active change 包，完成后 fold back 到 canonical docs 或 history。
6. Verification 层
   - 通过 repo-native 测试、diff check、doctor 输出和最终 main checkout 验证闭环。
7. Support extension 层
   - `family-plan` 默认治理 11 个 OPL series 可维护 repo。`opl-aion-shell` 等 upstream shell repo 只在用户显式要求或当前任务触及 shell carrier / support docs 时作为 extension 纳入；它们不是默认 Foundry Agent truth set。
   - `contracts/support-repo-policy.json` 物化这条 support-extension policy；`family-plan` 从同一 source 派生 `support_repo_policy`，native profile 把该合同列为插件管理面。该合同是 no-resurrection / no-second-truth guard，不是目标 repo truth 或 Foundry Agent truth owner 集合。

## 自动开发文档回路

用户只需要维护 ideal-state / target-state reference。治理流程必须从 live source、contracts、tests、CLI/read-model 和当前 docs 中重写三个派生输出：当前状态摘要、现状与理想态差距、下一轮 Agent prompt。通常落点是各 repo 的 single Active Truth plan；若 repo 使用其他 canonical active plan，需要显式映射，不能新增第二套计划文档。

当目标 repo 缺少稳定 active owner 时，skill 可使用 `templates/active-truth-plan.md` 的最小形状：ideal-state reference、current state summary、functional/structural gaps、test/evidence gaps、next-round Agent prompt 和 history/tombstone foldback。该模板只定义文档形状，不承担语义判断。

CLI 不承担 Active Truth 语义治理。doctor 只提示明显结构风险；`native-sync` 只维护 `contracts/opl-native-profile.json` 这种同步声明；`family-plan` 只生成 workflow map 和 coverage discipline。真正的文档内容判断由 Codex 按 skill 读取 live repo truth、ideal-state reference、active plan 和 machine-readable evidence 后执行。

## 文档组合审计

正式治理的语义范围覆盖目标 repo 的 `README*` 与 `docs/**/*.md`。active truth owner 只承载当前状态摘要、当前差距和下一轮 Agent prompt；其他文档按唯一任务分层：canonical current truth、public narrative、product/runtime/source/delivery support、policy/spec/reference、history 或 tombstone。

治理流程逐段比较文档 claim 与 live repo truth。当前事实折回 canonical owner；active work 留在 single Active Truth plan；支撑材料进入对应 support 层；过程材料进入 history；退役 surface 进入 tombstone/provenance；没有当前角色的旧内容直接删除。历史增量长清单应折叠成当前状态表、剩余 gap 和 history pointer。

治理流程按语义主题选择 Single Source of Truth，再处理 peer docs。每个主题只能有一个当前 owner；其他文档只保留入口摘要、指针、独有支撑细节、machine-boundary notes 或 history/provenance。无法确定 SSOT 时，不做大规模合并或删除，而是记录冲突、缺失证据和 next owner。

过时模块、接口、测试、文档、workflow 和入口不通过兼容层延长寿命。只要 replacement 与 no-active-caller 证据成立，skill 指导代理直接退役并同步文档，不新增 alias、facade、wrapper 或旧路线复活叙述。

## 边界

doctor 只读，不执行清理、不修改目标仓、不生成 owner receipt。`native-sync --apply` 只允许写目标仓的 `contracts/opl-native-profile.json`，用于插件原生升级和 drift 检查。本仓的 `contracts/support-repo-policy.json` 只约束 OPL Doc 自身如何把 support repos 保持为 explicit extension。`family-plan` 不生成 repo truth、runtime truth、domain truth、artifact authority、quality verdict、owner receipt 或 Foundry Agent truth owner set。skill 可以指导 Codex 修改目标仓文档，但必须先读取目标 repo 约束并运行对应验证。
