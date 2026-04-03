# 阶段 2：实现

## 目标

逐页绘制精细化 UI，每页附带说明卡片。

## batch_design 操作语法

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

## 属性格式要点

**高频踩坑点，严格遵守：**

| 属性 | 正确写法 | 错误写法 |
|------|----------|----------|
| stroke | `{"fill": "#color", "thickness": 1}` | `"#color"` (字符串) |
| cornerRadius | 数字 `4` | 字符串 `"4px"` |
| I() 父ID | `I("", {...})` 根级 | `I("frame", {...})` |
| 变量绑定 | `x = I(...)` | `var x = I(...)` |
| D() ID含数字 | `D("38f4l")` 带引号 | `D(38f4l)` 不带引号 |

## 绘制规则

### 一次绘制一个页面

**使用变量绑定在一个 batch_design 调用中完成整个页面。** 不要分多次调用同一页面的元素。

```
frame = I("", {"type": "frame", "width": 1920, "height": 1080, "x": 0, "y": 1280, ...})
nav = I(frame.id, {"type": "frame", "width": "fill_container", "height": 64, ...})
logo = I(nav.id, {"type": "text", "content": "Logo", ...})
body = I(frame.id, {"type": "frame", "width": "fill_container", "height": "fill_container", "layout": "horizontal", ...})
...
```

### 图标绘制

**优先使用 `icon_font` 类型 + Lucide 字体**，这是 Pencil 原生支持的图标方案。

```
# 标准图标（外层 frame 容器 + icon_font）
icon = I(parentId, {"type": "frame", "name": "Leading Icon", "width": 16, "height": 16, "layout": "none"})
I(icon.id, {"type": "icon_font", "width": 16, "height": 16, "iconFontName": "chevron-right", "iconFontFamily": "lucide", "fill": "$--foreground"})
```

| 属性 | 说明 |
|------|------|
| `iconFontFamily` | 固定为 `"lucide"` |
| `iconFontName` | Lucide 图标名，如 `plus`、`chevron-right`、`circle`、`search`、`settings` 等 |
| 外层 frame | 必须有，`layout: "none"`，固定尺寸（常用 16×16 或 20×20） |
| `fill` | 控制图标颜色 |

常用 Lucide 图标名：`plus`、`minus`、`x`、`check`、`chevron-right`、`chevron-down`、`circle`、`search`、`settings`、`home`、`user`、`bell`、`menu`、`arrow-right`、`info`、`alert-triangle`、`trash-2`

**何时用 `path` 手绘**：仅当 Lucide 没有所需图标时，用 SVG path 手绘（复杂度高，尽量避开）。

### 文本换行

Pencil 不支持 `flexWrap`。需要手动将长文本拆分为多个 text 节点。

### PC 端组件参考尺寸

| 组件 | 推荐尺寸 | 备注 |
|------|----------|------|
| 顶部导航栏 | fill_container × 56-64 | 水平布局，内含 logo + 导航链接 + 操作区 |
| 侧边栏 | 240-320 × fill_container | 固定宽度 |
| 卡片间距 | gap: 16-24 | |
| 内边距 | padding: 16-24 | |

### 移动端组件参考尺寸

| 组件 | 推荐尺寸 | 备注 |
|------|----------|------|
| 顶部导航 | fill_container × 44-56 | 含汉堡菜单图标 |
| 底部栏 | fill_container × 56-80 | 固定底部 |
| 卡片内边距 | padding: 16 | 左右留白 |
| 触控区域 | ≥ 44px | 按钮和可点击元素 |

## 变体行绘制（可选）

当草图中有组件交互状态变体（hover、active、disabled、空态、加载态、错误态等）时，在页面下方绘制变体行。

**何时跳过**：组件状态单一，或草图未要求展示多状态。

主页面只画默认态。变体以缩略图形式排列，遵循阶段 1 的变体行定位规则。

```
# 变体行绘制示例（PC 页面下方）
label = I(frame.id, {"type": "text", "content": "Hover", "x": 0, "y": 1180, ...})
variant = I(frame.id, {"type": "frame", "width": 940, "height": 540, "x": 0, "y": 1200, "layout": "vertical", ...})
# ... 绘制 hover 状态的组件

label2 = I(frame.id, {"type": "text", "content": "Disabled", "x": 980, "y": 1180, ...})
variant2 = I(frame.id, {"type": "frame", "width": 940, "height": 540, "x": 980, "y": 1200, "layout": "vertical", ...})
# ... 绘制 disabled 状态的组件
```

**注意**：变体行在同一个 `batch_design` 调用中与主页面一起完成。

## 页面说明卡片

每个页面右侧必须有说明卡片，记录草图和设计稿中无法表达的细节。

| 属性 | PC 说明 | Phone 说明 |
|------|---------|------------|
| 宽度 | 280px | 280px |
| 边框色 | `#4ecdc4`（青绿） | `#ff6b6b`（红色） |

### 说明卡片内容

只写设计稿无法表达的信息：

1. **布局行为** — 固定区域 vs 可滚动区域、吸顶/吸底
2. **交互说明** — 悬浮效果、点击行为、动画
3. **未展示状态** — 空状态、加载态、错误态
4. **响应式断点** — 如果同时有 PC 和 Phone 版本

## ⚠️ 不可避免的坑点

| 坑点 | 现象 | 处理方式 |
|------|------|----------|
| "wrong .pen file" 间歇性报错 | 同样的 filePath 参数有时成功有时失败 | 在 `--args` 中尝试包含和省略 `filePath` 两种方式；交替重试 |
| batch_design 部分执行 | 批量操作第一条成功后报错，产生幽灵节点 | 报错后立即调用 `get_editor_state` 检查，用 D() 清理残留节点 |

## 节点查询速查

实现过程中频繁需要查询节点状态。所有脚本位于 `scripts/` 目录，配合 batch_get 使用。

**重要前提**：`batch_get` 返回 `list`（不是 `{"nodes": [...]}`），且 `ids` 参数**不起过滤作用**——始终返回所有顶层节点。传任意已有 ID 即可触发返回。所有 batch_get 调用必须加 `--timeout 120000`。

### 两步调用模式

```bash
# 第一步：获取数据（固定写法，ids 传任意已有 ID）
mcporter call pencil.batch_get --args '{"ids": ["anyId"]}' --timeout 120000 > /tmp/pencil_output.json

# 第二步：用脚本处理（替换 TARGET_ID）
python3 scripts/node_tree.py /tmp/pencil_output.json TARGET_ID
```

### 查看编辑器全貌（最轻量，无需 batch_get）

```bash
mcporter call pencil.get_editor_state
```

### 可用脚本

| 脚本 | 用途 | 示例 |
|------|------|------|
| `scripts/node_tree.py` | 查看节点树结构（含子节点） | `python3 scripts/node_tree.py /tmp/pencil_output.json fkhZy` |
| `scripts/node_props.py` | 查看节点样式属性 | `python3 scripts/node_props.py /tmp/pencil_output.json fkhZy zbmY3` |
| `scripts/node_children.py` | 查看直接子节点 ID | `python3 scripts/node_children.py /tmp/pencil_output.json nVPnL` |
| `scripts/extract_tokens.py` | 提取所有 $-- Design Token | `python3 scripts/extract_tokens.py /tmp/pencil_output.json` |
| `scripts/diff_variants.py` | 对比多个组件变体属性 | `python3 scripts/diff_variants.py /tmp/pencil_output.json fkhZy zbmY3 9c1zX` |

### 查找画布空白区域

```bash
mcporter call pencil.find_empty_space_on_canvas --args '{"width": 1920, "height": 1080, "direction": "bottom", "padding": 200}' --timeout 120000
```

### 关键注意事项

- **mcporter 输出不能直接管道到 Python**，必须先 `> /tmp/pencil_output.json`
- **大节点（50KB+）会导致 MCP 断连**，避免一次查询整个设计系统
- **所有 batch_get 调用必须加 `--timeout 120000`**，默认 60s 超时不够

## 完成条件

所有页面绘制完成，每页附带说明卡片，**进入验证阶段**。
