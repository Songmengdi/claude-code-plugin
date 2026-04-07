# .pen 文件数据结构

## 顶层结构

```json
{
  "version": "2.10",
  "children": [ ... ],   // 所有顶层节点
  "variables": { ... }   // Design Token
}
```

## 节点类型

### frame（容器/组件）

承载布局和视觉属性，可包含子节点。

```json
{
  "type": "frame",
  "id": "kidiO",
  "name": "Sidebar",
  "x": 0, "y": 1280,
  "width": 280,
  "height": "fill_container",
  "fill": "$$--card",
  "cornerRadius": "$$--radius-s",
  "stroke": { "thickness": 1, "fill": "$$--border" },
  "layout": "vertical",
  "gap": 12,
  "padding": [16, 12],
  "justifyContent": "space_between",
  "alignItems": "center",
  "children": [ ... ]
}
```

| 属性 | 类型 | 可选值 |
|------|------|--------|
| `width/height` | number / string | `"fill_container"` / `"fit_content(0)"` |
| `fill` | string | 色值或 `"$$--变量名"` |
| `cornerRadius` | number / string | 数字或 `"$$--变量名"` |
| `stroke` | object | `{"thickness": number, "fill": string}` |
| `layout` | string | `"vertical"` / `"horizontal"` / `"none"` |
| `gap` | number | 子元素间距 |
| `padding` | number / array | 单数字、`[上下, 左右]`、`[上, 右, 下, 左]` |
| `justifyContent` | string | `"start"` / `"end"` / `"center"` / `"space_between"` |
| `alignItems` | string | `"start"` / `"end"` / `"center"` |

### text（文本）

```json
{
  "type": "text",
  "id": "RWTPV",
  "name": "title",
  "fill": "$$--foreground",
  "content": "AI Assistant",
  "fontFamily": "Inter",
  "fontSize": 15,
  "fontWeight": "700"
}
```

仅支持 `fill`、`content`、`fontFamily`、`fontSize`、`fontWeight`、`textGrowth`、`width`。不支持 `layout`、`padding`、`gap`、`cornerRadius`。

### rectangle（矩形/分隔线）

```json
{
  "type": "rectangle",
  "id": "W0XXB",
  "name": "Separator",
  "fill": "$$--border",
  "width": "fill_container",
  "height": 1
}
```

不可包含子节点。分隔线典型模式：`height: 1` + `width: "fill_container"`。

### icon_font（图标）

```json
{
  "type": "icon_font",
  "id": "4OCFR",
  "name": "newIcon",
  "width": 14,
  "height": 14,
  "iconFontName": "plus",
  "iconFontFamily": "lucide",
  "fill": "#ffffff"
}
```

- 图标来自 [Lucide](https://lucide.dev/) 图标集
- `iconFontName` 对应 Lucide 中的图标名（kebab-case → PascalCase，如 `chevron-down` → `ChevronDown`）
- 常见图标：`plus`、`search`、`bot`、`chevron-down`、`chevron-up`、`settings`、`log-out`、`trash-2`、`check`、`send`

## Design Token（variables）

```json
"variables": {
  "$--accent":     { "type": "color",  "value": "#2383e2" },
  "$--background": { "type": "color",  "value": "#fefefe" },
  "$--card":       { "type": "color",  "value": "#ffffff" },
  "$--foreground": { "type": "color",  "value": "#37352f" },
  "$--muted":      { "type": "color",  "value": "#9b9a97" },
  "$--border":     { "type": "color",  "value": "#f0ece5" },
  "$--radius-s":   { "type": "number", "value": 8 },
  "$--radius-m":   { "type": "number", "value": 16 }
}
```

- 类型：`color`（色值）、`number`（数值）
- 节点中用 `"$$--accent"`（双 `$`）引用

## 节点命名约定

| 模式 | 含义 | 示例 |
|------|------|------|
| `ComponentName` | 组件实例 | `Sidebar`、`Chat Area`、`Input Bar` |
| `ComponentName/State` | 状态变体 | `Button/Hover`、`Conv Item/Active`、`Input Sending` |
| `Group/Category` | 分组容器 | `Group/Today`、`Group/Yesterday` |
| `descXxx` | 说明卡片内容 | `descTitle`、`descL1` |
| `s_xxx` | 风格卡片元素 | `s_title`、`s_bg`、`s_ac` |

## 典型组件嵌套模式

### 页面布局
```
frame[1920×1080, vertical]
  ├── frame[Sidebar, 280px, vertical, fill_container]
  └── frame[Main Area, fill_container, vertical]
```

### 列表分组
```
frame[Conversation List, vertical, gap:8]
  └── frame[Group/Today, vertical, gap:4]
        ├── text[label, "今天", muted]
        └── frame[items, vertical, gap:2]
              └── frame[Conv Item, cornerRadius, padding]
```

### 折叠/展开组件
```
折叠态: frame[height:36, space_between, center]
  ├── frame[Left] → text(工具名) + text(路径)
  └── frame[Right] → text("展开") + icon(chevron-down)

展开态: frame[vertical, gap:6]
  ├── frame[Header, space_between]
  ├── frame[Code Preview, fill:#1e1e2e]
  └── text("展开全部")
```
