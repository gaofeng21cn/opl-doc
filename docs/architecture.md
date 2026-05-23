# 架构

Owner: `One Person Lab`
Purpose: `architecture`
State: `active_truth`
Machine boundary: 本文是人读架构；可执行行为以 `scripts/opl_doc_doctor.py` 和 skill 为准。

## 分层

1. Skill 层
   - 给 Codex 提供文档生命周期工作流、OPL series治理规则和硬边界。
2. Doctor 层
   - 只读扫描 repo docs，输出 profile、canonical docs 状态和 findings。
3. Repo-native anchor 层
   - 在目标 repo 的 `.opl-doc-governance/` 下保存 agent-readable config 和入口，让后续代理从仓库内发现治理规则。
4. Change packet 层
   - 为非平凡开发提供 active change 包，完成后 fold back 到 canonical docs 或 history。
5. Verification 层
   - 通过 repo-native 测试、diff check、doctor 输出和最终 main checkout 验证闭环。

## 边界

doctor 只读，不执行清理、不修改目标仓、不生成 owner receipt。`init-repo` 是显式写入命令，只写 `.opl-doc-governance/` 本地治理入口。skill 可以指导 Codex 修改目标仓文档，但必须先读取目标 repo 约束并运行对应验证。
