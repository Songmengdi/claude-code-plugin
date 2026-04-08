# 设计属性到代码映射

## 布局 → Flexbox

| Pencil | CSS | Tailwind |
|--------|-----|----------|
| `layout: "vertical"` | `flex-direction: column` | `flex flex-col` |
| `layout: "horizontal"` | `flex-direction: row` | `flex flex-row` |
| `layout: "none"` | `position: relative` | `relative` |
| `gap: 8` | `gap: 8px` | `gap-2` |
| `padding: [16, 12]` | `padding: 16px 12px` | `py-4 px-3` |
| `justifyContent: "space_between"` | `justify-content: space-between` | `justify-between` |
| `alignItems: "center"` | `align-items: center` | `items-center` |
| `width: "fill_container"` | `width: 100%` | `w-full` |
| `height: "fill_container"` | `flex: 1` | `flex-1` |

## 视觉 → CSS

| Pencil | CSS |
|--------|-----|
| `fill: "$$--accent"` | `background-color: var(--accent)` |
| `stroke: {"thickness": 1, "fill": "$$--border"}` | `border: 1px solid var(--border)` |
| `cornerRadius: "$$--radius-s"` | `border-radius: var(--radius-s)` |

## 文本 → CSS

| Pencil | CSS |
|--------|-----|
| `fill: "$$--foreground"` | `color: var(--foreground)` |
| `fontFamily: "Inter"` | `font-family: Inter` |
| `fontSize: 13` | `font-size: 13px` |
| `fontWeight: "600"` | `font-weight: 600` |

## 图标 → Lucide 组件

| Pencil | 代码 |
|--------|------|
| `type: "icon_font"` | lucide 图标库 |
| `iconFontName: "chevron-down"` | `<ChevronDown />`（kebab-case → PascalCase） |
| `width/height: 14` | `size={14}` |

## 变量引用

节点中用 `"$$--accent"`（双 `$`）引用 variables 中 `"$--accent"` 的值。
`resolveVariables: true` 可查看解析后的实际值。
