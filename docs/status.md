# 当前状态

Owner: `One Person Lab`
Purpose: `status`
State: `active_truth`
Machine boundary: 本文是人读状态摘要；当前行为以 contracts、源码、测试和 CLI 输出为准。

## 当前维护面

- `skills/opl-doc/SKILL.md` 是 canonical 治理入口，定义 SSOT-first 语义合并、全量文档组合审计、Active Truth 收薄、批次门禁、coverage ledger 与过时面退役规则。
- `scripts/opl_doc_doctor.py` 只负责命令 bootstrap；`scripts/opl_doc_doctor_parts/` 分别持有 profile discovery、只读 doctor、native profile sync、family-plan、CLI 与 rendering 实现。
- doctor 只输出风险地图，`native-check|native-sync` 只校验或物化 `contracts/opl-native-profile.json`，`family-plan` 只输出治理 workflow；三者都不能替代目标 repo truth。
- `contracts/support-repo-policy.json` 是 support extension/no-resurrection 的唯一机器合同；旧 `contracts/support_repo_policy.json` 不存在且不得恢复为 alias。
- `family-plan --workspace-root` 从真实 Git 根仓、repo-local owner 标识与 canonical GitHub owner 发现本轮范围；内置 11 仓/22 个概念参考只是 workflow baseline，已退役或不存在仓库不形成 backlog，Aion/Hermes 等 shell repo 默认只读扩展。
- `scripts/verify.sh`、`tests/test_opl_doc_doctor.py` 与 `tests/test_install_local_plugin.py` 守住命令行为、profile/support policy、退役旧入口与 facade 的 no-resurrection 边界。

## 当前治理状态

当前没有从 fresh source、tests、CLI 或 contracts 证实的 repo-local 功能/结构 gap。
[Active Truth plan](./active/opl-doc-active-truth-plan.md) 只维护 no-gap 判断、条件触发的下一轮审计入口与禁止声明；已落地能力的详细定义归 skill、contracts、源码、测试和本页，不在 active plan 保存完成台账。

用户级 install 校验只在 installer/sync 写集实际变化时运行；`native-sync --apply` 也只在 profile source 变化时执行。未触发这些写集不是 evidence gap，更不表示 live install、外部 repo sync 或目标 repo readiness 已证明。

退役旧 skill 名、installer cleanup tail、doctor entrypoint re-export 与 package-root facade 的 provenance 留在 `docs/history/`；active source/tests 只保留 no-resurrection guard，不恢复兼容入口。

## 权威边界

OPL Doc 不持有目标 repo 的 runtime/domain truth、artifact authority、quality verdict、owner receipt、release/production readiness 或 Foundry Agent truth set。doctor clean、profile synced、family-plan 输出、Markdown 完整、focused tests、commit/push 或 clean tracking ref 都不能推出这些结论。

## 验证入口

```bash
python3 scripts/opl_doc_doctor.py doctor . --format json
python3 scripts/opl_doc_doctor.py support-profile-check . --format json
python3 scripts/opl_doc_doctor.py family-plan --workspace-root /Users/gaofeng/workspace --format json
python3 scripts/opl_doc_doctor.py native-check .
bash scripts/verify.sh
```

涉及 installer 或 profile materialization 的实际变更时，再分别运行 `python3 scripts/install_local_plugin.py --verify-only` 或 `native-sync --dry-run|--apply`，并以变更后的最终 bytes 重跑默认验证。
