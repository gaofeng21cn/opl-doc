# OPL Doc 协作规范

你始终用中文回复。

本仓用于维护 OPL-native 文档生命周期治理技能、脚本和参考模板。它只治理开发相关文档、变更包、归档和软件工程闭环，不承载 OPL series 的 domain truth、runtime truth、artifact authority 或 owner receipt。

doctor、native profile 和 family-plan 都只是 workflow / lightweight risk map / profile sync，不是 repo truth、runtime truth、domain truth、artifact authority、quality verdict、owner receipt、production readiness 或 Foundry Agent truth set。`opl-doc`、`opl-aion-shell` 等 support repo 只作为 explicit extension 纳入，不进入默认 Foundry Agent truth owner 集合。

## 工作原则

- 修改前先读相关文件、测试和当前仓库约束。
- 保持实现小而可验证，不引入不必要依赖。
- 文档、脚本和测试必须同步更新。
- 新增长期文档需声明 `Owner`、`Purpose`、`State`、`Machine boundary`。
- 外部框架只能作为参考；本仓 canonical 规则以 OPL series 的文档生命周期、active/history/tombstone、contracts/read-model 边界为准。
- 不保留兼容污染面：active caller 迁出后进入 delete/archive/tombstone，而不是新增 alias 或 facade。

## 验证

默认验证命令使用仓内 wrapper，避免把 pytest cache、Python bytecode 或临时输出写入开发 checkout：

```bash
bash scripts/verify.sh
```

若需要单独运行 pytest 或 doctor 命令，优先复用 `scripts/verify.sh` 中的
`OPL_DOC_REPO_TEMP_ROOT`、`PYTHONDONTWRITEBYTECODE`、`PYTHONPYCACHEPREFIX` 和
`PYTEST_ADDOPTS` 环境；不要把 `.pytest_cache`、`__pycache__` 或 `*.pyc` 留在仓库中。
