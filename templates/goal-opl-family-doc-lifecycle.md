# OPL Series Docs Lifecycle Goal

使用 OPL Doc Governance，在 `one-person-lab`、`med-autoscience`、`med-autogrant`、`redcube-ai`、`opl-meta-agent` 及后续纳入的 OPL-compatible repo 执行文档生命周期治理。

执行代理应自动创建或延续 `/goal`，用户只需要说“使用 OPL Doc Governance 治理 OPL series 的开发文档生命周期”。

以 OPL series 各 repo 的理想情况、差距及完善计划为主要参考，根据现在各个 repo 代码、contracts、tests、CLI/read-model 和 docs 的实际情况，逐条评估各个 repo `README*` 与 `docs/**/*.md` 下其他所有文档。

目标：

- 清理和归档已经过时的内容，避免二次污染。
- 优化文档生命周期管理，让每个文档都有唯一任务和定位。
- 保证不同文档之间分层、分工明确，不互相打架。
- 将按历史增量堆叠的长清单折叠成当前状态表、active gap 和 history pointer。
- 对已经过时的模块、接口、测试和文档入口，按理想态直接退役清理，不保留兼容面、alias、facade 或 wrapper。
- 明确区分功能/结构差距与测试/证据差距；不能把 evidence tail 写成“功能未实现”，也不能把文档整齐写成 production ready。
- 保持 OPL-native taxonomy，不迁移到 OpenArc、OpenSpec、Spec Kit 或其他外部文件框架。

工作方式：

- 每个 repo 先读根层 `AGENTS.md`，存在 `TASTE.md` 时先按当前 `TASTE.md` 校准。
- 读 canonical docs：`README*`、`docs/README*`、`docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`。
- 读 active/gap/ideal-state docs，并用 live source/contracts/tests/read-model 验证重要断言。
- 可以用 subagent 并行开多个 worktree 推进，但每条线必须有清晰 write scope。
- 每条线完成后跑新鲜验证，提交，吸收回 `main`，删除对应 worktree/branch。
- 最终在 `main` 上再次验证，并更新 canonical docs、history/tombstone 和必要的 contracts/read-model references。

完成口径：

- canonical docs 只表达当前事实。
- active docs 只保留当前计划、差距和 baton。
- history/tombstone 承接过程材料和退役语义。
- prose 文档不与 contracts、tests、CLI/read-model 矛盾。
- 没有新增兼容污染面或旧路线复活文案。
- 最终 main checkout 验证通过，且临时 worktree/branch 已清理。
