---
name: ui-implement
description: |
  从 Pencil 精细化设计稿（.pen 文件）中提取设计信息，用于指导前端代码实现。
  当用户要求基于设计稿实现前端页面、组件或样式时使用此技能。
  触发场景：用户提供 .pen 文件路径并要求实现代码时，或用户提到"根据设计稿"、"实现UI"、"从设计稿读取信息"等。
  不自动触发，用户需通过 /ui-implement 手动调用。
---

# UI 实现：从设计稿提取信息

用户提供 .pen 文件路径后，通过 Pencil MCP 工具提取设计信息。

## Pencil MCP 调用方式

所有 Pencil MCP 工具通过 `mcporter call` 调用，基本格式：

```bash
mcporter call pencil.<工具名> --args '<JSON参数>' --timeout <毫秒>
```

**关键参数**：
- `filePath` — .pen 文件的绝对路径，避免编辑器焦点切换导致错误
- `--timeout` — 大文件操作必须加 `--timeout 120000`

**并发限制**：不要同时发起多个 `batch_get` 调用，MCP 不支持并发，会导致 JSON 解析失败。

**输出处理**：mcporter 输出 JSON 到 stdout，可直接管道到 Python 处理。注意：管道时必须加 `2>/dev/null` 抑制 stderr 干扰。

```bash
mcporter call pencil.get_variables --args '{"filePath": "/path/to/file.pen"}' --timeout 30000 2>/dev/null | python3 -c 'import sys,json; data=json.load(sys.stdin); ...'
```

**Python 内联脚本注意**：用单引号包裹 Python 代码，内部用双引号。f-string 中不能使用 `\"`（Python 3.10 限制），需先将值赋给临时变量。

## 可用工具

| 工具 | 用途 | 调用格式 |
|------|------|----------|
| `get_variables` | 获取所有 Design Token | `--args '{"filePath": "..."}'` |
| `batch_get` | 获取节点树（支持 resolveVariables） | `--args '{"filePath": "...", "resolveVariables": true}'` |
| `get_editor_state` | 查看编辑器状态（当前文件） | `--args '{}'` |

## 提取流程

### Step 1: Design Token（设计变量）

Token 是设计系统的色彩和数值基础，直接映射为 CSS 变量 / Tailwind 主题。

```bash
mcporter call pencil.get_variables \
  --args '{"filePath": "/path/to/file.pen"}' \
  --timeout 30000 2>/dev/null
```

或管道提取为代码可用的格式：

```bash
mcporter call pencil.get_variables \
  --args '{"filePath": "/path/to/file.pen"}' \
  --timeout 30000 2>/dev/null | python3 -c '
import sys, json
data = json.load(sys.stdin)
for name, token in data.get("variables", {}).items():
    print(f"{name}: {token[\"value\"]}  /* {token[\"type\"]} */")
'
```

**代码映射**：`$--accent: #2383e2` → CSS 变量 `--accent: #2383e2;` 或 Tailwind 主题扩展。

### Step 2: 页面总览

了解设计稿包含哪些页面、变体和说明卡片。

```bash
mcporter call pencil.batch_get \
  --args '{"filePath": "/path/to/file.pen"}' \
  --timeout 120000 2>/dev/null | python3 -c '
import sys, json
data = json.load(sys.stdin)
for c in (data if isinstance(data, list) else data.get("nodes", data.get("children", []))):
    if isinstance(c, dict):
        cid = c["id"]
        print(f"{cid} ({c.get(\"name\",\"\")}) type={c[\"type\"]} {c.get(\"width\",\"\")}x{c.get(\"height\",\"\")}")
'
```

**识别规则**：
- **页面**：尺寸 1920×1080（PC）或 375×812（Phone）→ 代码实现的核心
- **变体**：name 含 `/`（如 `Button/Hover`、`Conv Item/Active`）→ 组件状态
- **说明卡片**：name 含 `Description` → 交互/布局行为说明
- **风格卡片**：通常是第一个子节点 → 配色/字体规范

### Step 3: 交互与布局说明

从说明卡片中提取代码无法从视觉获取的信息。

```bash
mcporter call pencil.batch_get \
  --args '{"filePath": "/path/to/file.pen", "resolveVariables": false}' \
  --timeout 120000 2>/dev/null | python3 -c '
import sys, json

data = json.load(sys.stdin)
nodes = data if isinstance(data, list) else data.get("nodes", data.get("children", []))

# 替换为实际的说明卡片 ID
DESC_ID = "DESCRIPTION_ID"

def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict): continue
        if n.get("id") == tid: return n
        r = find(n.get("children", []), tid)
        if r: return r
    return None

node = find(nodes, DESC_ID)
if node:
    for c in node.get("children", []):
        if isinstance(c, dict) and c.get("content"):
            cname = c.get("name", "")
            print(f"{cname}: {c[\"content\"]}")
'
```

重点关注：**布局行为**（固定/滚动/吸顶吸底）、**交互说明**（悬浮/点击/展开折叠）、**响应式**（PC/Phone 差异）。

### Step 4: 组件树结构

对每个需要实现的页面，递归读取组件树。这是最核心的步骤。

```bash
mcporter call pencil.batch_get \
  --args '{"filePath": "/path/to/file.pen", "resolveVariables": false}' \
  --timeout 120000 2>/dev/null | python3 -c '
import sys, json

data = json.load(sys.stdin)
nodes = data if isinstance(data, list) else data.get("nodes", data.get("children", []))
PAGE_ID = "PAGE_ID"

def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict): continue
        if n.get("id") == tid: return n
        r = find(n.get("children", []), tid)
        if r: return r
    return None

def tree(node, indent=0):
    prefix = "  " * indent
    nid = node["id"]
    name = node.get("name", "")
    ntype = node.get("type", "")
    w = node.get("width", "")
    h = node.get("height", "")
    layout = node.get("layout", "")
    # 文本节点显示内容，图标节点显示图标名
    extra = ""
    if ntype == "text":
        content = node.get("content", "")
        extra = f' "{content}"'
    elif ntype == "icon_font":
        icon = node.get("iconFontName", "")
        iw = node.get("width", "")
        ih = node.get("height", "")
        extra = f" icon={icon} {iw}x{ih}"
    print(f"{prefix}{nid} ({name}) [{ntype}] {w}x{h} layout={layout}{extra}")
    for c in node.get("children", []):
        if isinstance(c, dict):
            tree(c, indent + 1)

page = find(nodes, PAGE_ID)
if page:
    tree(page)
'
```

**组件识别**：
- `name` 是语义锚点：`Sidebar`、`Chat Area`、`Input Bar` 直接对应代码组件
- `layout` 决定 CSS 布局方向：`vertical` → flex-col，`horizontal` → flex-row
- `fill_container` → 撑满父容器

### Step 5: 组件样式详情

提取特定组件的精确样式值。

```bash
mcporter call pencil.batch_get \
  --args '{"filePath": "/path/to/file.pen", "resolveVariables": false}' \
  --timeout 120000 2>/dev/null | python3 -c '
import sys, json

data = json.load(sys.stdin)
nodes = data if isinstance(data, list) else data.get("nodes", data.get("children", []))
TARGET_IDS = ["id1", "id2", "id3"]  # 替换为目标组件 ID

def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict): continue
        if n.get("id") == tid: return n
        r = find(n.get("children", []), tid)
        if r: return r
    return None

PROPS = ["id","name","type","layout","width","height","fill","stroke","cornerRadius","gap","padding","justifyContent","alignItems","fontFamily","fontSize","fontWeight","content","iconFontName"]

for tid in TARGET_IDS:
    node = find(nodes, tid)
    if node:
        nname = node.get("name", "")
        print(f"=== {tid} ({nname}) ===")
        for p in PROPS:
            if p in node:
                print(f"  {p}: {node[p]}")
'
```

### Step 6: 变体状态

组件通常有多种状态（默认、悬浮、激活等），需要全部提取。

```bash
mcporter call pencil.batch_get \
  --args '{"filePath": "/path/to/file.pen", "resolveVariables": false}' \
  --timeout 120000 2>/dev/null | python3 -c '
import sys, json

data = json.load(sys.stdin)
nodes = data if isinstance(data, list) else data.get("nodes", data.get("children", []))
VARIANT_IDS = ["DEFAULT_ID", "HOVER_ID", "ACTIVE_ID"]  # 替换为变体 ID

def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict): continue
        if n.get("id") == tid: return n
        r = find(n.get("children", []), tid)
        if r: return r
    return None

PROPS = ["name","fill","stroke","cornerRadius","padding","gap","layout","justifyContent","alignItems","opacity"]

for tid in VARIANT_IDS:
    node = find(nodes, tid)
    if node:
        nname = node.get("name", "")
        print(f"--- {nname} ---")
        for p in PROPS:
            if p in node:
                print(f"  {p}: {node[p]}")
        print()
'
```

变体命名规则：`ComponentName/State`（如 `Conv Item/Hover`）。

### 补充：获取解析后的实际色值

上述步骤默认使用 `resolveVariables: false`，输出变量引用（如 `$$--accent`）。如需直接获取解析后的实际值，将参数改为 `true`：

```bash
mcporter call pencil.batch_get \
  --args '{"filePath": "/path/to/file.pen", "resolveVariables": true}' \
  --timeout 120000 2>/dev/null | python3 -c '
import sys, json

data = json.load(sys.stdin)
nodes = data if isinstance(data, list) else data.get("nodes", data.get("children", []))
TARGET_IDS = ["id1", "id2"]

def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict): continue
        if n.get("id") == tid: return n
        r = find(n.get("children", []), tid)
        if r: return r
    return None

PROPS = ["id", "name", "fill", "stroke", "cornerRadius"]

for tid in TARGET_IDS:
    node = find(nodes, tid)
    if node:
        nname = node.get("name", "")
        print(f"=== {tid} ({nname}) ===")
        for p in PROPS:
            if p in node:
                print(f"  {p}: {node[p]}")
'
```

输出示例：`fill: #2383e2`（而非 `fill: $$--accent`）。适用于需要快速确认实际色值的场景。

## 设计属性到代码的映射

### 布局 → Flexbox

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

### 视觉 → CSS

| Pencil | CSS |
|--------|-----|
| `fill: "$$--accent"` | `background-color: var(--accent)` |
| `stroke: {"thickness": 1, "fill": "$$--border"}` | `border: 1px solid var(--border)` |
| `cornerRadius: "$$--radius-s"` | `border-radius: var(--radius-s)` |

### 文本 → CSS

| Pencil | CSS |
|--------|-----|
| `fill: "$$--foreground"` | `color: var(--foreground)` |
| `fontFamily: "Inter"` | `font-family: Inter` |
| `fontSize: 13` | `font-size: 13px` |
| `fontWeight: "600"` | `font-weight: 600` |

### 图标 → Lucide 组件

| Pencil | 代码 |
|--------|------|
| `type: "icon_font"` | lucide 图标库 |
| `iconFontName: "chevron-down"` | `<ChevronDown />`（kebab-case → PascalCase） |
| `width/height: 14` | `size={14}` |

## .pen 数据结构速查

> 完整结构见 `references/design-structure.md`

**4 种节点类型**：

| 类型 | 用途 | 关键属性 |
|------|------|----------|
| `frame` | 容器/组件 | layout, gap, padding, justifyContent, alignItems, fill, cornerRadius, stroke |
| `text` | 文本 | content, fill, fontFamily, fontSize, fontWeight（不支持 layout/padding/gap） |
| `rectangle` | 矩形/分隔线 | fill, width, height（不可含子节点） |
| `icon_font` | 图标（lucide） | iconFontName, width, height, fill |

**变量引用**：`"$$--accent"`（双 `$`）引用 variables 中 `"$--accent"` 的值。`resolveVariables: true` 可查看解析后的实际值。

**尺寸关键字**：`"fill_container"` = 撑满父容器，`"fit_content(0)"` = 自适应内容。

## 实现建议

1. **先建 Token 体系**：将 Design Token 转为 CSS 变量或主题配置
2. **再搭页面骨架**：根据组件树确定嵌套关系和布局方向
3. **逐组件填充样式**：从叶子节点（文本/图标）开始，逐层向上
4. **最后处理交互**：根据说明卡片添加事件处理和状态切换
5. **变体对应状态**：Hover/Active/Disabled 等变体对应 CSS 伪类或组件 state
