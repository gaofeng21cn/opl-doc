# 硬约束

Owner: `One Person Lab`
Purpose: `invariants`
State: `active_truth`
Machine boundary: 本文是人读硬约束；守门以测试和 review 执行。

1. 本仓只治理开发相关文档生命周期和工程闭环。
2. 不替代任何 domain repo 的 truth、quality verdict、artifact authority 或 owner receipt。
3. OPL series 文件治理不迁移到 OpenArc/OpenSpec/Spec Kit 默认路径。
4. active docs 是当前唯一 Active Truth 的重写面，表达当前完成进度、当前差距和下一轮 Agent prompt；过程材料进入 history；退役内容进入 tombstone/provenance。
5. 已退役模块、接口、测试和文档入口不保留兼容 alias。
6. Markdown 完整性不能替代 contracts、tests、CLI/read-model 或 runtime ledger。
7. doctor 默认只读，不能写目标 repo。
8. repo-native 指读取目标 repo 自己已有的开发入口，不指向目标 repo 安装本仓 CLI 或生成治理工具目录。
9. OPL family 自动开发治理必须把 ideal-state reference 当输入，把当前完成进度、现状与理想态差距、下一轮 Agent prompt 当派生输出；不能让用户手工维护这些派生状态。
10. active docs 不能保存执行日志、时间线、完成流水或长历史清单；这些内容只能压缩进入 history/tombstone，以免污染 Active Truth。
11. 正式治理必须覆盖 `README*` 与 `docs/**/*.md` 的实质内容审计；不能只整理 active gap 文档或只修 doctor findings。
12. 每份长期文档必须只有一个 owner、purpose、state 和 machine boundary；同一文档混合多个职责时必须拆分、迁移、归档、tombstone 或删除。
13. 过时模块、接口、测试、文档、workflow 和入口在 replacement 与 no-active-caller 证据成立后直接退役；不新增 facade、wrapper、兼容 prose 或旧路线复活文案。
14. 默认 OPL series 治理范围是 6 个 repo 和 12 个主参考文档；除非用户显式缩小范围，不得退回旧的 5 仓/10 文档范围。
15. 长线治理必须区分本轮 tranche closeout 与全局 `/goal` 完成；coverage ledger 仍有未覆盖文档、未折回 stale/retire 候选或未完成 gap 时，不得把全局目标标记 complete。
16. doctor、native profile 和 family-plan 只能作为 workflow / lightweight risk map / profile sync；不得写成 repo truth、runtime truth、domain truth、artifact authority、quality verdict、owner receipt、production readiness 或 Foundry Agent truth set。
17. `opl-doc`、`opl-aion-shell` 等 support repo 默认是 extension。除非用户显式要求或当前任务触及 support repo，本仓不得把它们加入默认 governed Foundry Agent truth owner 集合。
18. OPL series 根层 `README*` 面向用户，默认采用问题、价值、场景、开始方式和效果的叙事；`executor-first`、stage、route、receipt、typed blocker、Tool Affordance Boundary、domain truth、quality verdict 等技术边界只放在折叠的 Agent / 开发者 / operator 区或 canonical 技术文档。
