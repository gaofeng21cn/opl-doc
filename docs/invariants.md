# 硬约束

Owner: `One Person Lab`
Purpose: `invariants`
State: `active_truth`
Machine boundary: 本文是人读硬约束；守门以测试和 review 执行。

1. 本仓只治理开发相关文档生命周期和工程闭环。
2. 不替代任何 domain repo 的 truth、quality verdict、artifact authority 或 owner receipt。
3. OPL series 文件治理不迁移到 OpenArc/OpenSpec/Spec Kit 默认路径。
4. active docs 是当前唯一 Active Truth 的重写面，表达当前状态摘要、当前差距和下一轮 Agent prompt；过程材料进入 history；退役内容进入 tombstone/provenance。
5. 已退役模块、接口、测试和文档入口不保留兼容 alias。
6. Markdown 完整性不能替代 contracts、tests、CLI/read-model 或 runtime ledger。
7. doctor 默认只读，不能写目标 repo。
8. repo-native 指读取目标 repo 自己已有的开发入口，不指向目标 repo 安装本仓 CLI 或生成治理工具目录。
9. OPL family 自动开发治理必须把 ideal-state reference 当输入，把当前状态摘要、现状与理想态差距、下一轮 Agent prompt 当派生输出；不能让用户手工维护这些派生状态。
10. active docs 不能保存执行日志、时间线、完成流水或长历史清单；这些内容只能压缩进入 history/tombstone，以免污染 Active Truth。
11. 正式治理必须覆盖 `README*` 与 `docs/**/*.md` 的实质内容审计；不能只整理 active gap 文档或只修 doctor findings。
12. 文档治理必须先按语义主题确定 Single Source of Truth，再按内容段落合并、删除、归档、收薄或纳入细节；不得按文件名、目录相邻、篇幅、重复次数或最近编辑时间决定真相 owner。
13. 每份长期文档必须只有一个 owner、purpose、state 和 machine boundary；同一文档混合多个职责时必须拆分、迁移、归档、tombstone 或删除。
14. 过时模块、接口、测试、文档、workflow 和入口在 replacement 与 no-active-caller 证据成立后直接退役；不新增 facade、wrapper、兼容 prose 或旧路线复活文案。
15. 默认 OPL series 治理范围是 11 个可维护 repo 和 22 个主参考文档；除非用户显式缩小范围，不得退回旧的 7 仓/14 文档范围。
16. 长线治理必须区分本轮 tranche closeout 与全局 `/goal` 完成；coverage ledger 仍有未覆盖文档、未折回 stale/retire 候选或未完成 gap 时，不得把全局目标标记 complete。
17. doctor、native profile 和 family-plan 只能作为 workflow / lightweight risk map / profile sync；不得写成 repo truth、runtime truth、domain truth、artifact authority、quality verdict、owner receipt、production readiness 或 Foundry Agent truth set。
18. `opl-doc`、`opl-aion-shell` 等 support repo 默认是 extension。除非用户显式要求或当前任务触及 support repo，本仓不得把它们加入默认 governed Foundry Agent truth owner 集合。
19. OPL series 根层 `README*` 面向用户，默认采用问题、价值、场景、开始方式和效果的叙事；`executor-first`、stage、route、receipt、typed blocker、Tool Affordance Boundary、domain truth、quality verdict 等技术边界只放在折叠的 Agent / 开发者 / operator 区或 canonical 技术文档。
20. Live Evidence 后置是文档治理基本原则。治理工作先关闭结构/功能缺口：SSOT owner、Active Truth owner、taxonomy、section classification、stale prose retirement、tombstone/no-resurrection、native profile drift、doctor risk map、family-plan workflow 和 verification hygiene。目标 repo 的 runtime evidence、owner receipt、domain/App/brand readiness、release/production evidence、真实项目 evidence 或 support repo live install evidence 只能作为后置 evidence / owner lane；除非它们正在保护 authority、不可逆 mutation、ready claim、release claim 或 owner receipt，否则不得阻塞文档结构治理。doctor clean、native-check pass、family-plan 输出、Markdown 完整、profile synced 或 docs foldback 也不得替代目标 repo ready claim。
21. Gap 文档是 active tracker，不是完成史。理想态文档继续定义目标；active gap / active truth plan 只保留仍开放的当前 gap、后置 evidence 指针、forbidden claims 和下一轮 fresh-audit baton。功能/结构 gap 落地后必须删除或重写 active 条目；当前没有 gap 时，active plan 应保持薄 no-gap/current-state 读法。已完成调研、规划、closeout、branch/worktree、receipt 流水和验证过程进入 history/provenance、owner ledger 或提交历史。
22. 多仓或长线治理在修改前必须先形成 `governance_worklist` / authority-aware matrix，候选需声明 truth owner、owner surface、route、doc lifecycle、authority blocker、allowed/forbidden write set、验证命令、parallel group 和状态；不得从单个文件、单个 doctor warning 或单条 stale phrase 直接开改。
23. 治理 tranche 必须满足最小有效批次门：默认选择 3-7 个安全 SSOT/docs 项或 2-5 个结构项；只有一个低价值小切片时输出 `no_safe_batch_matrix` 并结转，除非它是 P0 stale-lane cleanup、阻断性 SSOT 冲突或用户明确指定的单点修复。
24. 上游 fork 主体和 support repo extension 不是治理/重构压力来源；`opl-hermes-shell/**`、`opl-aion-shell/**`、`one-person-lab-app/shells/aionui/**`、`one-person-lab-app/_external/hermes-agent/**` 默认只能 read-only 盘点 owner/fork 边界，命中候选必须标 `not_safe` 或 `blocked_owner_gated`，原因写 `upstream_fork_excluded`。
