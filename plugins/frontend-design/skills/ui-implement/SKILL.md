---
name: ui-implement
description: 从 Pencil 精细化设计稿（.pen 文件）中提取设计信息，用于指导前端代码实现。
disable-model-invocation: true
---

# UI 实现：从设计稿提取信息

用户提供 .pen 文件路径后，通过 Pencil MCP 工具提取设计信息，用于编写前端代码。

## 调用基础

```bash
# 1. 发现可用方法
mcporter list pencil

# 2. 调用格式
mcporter call pencil.<方法名> --args '<JSON参数>' --timeout <毫秒>
```

**注意事项**：
- `filePath` 必须用绝对路径
- 大文件操作加 `--timeout 120000`
- 不可并发调用 `batch_get`，会导致 JSON 解析失败
- 管道到 Python 时加 `2>/dev/null` 抑制 stderr
- Python f-string 中不能用 `\"`，需先赋值给临时变量

> 更多踩坑点见 `references/mcporter-notes.md`

## 提取方法论

核心思路：**先全局后局部，先结构后细节**。每一步的输出决定下一步查什么。

### 1. 获取设计系统

用 `get_variables` 获取所有 Design Token。Token 是色彩、间距、圆角等基础变量，直接映射为 CSS 变量或 Tailwind 主题。

变量名格式：`$--accent`（单 `$`），节点中引用为 `$$--accent`（双 `$`）。

### 2. 画布总览

用 `batch_get` 获取所有顶层节点，建立全局认知：

- **页面**：尺寸 1920×1080（PC）或 375×812（Phone）— 需要实现的核心
- **变体**：name 含 `/`（如 `Button/Hover`）— 组件的交互状态
- **说明卡片**：name 含 `Description` — 交互/布局行为描述
- **风格卡片**：通常是第一个节点 — 配色字体规范

这一步的目的是确定：需要实现哪些页面、每个页面有哪些组件变体、有哪些说明需要阅读。

### 3. 阅读说明卡片

从说明卡片中提取代码无法从视觉获取的信息：布局行为（固定/滚动/吸顶吸底）、交互说明（悬浮/点击/展开折叠）、响应式差异（PC/Phone）。

说明卡片是 text 节点，通过 `content` 属性获取文字内容。

### 4. 提取组件结构与样式

对每个需要实现的页面/组件，用 `batch_get` 获取其节点树。**同时关注结构和样式**，因为两者在同一遍遍历中获取最高效。

**结构信息**（决定 HTML 结构）：
- **嵌套关系** — frame 嵌套决定组件层级
- **layout** — `vertical` → flex-col，`horizontal` → flex-row，`none` → relative
- **gap / padding / justifyContent / alignItems** — 间距和对齐
- **尺寸** — `fill_container` 撑满父容器，`fit_content(0)` 自适应内容
- **name** — 语义锚点，直接对应代码中的组件名

**样式信息**（决定 CSS）：
- **fill** — 背景色（可能是变量引用 `$$--xxx` 或直接色值）
- **stroke** — 边框（`{"thickness": 1, "fill": "..."}`）
- **cornerRadius** — 圆角
- **fontFamily / fontSize / fontWeight** — 排版（仅 text 节点）

**叶子节点内容**：
- `text` 节点的 `content` — 实际文字内容
- `icon_font` 节点的 `iconFontName` — Lucide 图标名（kebab-case → PascalCase）

默认 `batch_get` 返回变量引用。如需解析后的实际色值，用 `resolveVariables: true`。

> 属性到代码的映射表见 `references/code-mapping.md`，完整数据结构见 `references/design-structure.md`

### 5. 提取变体差异

组件通常有多种状态（默认、悬浮、激活、禁用等）。变体的 name 格式为 `ComponentName/State`。

对比同一组件的不同变体，提取差异属性（通常是 fill、stroke、opacity），映射为 CSS 伪类或组件 state。

## 控制 batch_get 数据量

避免一次性大范围深读取。策略：先用无参数调用获取顶层概览，再用 `nodeIds` + `readDepth` 按需深入特定节点。

| 参数 | 作用 |
|------|------|
| `nodeIds: ["id1", "id2"]` | 只读取指定节点及其子节点 |
| `readDepth: 2` | 控制向下读取几层（默认1） |
| `parentId: "xxx"` | 限定搜索范围在某个节点内 |
| `patterns: [{"reusable": true}]` | 按属性模式搜索 |

## batch_get 返回数据结构

```json
{
  "results": [
    {
      "node": { "id": "xxx", "name": "...", "type": "frame", ... },
      "children": [
        { "node": {...}, "children": [...] },
        { "node": {...}, "children": [...] }
      ]
    }
  ]
}
```

每个结果包含 `node`（节点自身属性）和 `children`（子节点数组，递归结构）。遍历时从根节点开始，逐层提取结构、样式和内容。
