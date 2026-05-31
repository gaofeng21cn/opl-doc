# OPL Doc 协作规范

你始终用中文回复。

本仓用于维护 OPL-native 文档生命周期治理技能、脚本和参考模板。它只治理开发相关文档、变更包、归档和软件工程闭环，不承载 OPL series 的 domain truth、runtime truth、artifact authority 或 owner receipt。

## 工作原则

- 修改前先读相关文件、测试和当前仓库约束。
- 保持实现小而可验证，不引入不必要依赖。
- 文档、脚本和测试必须同步更新。
- 新增长期文档需声明 `Owner`、`Purpose`、`State`、`Machine boundary`。
- 外部框架只能作为参考；本仓 canonical 规则以 OPL series 的文档生命周期、active/history/tombstone、contracts/read-model 边界为准。
- 不保留兼容污染面：active caller 迁出后进入 delete/archive/tombstone，而不是新增 alias 或 facade。

## 验证

默认验证命令：

```bash
python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor .
python3 scripts/opl_doc_doctor.py family-plan --format markdown
```

