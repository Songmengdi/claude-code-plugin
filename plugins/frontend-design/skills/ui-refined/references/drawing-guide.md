# 绘制规则

## 图标绘制

**必须使用 `icon_font` 类型 + Lucide 字体**。Pencil 不渲染 Unicode 字符（▾ ▴ 等），所有图标必须用 icon_font。

### 独立图标

直接放在 flex 容器中，无需 wrapper frame：

```
I(parentId, {"type": "icon_font", "width": 14, "height": 14, "iconFontName": "chevron-down", "iconFontFamily": "lucide", "fill": "$--muted"})
```

### 文本 + 图标组合

必须包裹在子 frame 中：

```
btn = I(parentId, {"type": "frame", "name": "Expand Btn", "gap": 4, "alignItems": "center"})
I(btn, {"type": "text", "fill": "$--muted", "content": "展开", "fontFamily": "Inter", "fontSize": 11})
I(btn, {"type": "icon_font", "iconFontFamily": "lucide", "iconFontName": "chevron-down", "width": 14, "height": 14, "fill": "$--muted"})
```

### icon_font 属性

| 属性 | 说明 |
|------|------|
| `iconFontFamily` | 固定为 `"lucide"` |
| `iconFontName` | Lucide 图标名（见下方列表） |
| `fill` | 控制图标颜色 |
| 外层 frame | **仅在文本+图标组合时需要**，独立图标可直接放在父容器中 |

### 常用 Lucide 图标名

`plus`、`minus`、`x`、`check`、`chevron-right`、`chevron-down`、`chevron-up`、`circle`、`search`、`settings`、`home`、`user`、`bell`、`menu`、`arrow-right`、`info`、`alert-triangle`、`trash-2`、`send`、`stop-circle`、`image`、`paperclip`

### 何时用 path 手绘

仅当 Lucide 没有所需图标时，用 SVG path 手绘（复杂度高，尽量避开）。

## 文本换行

Pencil 不支持 `flexWrap`。需要手动将长文本拆分为多个 text 节点。

## Flex 布局组合规则

Pencil 的 flex 布局（`justifyContent`、`alignItems`）作用于**直接子节点**。违反以下规则会导致元素错位或分布异常。

### 规则 1：文本 + 图标必须包裹在子 frame 中

`text` 和 `icon_font` 作为独立子节点放在 flex 容器中时，无法像 HTML 那样自然排列。必须将它们包裹在一个子 frame 中：

```
# ❌ 错误：text 和 icon_font 作为独立子节点
frame(space_between)
  Tag text          ← 被推到最左
  Path text         ← 被推到中间
  "展开" text       ← 被推到中间偏右
  chevron-down icon ← 被推到最右

# ✅ 正确：相关元素分组到子 frame 中
frame(space_between)
  Left frame(gap: 8, alignItems: center)
    Tag text
    Path text
  Expand Btn frame(gap: 4, alignItems: center)
    "展开" text
    chevron-down icon_font
```

### 规则 2：space_between 只适合两个子组

`space_between` 将子节点沿主轴两端对齐。当直接子节点超过 2 个时，元素会被均匀分布到不期望的位置。

**正确做法**：始终将内容归纳为两个逻辑组（如"左侧信息"和"右侧操作"），每个组用一个子 frame 包裹，让 `space_between` 只作用在这两个组之间。

### 规则 3：icon_font 可直接放在 flex 容器中

不需要用 `layout: none` 的 wrapper frame 包裹 icon_font。直接将 icon_font 作为 flex 容器的子节点即可，Pencil 会正确计算其尺寸和位置。

### 规则 4：不要为内容可变的节点设置显式 height

显式 height 会导致内容溢出被裁剪。创建时省略 height 属性，让 Pencil 根据子节点自动计算。**注意**：U() 无法将已有 height 改为 `fit_content`，如果必须移除 height，需删除节点重建。

## PC 端组件参考尺寸

| 组件 | 推荐尺寸 | 备注 |
|------|----------|------|
| 顶部导航栏 | fill_container × 56-64 | 水平布局，内含 logo + 导航链接 + 操作区 |
| 侧边栏 | 240-320 × fill_container | 固定宽度 |
| 卡片间距 | gap: 16-24 | |
| 内边距 | padding: 16-24 | |

## 移动端组件参考尺寸

| 组件 | 推荐尺寸 | 备注 |
|------|----------|------|
| 顶部导航 | fill_container × 44-56 | 含汉堡菜单图标 |
| 底部栏 | fill_container × 56-80 | 固定底部 |
| 卡片内边距 | padding: 16 | 左右留白 |
| 触控区域 | ≥ 44px | 按钮和可点击元素 |
