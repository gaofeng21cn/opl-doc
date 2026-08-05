# OPL Doc active truth plan

Owner: `OPL Doc`
Purpose: `active_truth_plan`
State: `active_plan`
Machine boundary: 本文是人读 current-state / gap / next-audit baton；机器真相以 `.codex-plugin/plugin.json`、contracts、skill、源码、测试和 repo-native verification 输出为准。

## Ideal-State Reference

- Canonical target: `skills/opl-doc/SKILL.md`。
- Durable current status: `docs/status.md`。
- Invariants: `docs/invariants.md`，尤其是 no-second-truth、support extension、whole-portfolio audit、batch gate、tranche/global-goal 分离和无兼容面退役。

## Active Owner Discovery

本文是本仓唯一 Active Truth owner。`docs/status.md` 持有 durable current facts；`docs/history/` 只保存退役 provenance。当前没有第二份 active plan 或竞争 owner。

## Current State Summary

- canonical skill、只读 doctor、native profile sync、dynamic family-plan、support policy/no-resurrection guard、repo-temp verification、governance worklist/batch gate 和 remote readback discipline 均有 source/tests/contracts owner。
- Current selected functional / structural gap: `none`。
- installer live verification 与 profile materialization 是对应写集触发后的验证 lane，不是常驻 gap。
- doctor、native profile、family-plan 与本仓测试只证明 OPL Doc 自身治理面，不证明目标 repo、runtime、domain、release、owner acceptance 或全局 OPL family complete。

## Current-State vs Ideal-State Gaps

没有从 fresh source、tests、CLI、contracts 或 docs truth 证实的 repo-local 功能/结构 gap。新 gap 必须先给出真实 owner surface、当前断点、精确 write set 和可复现验证；不得从旧完成行、doctor warning、缺少 live install 或一次外部 repo 未同步制造 backlog。

## Next-Round Agent Prompt

Objective:

- 从 fresh OPL Doc source/contracts/tests/CLI 重新审计当前 ideal state，只选择有证据且满足批次门禁的治理 gap；没有安全批次时输出 `no_safe_batch_matrix`。

Write scope:

- 只写被新 gap 直接影响的 `skills/opl-doc/SKILL.md`、`scripts/opl_doc_doctor_parts/`、contracts、tests、canonical docs 与本计划。

Non-goals:

- 不把 support repo 纳入默认 Foundry Agent truth set；不恢复旧 skill 名、installer cleanup hook、alias、facade、wrapper 或第二 truth；不写目标 repo truth、owner receipt 或 readiness claim。

Live truth inputs:

- `AGENTS.md`、`.codex-plugin/plugin.json`、`contracts/`、`skills/opl-doc/SKILL.md`、`scripts/opl_doc_doctor.py`、`scripts/opl_doc_doctor_parts/`、`scripts/install_local_plugin.py`、`tests/` 和 canonical docs。

Required actions:

- fresh 检查 branch/head/dirty/worktree/remote/owner write set；先建 authority-aware worklist；按 semantic owner 实现最小安全批次；删除已关闭 gap 与过程流水；只把 durable fact 折回 canonical owner。

Verification commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor . --format json
python3 scripts/opl_doc_doctor.py support-profile-check . --format json
python3 scripts/opl_doc_doctor.py family-plan --format markdown
python3 scripts/opl_doc_doctor.py native-check .
bash scripts/verify.sh
git diff --check
```

Completion gate:

- 每个变更 claim 有 source/test/CLI/contract evidence；active plan 只保留 current gap 与下一 baton；最终 `main` bytes 验证、push 与远端 ref 回读完成，任务自有临时面已清理。单轮 tranche 不关闭仍有未覆盖文档的全局 goal。

Foldback target:

- durable current fact 进入 `docs/status.md` 或对应 machine owner；退役 provenance 进入 `docs/history/`；当前 gap 与下一轮入口只留本文。

## History / Tombstone Foldback

退役旧 skill 名、installer cleanup tail、doctor entrypoint re-export 与 package-root facade 的记录继续留在 `docs/history/`。active source/tests 只保留 no-resurrection guard，不保存其执行流水或重新暴露兼容入口。
