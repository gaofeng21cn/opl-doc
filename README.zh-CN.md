# OPL Doc Governance

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

<p align="center"><strong>面向 AI 长时间软件开发的文档生命周期治理工具</strong></p>
<p align="center">一个 Codex skill 和只读 CLI doctor，用来让开发文档保持当前、分层清楚，并服务自主工程闭环。</p>

## 为什么需要它

长时间 AI 开发最容易被过时文档拖垮：旧计划留在 active 路径，历史清单不断堆叠，已经退役的接口看起来还活着，代理每次都要重新判断互相矛盾的文档。

OPL Doc Governance 把文档清理变成可重复执行的工作流。它帮助代理读取仓库当前事实，按生命周期角色逐份分类文档，清理过时内容，把历史折叠进 archive 或 tombstone，并通过验证完成工程闭环。

它是 OPL-native 的治理工具。OpenArc、OpenSpec、Spec Kit、Agent OS 等项目是有用参考，但本仓不会把 OPL 系列项目迁移到外部固定文件布局。

## 它提供什么

- **Codex skill**：可复用的开发文档生命周期治理流程。
- **自动 goal 模式**：遇到 OPL series、多仓、长周期或会修改文档的治理请求时，skill 要求代理先创建或延续 `/goal`。
- **只读 doctor**：CLI 扫描 canonical docs、生命周期头、active 旧词和历史增量长清单风险。
- **OPL series 工作流**：为 `one-person-lab`、`med-autoscience`、`med-autogrant`、`redcube-ai`、`opl-meta-agent` 以及后续 OPL-compatible repo 生成治理计划。
- **Change packet 模板**：为非平凡文档或工程变更提供短期 active 工作包。

## 快速开始

安装为本地 Codex plugin：

```bash
python3 scripts/install_local_plugin.py
```

重启 Codex 后，一句话使用：

```text
使用 OPL Doc Governance 治理这个 repo 的开发文档生命周期。
```

治理完整 OPL series：

```text
使用 OPL Doc Governance 治理 OPL series 的开发文档生命周期。
```

对于 OPL series、多仓清理、长周期自治、或提到 worktree/subagent/吸收回 `main` 的任务，skill 会主动进入或延续 `/goal`。短单仓只读审计先跑 doctor，不强制 goal。

## CLI

只读审计：

```bash
python3 scripts/opl_doc_doctor.py doctor /path/to/repo
python3 scripts/opl_doc_doctor.py doctor /path/to/repo --format json
```

生成 OPL series 工作流：

```bash
python3 scripts/opl_doc_doctor.py family-plan --format markdown
python3 scripts/opl_doc_doctor.py family-plan --format json
```

需要本机 workspace 路径时：

```bash
python3 scripts/opl_doc_doctor.py family-plan --workspace-root /path/to/workspace --format json
```

覆盖或新增 repo：

```bash
python3 scripts/opl_doc_doctor.py family-plan --repo award=award-agent --format markdown
```

## 生命周期模型

每份长期开发文档都应只有一个任务：

| 生命周期角色 | 放置位置 |
| --- | --- |
| 当前事实 | `README*`、`docs/README*`、`docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md` |
| 当前执行与差距 | `docs/active/` |
| 产品、运行时、source、delivery 支撑 | `docs/product/`、`docs/runtime/`、`docs/source/`、`docs/delivery/` |
| 稳定政策、规格和参考 | `docs/policies/`、`docs/specs/`、`docs/references/` |
| 历史过程、退役计划、tombstone | `docs/history/` |
| 机器真相 | 源码、测试、contracts、CLI/API 输出、runtime ledger、receipt refs |

doctor 始终只读。它可以识别风险，但不会声明仓库 production-ready，也不会替代代码、测试、contracts、read model 或 owner receipt。

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
- `skills/opl-doc-governance/SKILL.md`：Codex 使用的 skill 入口。
- `skills/opl-doc-governance/agents/openai.yaml`：UI 元数据和默认 prompt。
- `scripts/opl_doc_doctor.py`：只读 doctor 和 family-plan 生成器。
- `scripts/install_local_plugin.py`：本地 plugin 安装脚本。
- `templates/`：goal 和 change-packet 模板。
- `tests/`：doctor、goal mode 和安装流程测试。

### 验证

```bash
python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor .
python3 scripts/opl_doc_doctor.py family-plan --format markdown
bash scripts/verify.sh
```

### 边界

- 本仓治理开发文档生命周期和软件工程闭环。
- 本仓不持有 OPL series 的项目真相、runtime truth、domain verdict、artifact authority 或 owner receipt。
- 本仓保留 OPL-native taxonomy，不把项目迁移到 OpenArc、OpenSpec、Spec Kit 或 Agent OS 的固定布局。
- public 默认值只使用 repo 名称，不写本机绝对路径；本机使用 `--workspace-root` 或 `--repo ID=PATH`。

### 文档

- [文档索引](./docs/README.md)
- [项目概览](./docs/project.md)
- [当前状态](./docs/status.md)
- [架构](./docs/architecture.md)
- [硬约束](./docs/invariants.md)
- [关键决策](./docs/decisions.md)
- [使用说明](./docs/usage.md)

</details>
