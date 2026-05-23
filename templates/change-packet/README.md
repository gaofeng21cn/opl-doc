# Change Packet

Owner: `One Person Lab`
Purpose: `change_packet_template`
State: `active_template`
Machine boundary: 本目录是人读变更包模板；不能替代 issue、commit、contract、test 或 runtime receipt。

## 适用场景

用于非平凡文档治理、结构调整、跨 repo closeout 或需要多轮验证的开发工作。轻量变更可以只在对话中写同等结构；长期 lane 可复制本目录到目标 repo 的 `docs/active/changes/<change-id>/`。

## 文件

- `intent.md`：为什么做、做什么、不做什么、owner 边界。
- `design.md`：设计判断、taxonomy 影响、machine-boundary 影响。
- `tasks.md`：执行 lane、文件范围、完成门。
- `verification.md`：验证命令、证据、失败解释。
- `foldback.md`：完成后哪些内容折返到 canonical docs、history 或 tombstone。

## 折返规则

完成后不要让 change packet 继续充当当前事实源。仍有效的事实进入 canonical docs；后续计划进入 active baton；过程记录进入 `docs/history/**`；退役语义进入 tombstone/provenance。

