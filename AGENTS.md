# OPL Doc

本仓维护 OPL family 的文档生命周期支持 Skill、doctor、contracts 和参考模板。

- OPL Doc 只持有文档治理能力与 support-repo policy，不持有 domain truth、runtime truth、artifact authority 或 owner receipts。
- doctor、family-plan 和 native-profile 输出是诊断与同步结果；当前事实以本仓 contracts、源码、测试及目标仓 readback 为准。
- 文档结构与生命周期细节按任务读取 `docs/` 和相关 contracts。

默认验证入口：`bash scripts/verify.sh`。

<!-- CODEGRAPH_START -->
## CodeGraph

- 本仓库使用本地 `.codegraph/` 索引；该目录不得纳入 Git。
- 定义、调用、影响范围和代码路径等结构检索优先使用 CodeGraph；字面文本检索使用 `rg`。
- 索引缺失或过期时运行 `codegraph init .` 或 `codegraph sync .`。
<!-- CODEGRAPH_END -->
