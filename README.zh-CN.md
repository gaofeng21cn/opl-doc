# OPL Doc

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

<p align="center"><strong>面向 AI 长时间工程开发的 OPL-native 文档管家</strong></p>
<p align="center">当 Codex 或其他代理需要理解目标并持续开发时，让仓库文档保持当前、分层清楚、可验证。</p>

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>服务对象</strong><br/>
      维护 OPL family 或 OPL-compatible 仓库的开发者与 AI operator
    </td>
    <td width="33%" valign="top">
      <strong>组织什么</strong><br/>
      理想态参考、Active Truth plan、history/tombstone 和验证证据
    </td>
    <td width="33%" valign="top">
      <strong>如何开始</strong><br/>
      直接让 Codex 使用 OPL Doc 治理当前 repo 或 OPL series
    </td>
  </tr>
</table>

## 为什么是 OPL Doc

AI 代理能否持续开发，取决于仓库是否清楚告诉它“现在什么是真的”。长时间工程推进后，旧计划会留在 active 文档里，历史清单越堆越长，已经退役的接口看起来仍然有效，下一位代理就要花大量上下文重新判断真实状态。OPL Doc 的目标是防止这种文档漂移，让每一轮 AI 工程接力都能从当前事实、清楚入口和可验证下一步开始。

OPL Doc 把这类清理工作变成可重复的文档管家流程。它帮助 Codex 读取当前仓库事实，逐段审计 README 和 docs 中的实质 claim，区分 active plan 和历史材料，让每个文档只保留一个任务，直接退役过时 surface，把过程内容折叠进 archive 或 tombstone，并用新鲜验证证据收口。

`opl-doc` 是 canonical plugin 和 skill 名。

它也帮助 OPL 系列仓库保持同一套当前叙事：用户入口讲清产品价值，开发者入口讲清边界和验证，过时的技术说法及时折回历史或 tombstone。OPL Doc 只治理这些文档 claim 是否与各仓当前事实一致，不成为第二真相源。

目标很直接：用户只需要一句话说“治理文档”，代理就应该知道如何开始、什么时候创建 `/goal`、如何避免旧文档二次污染，以及如何完成工程闭环。

## 它提供什么

- **稳定的文档管家入口**：让 Codex 知道先读什么、怎么判断旧内容、如何收尾，不需要用户反复写长 prompt。
- **从当前事实出发**：先读取目标仓现有规则、README、docs、代码、合同和验证入口，再决定哪些文案需要更新。
- **让 README 回到用户问题**：检查入口页是否讲清产品价值、使用场景和开始方式，把底层技术细节放回开发者区。
- **清理旧计划和旧入口**：把已完成计划、退役路线和过程材料折回 history 或 tombstone，避免继续污染 active 文档。
- **全量文档组合清理**：逐个审计 `README*` 和 `docs/**/*.md`，让每份长期文档只承担一个清晰任务。
- **OPL series 长线治理**：为 `one-person-lab`、`med-autoscience`、`med-autogrant`、`redcube-ai`、`opl-meta-agent`、`opl-bookforge`、`one-person-lab-app` 以及后续兼容仓库生成治理计划。
- **短期变更包模板**：为需要意图、设计、任务、验证和折回的变更提供临时工作包。

## 一句话开始

如果是在新机器上配置完整 Codex + OPL 全家桶，包括 OPL runtime、MAS/MAG/RCA/OMA 智能体可见面、BookForge 系列治理覆盖、OPL Flow、OPL Doc、One Person Lab App 和 companion tools，先从 [One Person Lab 新机器 Codex 全家桶安装入口](https://github.com/gaofeng21cn/one-person-lab/blob/main/docs/references/current-support/opl-new-machine-codex-bootstrap.md) 开始。

安装为本地 Codex plugin：

```bash
git clone git@github.com:gaofeng21cn/opl-doc.git
cd opl-doc
python3 scripts/install_local_plugin.py
python3 scripts/install_local_plugin.py --verify-only
```

这会把 plugin 复制到 `~/plugins/opl-doc`，注册到个人 marketplace，在 `~/.local/bin` 下创建用户级 `opl-doc-doctor` 命令，并安装 `opl-doc` skill 入口。它不会向被治理的 repo 写入任何文件。

重启 Codex 后，一句话使用：

- “使用 OPL Doc 治理这个 repo 的开发文档生命周期。”
- “使用 OPL Doc 治理 OPL series 的开发文档生命周期。”
- “使用 OPL Doc 清理 stale active docs，并把已完成计划折回 history。”

对于 OPL series、多仓清理、长周期自治、或提到 worktree/subagent/吸收回 `main` 的任务，skill 会主动进入或延续 `/goal`。默认 OPL series 是 7 个 repo、14 个主参考文档；短单仓只读审计先跑 doctor，不强制 goal。

## 它如何工作

- 代理先读取仓库协作规则和当前文档，再开始编辑；现有文案只是待验证的说法，必须用代码、合同、测试、命令输出和运行证据校准。
- doctor 先给出风险地图，但它不是治理输入，也不是任务清单。
- skill 把 ideal-state reference 当作用户维护的目标输入，从当前仓库事实派生完成进度、当前差距和下一轮 Agent prompt；canonical docs 要折回当前事实，而不是单独当作证明。
- 代理必须把实质文档说法与当前仓库事实逐段对照，再更新文档内容、合并重复职责、路由 stale material。
- 代理必须审计整个文档组合，而不只改 gap 文档；每份长期文档都应保留一个 owner、一个 purpose、一个 state 和一个 machine boundary。
- 如果目标 repo 缺少稳定 active owner，代理可以用 `templates/active-truth-plan.md` 作为 single Active Truth plan 的形状。
- skill 按内容角色路由章节，并在 closeout 前检查 closed gap、完成过程包和 stale wording 没有继续留在 active path。
- skill 将文档分类为当前事实、active plan、支撑参考、历史、tombstone 或 stale pollution。
- active docs 只保留当前工作；过程材料进入 history 或 tombstone references。
- 已过时的模块、接口、测试、文档、workflow 和入口在 replacement 与 no-active-caller 证据成立后直接退役；治理输出不得新增 compatibility alias、facade、wrapper 或“旧入口仍可用”叙述。
- OPL series 治理按 long-horizon tranche 续跑；单轮 verified / absorbed 只是 tranche closeout，coverage ledger 仍有未覆盖文档、剩余 stale/retire 候选或未完成 gap 时，不得关闭全局 `/goal`。
- 已完成工作折回 canonical docs，并用 repo-native 验证收口。

OPL Doc 是 OPL-native 的治理工具。OpenArc、OpenSpec、Spec Kit、Agent OS 等项目是有用参考，但本仓不会把 OPL 系列项目迁移到外部固定文件布局。

默认 OPL series workflow 覆盖 OPL、MAS、MAG、RCA、OMA、BookForge 和 App 七个治理 repo。`opl-doc`、`opl-aion-shell` 等 support repo 只是 workflow 或 shell-carrier 任务的 explicit extension，不是默认 Foundry Agent truth owner。

## CLI

只读审计：

```bash
opl-doc-doctor doctor /path/to/repo
opl-doc-doctor doctor /path/to/repo --format json
```

生成 OPL series 工作流：

```bash
opl-doc-doctor family-plan --format markdown
opl-doc-doctor family-plan --format json
```

`family-plan` 只生成 workflow map，不生成第二事实表。support repo 会出现在 `support_repo_policy` 中作为 extension-only 输入；当前事实仍回各 repo 自己的 canonical docs、contracts、tests 和运行证据。

需要本机 workspace 路径时：

```bash
opl-doc-doctor family-plan --workspace-root /path/to/workspace --format json
```

覆盖或新增 repo：

```bash
opl-doc-doctor family-plan --repo award=award-agent --format markdown
```

## 生命周期模型

每份长期开发文档都应只有一个任务。若一个文档混合当前事实、active plan、支撑参考、执行记录和历史，治理流程需要为每类内容选定 canonical owner，移动有用内容，并归档、tombstone 或删除重复材料。

| 生命周期角色 | 放置位置 |
| --- | --- |
| 当前事实 | `README*`、`docs/README*`、`docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md` |
| 当前执行与差距 | `docs/active/` |
| 产品、运行时、source、delivery 支撑 | `docs/product/`、`docs/runtime/`、`docs/source/`、`docs/delivery/` |
| 稳定政策、规格和参考 | `docs/policies/`、`docs/specs/`、`docs/references/` |
| 历史过程、退役计划、tombstone | `docs/history/` |
| 机器真相 | 源码、测试、contracts、CLI/API 输出和运行证据 |

doctor 始终只读。它可以识别风险，但不会管理文档语义、不会提供治理任务清单、不会声明仓库 production-ready，也不会替代代码、测试、contracts、read model 或运行证据。native profile 只做 profile sync / drift check；family-plan 只做 workflow plan；它们都不能成为第二真相源。

## Change Packet

非平凡工作可以在 `docs/active/changes/<change-id>/` 下使用短期工作包：

```text
intent.md
design.md
tasks.md
verification.md
foldback.md
```

变更完成后，把当前事实折回 canonical docs，把过程材料移入 history 或 tombstone references。

## 技术说明

<details>
  <summary><strong>展开开发者与代理细节</strong></summary>

### 仓库结构

- `.codex-plugin/plugin.json`：本地 Codex plugin manifest。
- `skills/opl-doc/SKILL.md`：canonical Codex skill 入口。
- `skills/opl-doc/agents/openai.yaml`：UI 元数据和默认 prompt。
- `scripts/opl_doc_doctor.py`：`doctor`、`family-plan`、`native-check` 和 `native-sync` 的仓内命令 bootstrap。
- `scripts/opl_doc_doctor_parts/`：按 profile discovery、invariant checks、plugin-native profile sync、family-plan 生成、CLI parsing 和 report rendering 拆分的 doctor 实现与 import API。
- `scripts/install_local_plugin.py`：本地 plugin 安装脚本。
- `docs/history/opl-doc-governance-tombstone.md`：已退役 `opl-doc-governance` 入口的 provenance。
- `templates/`：Active Truth plan、goal 和 change-packet 模板。
- `tests/`：doctor、goal mode 和安装流程测试。

### 验证

```bash
bash scripts/verify.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor .
python3 scripts/opl_doc_doctor.py family-plan --format markdown
```

### 边界

- 本仓治理开发文档生命周期和软件工程闭环。
- 本仓不持有 OPL series 的项目真相、runtime truth、domain verdict、artifact authority、quality verdict、owner receipt、production readiness 或默认 Foundry Agent truth set。
- 本仓保留 OPL-native taxonomy，不把项目迁移到 OpenArc、OpenSpec、Spec Kit 或 Agent OS 的固定布局。
- public 默认值只使用 repo 名称，不写本机绝对路径；本机使用 `--workspace-root` 或 `--repo ID=PATH`。
- OPL series 根层 README 面向用户，默认从问题、价值和使用场景讲起；`executor-first`、stage、route、receipt、typed blocker、Tool Affordance Boundary 等技术边界只在折叠的 Agent / 开发者 / operator 区或 canonical 技术文档中展开。

### 文档

- [文档索引](./docs/README.md)
- [项目概览](./docs/project.md)
- [当前状态](./docs/status.md)
- [架构](./docs/architecture.md)
- [硬约束](./docs/invariants.md)
- [关键决策](./docs/decisions.md)
- [使用说明](./docs/usage.md)

</details>
