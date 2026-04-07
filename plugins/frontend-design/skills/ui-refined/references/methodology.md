# Pencil MCP 安全操作方法论

## 核心原则：先读后写，信任原子性

每一步操作遵循：**确认状态 → 规划变更 → 执行（信任 batch_design 原子性）→ 必要时验证**。

## 工具链

以下脚本位于 `scripts/` 目录，替代手动 Python 代码：

| 脚本 | 用途 | 需要磁盘已保存 |
|------|------|----------------|
| `safe_batch.py` | 执行 batch_design（**首选执行方式**） | 否（直接操作内存） |
| `node_info.py` | 节点摘要（类型、尺寸、布局、子节点、父路径） | **是** |
| `node_children.py` | 子节点 ID 列表 | **是** |
| `verify.py` | 批量验证（存在/缺失/顺序/属性） | **是** |
| `auto_layout.py` | 自动排列变体间距 | **是** |

所有脚本直接传入 .pen 文件路径，无需先 batch_get。

## 操作流程

### 1. 修改前：确认状态

```bash
# 了解目标节点（支持多节点）
python3 scripts/node_info.py file.pen id1 id2 id3

# 如需确认父节点的子节点顺序
python3 scripts/node_children.py file.pen PARENT_ID
```

需要确认的关键信息：
- **节点类型** — text/frame/rectangle，决定可用属性
- **父节点** — 决定 I() 的 parentId 和 M() 的目标
- **子节点顺序** — 决定 M() 的 index
- **是否已有显式 height** — 有则 U() 无法改为 fit_content

### 2. 规划变更

#### 2.1 结构变更必须先画节点树

**这是最容易犯错的地方。** 修改或新增涉及多层嵌套的组件时，不要直接开始写 I/U/M 操作。先在回复中画出**目标节点树**，明确每个属性属于哪一层。

**错误做法**：看到"加个删除图标"，直接改父容器 layout=horizontal，导致所有子节点挤在一行。

**正确做法**：先画出目标树，确认层级关系，再分批执行。

```
# 示例：给会话卡片右侧加删除图标（仅 Hover 态）

# 先画目标节点树：
FtwgH (horizontal, space_between, center)
├── hMcKA/textGroup (vertical, gap:2, fill_container)
│   ├── isUtC  "标题"
│   └── EzF9G  "时间"
└── hTCAr/trash-2 icon

# 然后规划执行顺序：
# Batch 1: I() 创建 textGroup
# Batch 2: M() 把文本移入 textGroup，M() 图标移到 textGroup 后面
# Batch 3: U() 设置 FtwgH 的布局属性
```

**节点树的作用**：
- 强迫你思考每个属性属于哪一层（layout 在容器层，fill 在视觉层）
- 避免属性加错层级（如 cornerRadius 加到外层背景而不是内层卡片）
- 避免遗漏中间层（如水平布局需要先把纵向元素包裹成子 frame）

#### 2.2 属性分层原则

| 属性类型 | 属于哪一层 | 示例 |
|----------|-----------|------|
| 布局属性 | **容器层** | layout, gap, padding, justifyContent, alignItems |
| 视觉属性 | **视觉元素层** | fill, stroke, cornerRadius, effects |
| 内容属性 | **叶子节点** | content(text), iconFontName(icon_font) |

一个常见的错误模式：把视觉属性（如 cornerRadius）加到了外层布局容器上，而实际应该加在内层视觉卡片上。**画节点树可以避免这类错误。**

#### 2.3 变更策略

| 场景 | 策略 |
|------|------|
| 修改属性 | 确认类型兼容后 U() 部分更新 |
| 调整层级/顺序 | **I() 创建获取真实 ID → 下一批用真实 ID 执行 M()**（M() 不能与变量绑定同批） |
| 删除后重建 | D() 清理 → verify 确认删除 → I() 重建 |
| 新增到指定位置 | I() 追加到末尾 → M() 移到目标 index |
| 结构变更（改嵌套/布局） | **先画节点树 → 再分批执行** |

**不可逆操作**（U() 无法做到）：
- 将已有 `height` 改为 `fit_content` — 需删除重建
- 改变节点 `type`
- 移除已有属性

**批次拆分原则**：
- 每批最多 8-10 个操作
- M() 必须用真实 ID，不能和变量绑定在同一批

### 3. 执行

**使用 `safe_batch.py` 执行：**

```bash
# 创建节点
python3 scripts/safe_batch.py file.pen 'x = I("parentId", {...})'

# 删除节点
python3 scripts/safe_batch.py file.pen 'D("oldId")'

# 修改属性
python3 scripts/safe_batch.py file.pen 'U("id", {"content": "new text"})'

# 调整顺序
python3 scripts/safe_batch.py file.pen 'M("a", "parentId", 0)'
```

**信任 batch_design 原子性：** 返回 success = 所有操作已执行，无需额外验证。

退出码：0 = 成功，1 = 失败。

### 4. 验证（按需）

当需要确认操作结果时（如批量删除、调试问题），单独使用 `verify.py`：

```bash
# 验证节点存在
python3 scripts/verify.py file.pen --exists id1 id2

# 验证节点已删除
python3 scripts/verify.py file.pen --missing oldId

# 验证子节点顺序
python3 scripts/verify.py file.pen --order parentId a b c

# 验证属性值
python3 scripts/verify.py file.pen --prop id content "new text"
```

**⚠️ Pencil MCP 没有保存功能。** batch_design 只修改内存状态，不会写入磁盘。

磁盘读取类脚本（`auto_layout.py`、`verify.py`、`node_info.py`、`node_children.py`）读取的是磁盘上的 .pen 文件，看不到内存中的最新变更。

**操作流程：**
1. 执行 batch_design 操作（内存变更）
2. 用户在 Pencil 中手动保存（Cmd+S）
3. 再运行磁盘读取类脚本

**不要用 batch_get 验证大文件（>200KB），会导致 SIGSEGV 崩溃。**

### 5. 错误恢复

#### "wrong .pen file" 错误

**不要立即重试。** 此错误具有歧义性：操作可能已成功写入内存。

```bash
# 先验证操作是否已生效（需等待磁盘同步）
python3 scripts/verify.py file.pen --exists newId  # 或 --missing / --order

# 已生效 → 不需要重试
# 未生效 → open_document 后重试
```

#### batch_design 操作失败

batch_design 有原子性：一条失败，整批回滚。检查是否有幽灵节点：

```bash
# 检查父节点子节点是否符合预期
python3 scripts/node_children.py file.pen PARENT_ID

# 有幽灵节点 → D() 清理 → verify 确认 → 重新执行
```
