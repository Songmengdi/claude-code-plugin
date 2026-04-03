---
name: ui-refined
description: |
  基于 Excalidraw 草图，使用 Pencil MCP 工具进行 UI 精细化设计。
  当用户需要将草图/线框图转化为精细化 UI、需要在 Pencil 中实现页面设计、
  需要选择设计风格并实现响应式布局时触发。
  包括：读取草图、风格选择、PC/移动端实现、说明卡片、质量验证。
  关键词：精细化、UI实现、Pencil、设计稿、样式、风格、refined、design、实现布局。
  即使用户只说"把草图变成设计稿"、"实现这个页面"、"精细化UI"，也应触发此 skill。
---

# UI 精细化设计

从 Excalidraw 草图出发，通过 Pencil MCP 工具产出精细化 UI 设计稿。

## 核心原则

1. **草图驱动** — 所有设计决策基于 Excalidraw 草图，不凭空猜测
2. **渐进披露** — 每个阶段只读取该阶段的指令，不要提前翻阅后续阶段
3. **一次一页** — 每个页面在一个 batch_design 调用中完成
4. **验证闭环** — 每页完成后导出验证，有问题立即修正

## 阶段化工作流程

本技能分为 4 个阶段，每个阶段的详细指令存储在独立文件中。

**当前你只处于一个阶段。禁止猜测其他阶段该做什么。**

| # | 名称 | 详情 |
|---|------|------|
| 0 | 准备 | `phases/phase-0.md` |
| 1 | 规划 | `phases/phase-1.md` |
| 2 | 实现 | `phases/phase-2.md` |
| 3 | 验证 | `phases/phase-3.md` |

### 执行规则（强制）

1. **每个阶段的第一步必须是 `Read` 对应的 `phases/phase-N.md`**，未读取前禁止执行任何阶段操作
2. 阶段完成后**停止并等待用户回应后再进入下一阶段**
3. 验证阶段发现问题需修正时，回到实现阶段重新执行

## .pen 文件管理

| 操作 | 方式 |
|------|------|
| 创建 | `echo '{"version": "2.10", "children": []}' > <path>.pen` |
| 打开 | `mcporter call pencil.open_document --args '{"filePathOrTemplate": "绝对路径"}'` |
| 存储位置 | 项目 `<root>/ui-design/xxx.pen` |
