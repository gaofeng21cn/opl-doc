# OPL Series Docs Lifecycle Goal

使用 OPL Doc，在 `one-person-lab`、`med-autoscience`、`med-autogrant`、`redcube-ai`、`opl-meta-agent`、`opl-bookforge`、`one-person-lab-app` 及后续纳入的 OPL-compatible repo 执行文档生命周期治理。

执行代理应自动创建或延续 `/goal`，用户只需要说“使用 OPL Doc 治理 OPL series 的开发文档生命周期”。

默认 OPL series 范围是 7 个 repo；以各 repo 的理想情况和 single Active Truth plan 合计 14 个主参考文档为主要参考，根据现在各个 repo 代码、contracts、tests、CLI/read-model 和 docs 的实际情况，重写刷新各 repo 的当前完成进度、现状与理想态差距、下一轮 Agent prompt，并逐条评估各个 repo `README*` 与 `docs/**/*.md` 下其他所有文档。

目标：

- 清理和归档已经过时的内容，避免二次污染。
- 优化文档生命周期管理，让每个文档都有唯一任务和定位。
- 让用户只维护 ideal-state / target-state reference，治理流程自动维护完成进度、差距和下一轮 Agent prompt。
- 维护唯一 Active Truth / Single Source of Truth；active docs 是当前真相重写面，不是执行日志。
- 保证不同文档之间分层、分工明确，不互相打架。
- 将按历史增量堆叠的长清单折叠成当前状态表、active gap 和 history pointer。
- 对已经过时的模块、接口、测试和文档入口，按理想态直接退役清理，不保留兼容面、alias、facade 或 wrapper。
- 明确区分功能/结构差距与测试/证据差距；不能把 evidence tail 写成“功能未实现”，也不能把文档整齐写成 production ready。
- 保持 OPL-native taxonomy，不迁移到 OpenArc、OpenSpec、Spec Kit 或其他外部文件框架。
- 按 long-horizon tranche 续跑；本轮完成只表示本轮 verified / absorbed，不等于全局 `/goal` 完成。

工作方式：

- 每个 repo 先读根层 `AGENTS.md`，存在 `TASTE.md` 时先按当前 `TASTE.md` 校准。
- doctor 只作为预检风险地图；不能把 doctor findings 当成治理任务清单，不能只修 doctor 报的问题。
- 读 canonical docs：`README*`、`docs/README*`、`docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`。
- 读 single Active Truth plan 和 ideal-state reference，并用 live source/contracts/tests/read-model 验证重要断言。
- 对每个 active plan 和 canonical doc 的实质 claim 做 live truth 语义审计：读取 source、contracts、tests、package scripts、CLI/read-model 输出、runtime ledger、receipt 和 blocker，判断文档内容是当前事实、差距、证据尾项、历史 provenance 还是 stale pollution。
- 先发现 active truth owner：优先 repo 明示入口和 `docs/active/current-state-vs-ideal-gap.md`；多份 active plan 抢同一职责时保留 canonical owner，重写或退役重复文档。
- 如果某个 repo 缺少稳定 active truth owner，使用 OPL Doc 的 `templates/active-truth-plan.md` 作为章节形状；若已有 canonical active plan，则把同样章节映射进去，不新增第二套计划。
- 在 active plan 中重写三类派生输出：当前完成进度、现状与理想态差距、下一轮 Agent prompt；这个 prompt 就是下一轮 `/goal` 或长线 Codex 执行入口，不是普通 TODO。
- 逐段审阅 `README*` 和 `docs/**/*.md`，先按语义主题确定 Single Source of Truth，再把同主题材料分类为 canonical owner、covered_by_ssot support detail、conflict、stale pollution 或 history/provenance；根据 live truth 更新文档内容、合并重复职责、清理过时路径；不是只做结构扫描修复。
- 遇到重复章节时，优先保留当前 truth owner 中的唯一表述；support detail 只能指向 canonical owner，conflict/stale 内容直接重写、退役或归档，不保留 alias、facade、wrapper 或兼容说明。
- 下一轮 Agent prompt 必须能直接作为 `/goal` 或长线 Codex prompt 使用，并包含目标、写入范围、禁止范围、live truth 输入、必做动作、验证命令、完成口径和 foldback 目标。
- 开发完成后删除或重写已关闭 gap；执行流水、完成记录和弯路归入 `docs/history/` 或 tombstone/provenance。
- closeout 前检查：closed gap 已删除或重写、当前事实已折回 canonical docs、active path 不保留完成过程包、下一轮 prompt 只保留仍未完成的工作。
- 可以用 subagent 并行开多个 worktree 推进，但每条线必须有清晰 write scope。
- 每条线完成后跑新鲜验证，提交，吸收回 `main`，删除对应 worktree/branch。
- 每个 repo 维护 coverage ledger：已审文档/章节、已改文档、归档/tombstone/删除文档、未覆盖文档、剩余 stale/retire 候选和下一轮写入范围。
- 未覆盖文档清单、剩余 stale/retire 候选或未完成 gap 非空时，只能做 tranche closeout，并把剩余项折进下一轮 Agent prompt；不得把全局 `/goal` 标记 complete。
- 最终在 `main` 上再次验证，并更新 canonical docs、history/tombstone 和必要的 contracts/read-model references。

完成口径：

- canonical docs 只表达当前事实。
- active docs 只保留当前完成进度、差距和下一轮 Agent prompt。
- 每个治理 repo 都有从 live repo truth 重写刷新的当前完成进度、现状与理想态差距和下一轮 Agent prompt。
- history/tombstone 承接过程材料和退役语义。
- prose 文档不与 contracts、tests、CLI/read-model 矛盾。
- 没有新增兼容污染面或旧路线复活文案。
- 最终 main checkout 验证通过，且临时 worktree/branch 已清理。
- 全局完成还要求 7 个 repo 的 `README*` 与 `docs/**/*.md` 已逐段覆盖，coverage ledger 没有未覆盖文档或未折回的 stale/retire 候选。
