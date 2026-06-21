# OPL Doc active truth plan

Owner: `OPL Doc`
Purpose: `active_truth_plan`
State: `active_plan`
Machine boundary: 本文是人读开发计划与当前真相折返面；机器真相以 `.codex-plugin/plugin.json`、`skills/opl-doc/SKILL.md`、`scripts/opl_doc_doctor.py`、`scripts/opl_doc_doctor_parts/`、`scripts/install_local_plugin.py`、`tests/` 和 repo-native verification 输出为准。

## Ideal-State Reference

- Canonical target-state document: `skills/opl-doc/SKILL.md`
- Target-state summary: `opl-doc` 是 OPL-native 开发文档生命周期治理入口；doctor / native profile / family-plan 只提供 workflow、risk map 和 profile sync；正式治理必须从 live repo truth 出发，维护 Active Truth、coverage ledger、next-round prompt 和 stale-surface retirement。
- Non-negotiable invariants: `docs/invariants.md`，尤其是 no-second-truth、support repo extension、SSOT-first、whole-portfolio audit、tranche closeout 与 global goal 分离，以及退役旧模块/接口/测试/文档入口时不保留 alias / facade / wrapper / compatibility prose。

Live Evidence 后置是本文执行原则。`opl-doc` 的日常治理优先关闭功能/结构缺口：SSOT owner、Active Truth owner、taxonomy、section classification、stale prose retirement、tombstone/no-resurrection、native profile drift、doctor risk map、family-plan workflow 和 verification hygiene。目标 repo runtime evidence、owner receipt、domain/App/brand readiness、release/production evidence、真实项目 evidence 或 support repo live install evidence 是后置 evidence / owner lane；它们不能反向阻塞可独立完成的文档结构治理，也不能由 doctor clean、native-check pass、family-plan 输出、Markdown 完整、profile synced 或 docs foldback 替代为 ready claim。

## Active Owner Discovery

- Existing active truth owner: 本文。
- Duplicate or competing active docs to retire: 当前没有其他 `docs/active/*` active truth owner。
- Mapping note: 本仓此前由 `docs/status.md` 描述当前状态，但缺少 long-horizon active owner。`docs/status.md` 继续保留 durable current status；本文件持有当前完成进度、当前差距、下一轮 Agent prompt 和 coverage / next-scope foldback。

## Current Completion Progress

| Area | Current status | Live evidence | Notes |
| --- | --- | --- | --- |
| Canonical skill surface | done | `skills/opl-doc/SKILL.md`; `skills/opl-doc/agents/openai.yaml`; `tests/test_install_local_plugin.py` | Active skill name is `opl-doc`; the retired previous skill name is history-only, with a no-resurrection test scanning active plugin / skill / script / template surfaces. |
| Doctor CLI split | done | `scripts/opl_doc_doctor.py`; `scripts/opl_doc_doctor_parts/`; `tests/test_opl_doc_doctor.py`; `docs/history/opl-doc-doctor-entrypoint-facade-retirement.md`; `docs/history/opl-doc-doctor-parts-package-facade-retirement.md` | Command bootstrap and implementation modules are separated; old broad import facades are retired. |
| Local installer surface | done | `scripts/install_local_plugin.py`; `tests/test_install_local_plugin.py`; retired installer cleanup-tail tombstone in `docs/history/` | Installer installs only `opl-doc`, updates marketplace entry for `opl-doc`, and creates `opl-doc-doctor`; old-name cleanup tail is retired. |
| Family governance workflow | done | `scripts/opl_doc_doctor_parts/family_plan.py`; `templates/goal-opl-family-doc-lifecycle.md`; `tests/test_opl_doc_doctor.py` | Seven core repos are the default OPL series, now including OPL BookForge; support repos are explicit extension. |
| Native profile sync | done | `scripts/opl_doc_doctor_parts/plugin_sync.py`; `scripts/opl_doc_doctor_parts/profile_discovery.py`; `tests/test_opl_doc_doctor.py`; `docs/architecture.md` | `native-sync --apply` writes only `contracts/opl-native-profile.json` in a target repo; it does not create repo truth. |
| Support repo policy contract | done | `contracts/support-repo-policy.json`; `scripts/opl_doc_doctor_parts/constants.py`; `scripts/opl_doc_doctor_parts/family_plan.py`; `tests/test_opl_doc_doctor.py` | Support repos are machine-declared as extension-only, excluded from the default governed repo set and Foundry Agent truth set, and guarded against no-resurrection drift. |
| Support repo active truth owner | done | `opl-doc-doctor doctor . --format json`; this document | The support repo now has a detected Active Truth owner for current progress, gaps and next-round prompt. |
| Repo-temp verification hygiene | done | `scripts/verify.sh`; `scripts/opl_doc_doctor.py`; `pyproject.toml`; `tests/test_opl_doc_doctor.py` | Default verification routes Python bytecode and pytest cache outside the checkout; the doctor CLI disables bytecode writes before importing implementation modules; pytest cache provider is disabled for direct test runs. |

## Current-State vs Ideal-State Gaps

### Functional / Structural Gaps

| Gap | Ideal state | Current state | Required change | Owner surface | Evidence |
| --- | --- | --- | --- | --- | --- |
| support-repo-profile-contract | Support repo participates in OPL native profile drift checks without becoming a Foundry Agent truth owner. | `contracts/opl-native-profile.json` is committed for this support repo and declares `opl-doc` as a `codex_plugin` profile with extension-only authority; `contracts/support-repo-policy.json` materializes the extension-only support repo policy and no-resurrection guard used by `family-plan`. | Keep `native-check .` in default verification so profile drift fails closed; keep `family-plan` deriving support policy from `build_support_repo_policy()`; do not treat either contract as repo truth or Foundry Agent truth. | `contracts/opl-native-profile.json`; `contracts/support-repo-policy.json`; `scripts/opl_doc_doctor_parts/constants.py`; `scripts/opl_doc_doctor_parts/family_plan.py`; `scripts/opl_doc_doctor_parts/plugin_sync.py`; `scripts/verify.sh`; `docs/status.md` | `python3 scripts/opl_doc_doctor.py family-plan --format json`; `python3 scripts/opl_doc_doctor.py native-check .`; `bash scripts/verify.sh`. |
| active-support-coverage-ledger | OPL series tranches keep repo-by-repo coverage / next-scope evidence, including explicit support repos touched by the task. | Core skill requires coverage ledger, but `opl-doc` support repo previously had no active owner to carry current support-repo coverage state. | Keep this document updated when support repo governance changes; mirror cross-repo tranche coverage into the relevant governed repo ledger. | `docs/active/opl-doc-active-truth-plan.md`; OPL family ledger in `one-person-lab` | Current objective explicitly includes support repos touched this round. |
| repo-temp-verification-hygiene | Default verification should not create `.pytest_cache`, `__pycache__`, `*.pyc`, virtualenvs or install artifacts inside the development checkout. | `scripts/verify.sh` exports repo-temp Python/pytest cache environment; `scripts/opl_doc_doctor.py` disables bytecode writes before importing implementation modules; `pyproject.toml` disables pytest cache provider for direct pytest runs. | Keep cache/bytecode safeguards in `scripts/verify.sh` and the doctor CLI entrypoint, and guard them with tests. | `scripts/verify.sh`; `scripts/opl_doc_doctor.py`; `pyproject.toml`; `tests/test_opl_doc_doctor.py` | `bash scripts/verify.sh`; `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q`; `git status --short`; cache-dir scan. |

### Test / Evidence Gaps

| Gap | Existing implementation state | Missing evidence | Required verification | Foldback target |
| --- | --- | --- | --- | --- |
| full-install-live-verify | Installer and verify-only tests exist; default verification runs unit tests. | Live user-level install was not changed in this tranche. | For install-surface changes, run `python3 scripts/install_local_plugin.py --verify-only` after install/sync scope is explicitly assigned. | `docs/status.md`; this active plan |
| profile-contract-materialization | `native-sync` supports default and explicit dry-run plus apply, and this repo now commits the generated support profile contract. | Materialization evidence is structural only; no live install or external repo sync changed in this tranche. | For future profile changes, run `python3 scripts/opl_doc_doctor.py native-sync . --dry-run`, `python3 scripts/opl_doc_doctor.py native-sync . --apply`, `python3 scripts/opl_doc_doctor.py native-check .`, and `bash scripts/verify.sh`. | `contracts/opl-native-profile.json`; `docs/decisions.md`; this active plan |

## Next-Round Agent Prompt

Objective:

- Use OPL Doc to continue support-repo governance for `opl-doc` while preserving its extension-only boundary: maintain the committed `contracts/opl-native-profile.json` with `native-check`, update docs only from live source/tests/CLI evidence, and keep the retired previous skill-name surfaces history-only without restoring compatibility hooks.

Write scope:

- `contracts/opl-native-profile.json` or `contracts/support-repo-policy.json` when profile discovery, support repo policy, or canonical docs drift changes.
- `docs/active/opl-doc-active-truth-plan.md`, `docs/status.md`, `docs/decisions.md`, and relevant history tombstones only when live evidence changes.
- Tests under `tests/` only when source behavior changes.

Non-goals:

- Do not make `opl-doc` part of the default Foundry Agent truth owner set.
- Do not restore the retired previous skill-name skill, marketplace entry, installer cleanup hook, alias, facade, wrapper, or active README quick-start wording.
- Do not write target repo truth, runtime truth, artifact authority, quality verdict, owner receipt, or production readiness into doctor/native-profile/family-plan output.

Live truth inputs:

- `AGENTS.md`
- `README.md`, `README.zh-CN.md`, `docs/README.md`, `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md`
- `.codex-plugin/plugin.json`
- `skills/opl-doc/SKILL.md`
- `scripts/opl_doc_doctor.py`, `scripts/opl_doc_doctor_parts/`, `scripts/install_local_plugin.py`
- `tests/test_opl_doc_doctor.py`, `tests/test_install_local_plugin.py`

Required actions:

- Re-run doctor before editing and treat findings as risk map only.
- Compare any current-state claim against live source/tests/CLI output.
- Keep this plan as the support repo's active owner; route process material to `docs/history/`.

Verification commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor . --format json
python3 scripts/opl_doc_doctor.py family-plan --format markdown
python3 scripts/opl_doc_doctor.py native-sync . --dry-run
python3 scripts/opl_doc_doctor.py native-check .
bash scripts/verify.sh
git diff --check
find . -path './.git' -prune -o \( -name '.pytest_cache' -o -name '__pycache__' -o -name '*.pyc' \) -print
```

Completion / foldback gate:

- Closed gaps are removed or rewritten in this plan.
- Durable current facts are folded to `docs/status.md` or canonical docs.
- Process material is moved to history/tombstone.
- Active paths contain no dated execution diary.
- Next-round prompt names only remaining work.
- Final main checkout verification is complete.

## History / Tombstone Foldback

- Process material to archive: none in this tranche.
- Retired surfaces to tombstone: the retired previous skill-name tombstone and installer cleanup-tail tombstone in `docs/history/`, plus the doctor entrypoint/package-facade retirement records, remain the current no-resurrection records.
- No-resurrection guard: `tests/test_install_local_plugin.py` blocks the retired previous skill-name literal from resurfacing outside history tombstones and the negative guard itself; the same test file also blocks old-name skill files. `tests/test_opl_doc_doctor.py` blocks the broad doctor entrypoint re-export and package-root API facade. Do not restore the installer cleanup tail.
