# Pencil 工具与操作语法

## 核心工具速查

| 工具 | 用途 |
|------|------|
| `batch_design` | 批量操作节点（I/C/U/R/M/D/G） |
| `batch_get` | 获取节点详细信息（仅小文件使用） |
| `set_variables` | 定义设计变量（Design Token），组件通过 `$$--` 前缀引用 |
| `get_variables` | 查看已定义的设计变量 |
| `get_editor_state` | 获取当前编辑器状态（轻量，优先使用） |
| `open_document` | 打开 .pen 文件 |
| `find_empty_space_on_canvas` | 查找画布空白区域 |

## 调用格式

```bash
mcporter call pencil.<工具名> --args '<JSON参数>' --timeout 120000
```

**重要**：
- 始终在 `--args` 中显式传入 `filePath`，避免编辑器焦点切换导致 "wrong .pen file" 错误
- 大文件操作必须加 `--timeout 120000`

## 操作语法

操作字符串，用 `\n` 分隔，支持变量绑定（无 var/const）：

```
x = I("parentId", {"type": "frame", "width": 100, "height": 100})
U("id", {"width": 200})
D("id")
M("id", "newParentId", 0)
```

| 操作 | 语法 | 说明 |
|------|------|------|
| 插入 | `I("parentId", {...})` | 父ID为空字符串表示根级 |
| 更新 | `U("id", {...})` | 部分更新属性 |
| 删除 | `D("id")` | |
| 移动 | `M("id", "parentId", index)` | |
| 变量 | `x = I(...)` | 无 var/const 关键字 |

## 属性格式（高频踩坑点，严格遵守）

| 属性 | 正确写法 | 错误写法 |
|------|----------|----------|
| stroke | `{"fill": "#color", "thickness": 1}` | `"#color"` (字符串) |
| fill 透明 | `"#00000000"` (8位 hex) | `"none"` |
| fill 渐变 | `{"type": "gradient", "gradientType": "linear", ...}` | — |
| width/height 撑满 | `"fill_container"` (字符串) | `"100%"` 或数字 |
| width/height 自适应 | `"fit_content"` (字符串) | `"auto"` |
| cornerRadius | 数字 `4` | 字符串 `"4px"` |
| effects/阴影 | `effects: [{type: "shadow", shadowType: "outer", offset: {x:0,y:2}, blur: 8, color: "#0000001a"}]` | `shadow: {...}` (错误属性名) |
| textAlign | 不存在此属性 | — |
| fontFamily | `"Inter"` / `"JetBrains Mono"` | `"-apple-system"` (无效) |
| I() 父ID | `I("", {...})` 根级 | `I("frame", {...})` |
| 变量绑定 | `x = I(...)` | `var x = I(...)` |
| D() ID含数字 | `D("38f4l")` 带引号 | `D(38f4l)` 不带引号 |
| 变量引用 | `"$$--变量名"` (双`$`) | `"$--变量名"` (单`$`, 无效) |
| text 节点属性 | `fill`, `content`, `fontFamily`, `fontSize`, `fontWeight` | `cornerRadius`, `padding`, `layout`, `gap` (仅 frame 有效) |
| 图标 | `icon_font` 类型 + Lucide 字体（见 `references/drawing-guide.md`） | Unicode 字符如 ▾ ▴（Pencil 不渲染） |

> **更新节点属性前，先用 `batch_get` 确认节点类型**。`text`、`rectangle`、`frame` 支持的属性不同，对错误类型属性会报 `unexpected property`。

## 变量引用格式

组件中引用 Design Token 时，必须使用 `$$` 双美元符号前缀：

```bash
# 定义变量（set_variables）
mcporter call pencil.set_variables --args '{
  "filePath": "绝对路径",
  "variables": {
    "$--background": {"type": "color", "value": "#fefefe"},
    "$--card": {"type": "color", "value": "#ffffff"},
    "$--radius-m": {"type": "number", "value": 16}
  }
}'

# 引用变量（batch_design 中）
I("", {"type": "frame", "fill": "$$--background", "cornerRadius": "$$--radius-m"})
```

变量类型：`color`（颜色值）、`number`（数值如圆角、间距）、`string`（字体名等）。

> `batch_get` 的 `resolveVariables: true` 可查看解析后的实际值，`false` 查看原始变量引用。
