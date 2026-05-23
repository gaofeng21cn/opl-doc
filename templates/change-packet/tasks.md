# Change Tasks: <change-id>

Owner: `<owner>`
Purpose: `change_tasks`
State: `active_plan`
Machine boundary: 本文是短期任务分解；完成状态以提交、验证和 foldback 为准。

## Lanes

- [ ] Read target repo instructions and canonical docs.
- [ ] Capture current code/contracts/tests/read-model evidence relevant to the change.
- [ ] Update scoped docs/skills/templates.
- [ ] Remove or archive stale active wording without adding compatibility aliases.
- [ ] Update indexes so each long-lived document has one job.

## Parallelism

- Worktree/subagent lanes:
- Disjoint write scopes:

## Verification

- [ ] Run repo-native verification.
- [ ] Run `git diff --check`.
- [ ] Scan for conflict markers.
- [ ] Scan for stale wording or old-route resurrection terms relevant to this change.

## Absorb / Cleanup

- [ ] Absorb completed lane to `main`.
- [ ] Delete temporary worktree/branch created for this lane.
- [ ] Record remaining functional/structural gaps and test/evidence gaps separately.
