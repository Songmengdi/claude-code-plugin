# Pencil 工具详细规则和操作流程

## 完整的5个避免失败规则

### 规则1：永远不要在同一批次中向刚创建的节点插入子节点

这是最常见的错误原因。当你在批次中创建一个新节点时，给它分配的 binding 名称只在当前批次中作为引用存在。一旦批次完成，这个节点会有一个实际生成的 ID，但 binding 名称就失效了。

**为什么失败**：
- 批次执行时，新节点还没有实际 ID
- binding 名称只是批次内的临时引用
- 下一批次无法解析这个 binding 名称

**正确做法**：
```javascript
// ===== 批次1：创建所有父容器 =====
container1=I("parent", {type: "frame", name: "Container 1"})
container2=I("parent", {type: "frame", name: "Container 2"})
container3=I("parent", {type: "frame", name: "Container 3"})
// 返回：container1="abc123", container2="def456", container3="ghi789"

// ===== 批次2：向 container1 添加子节点 =====
child1=I("abc123", {type: "text", content: "Child 1"})
child2=I("abc123", {type: "text", content: "Child 2"})

// ===== 批次3：向 container2 添加子节点 =====
child3=I("def456", {type: "text", content: "Child 3"})
child4=I("def456", {type: "text", content: "Child 4"})

// ===== 批次4：向 container3 添加子节点 =====
child5=I("ghi789", {type: "text", content: "Child 5"})
child6=I("ghi789", {type: "text", content: "Child 6"})
```

**预防措施**：
- 创建父容器后，立即提交一批
- 等待返回结果，记录所有实际 ID
- 下一批再向这些实际 ID 插入子节点

---

### 规则2：Replace 操作后，旧 ID 立即失效

Replace 操作会删除旧节点并创建新节点，旧节点 ID 不再存在。

**为什么失败**：
- Replace 不是修改，而是删除+创建
- 旧节点被删除，ID 失效
- 任何对旧 ID 的引用都会失败

**正确做法**：
```javascript
// ===== 批次1：替换节点 =====
newNode=R("oldId", {
  type: "frame",
  name: "New Container",
  // ... 其他属性
})
// 返回：newNode="xyz999"

// ===== 批次2：向新节点添加子节点 =====
child=I("xyz999", {type: "text", content: "Hello"})
```

**或者使用 batch_get 获取新 ID**：
```javascript
// ===== 批次1：替换节点 =====
R("oldId", {type: "frame", ...})

// ===== 批次2：获取新 ID =====
batch_get({nodeIds: ["oldId"]})  // 会返回新的实际 ID

// ===== 批次3：使用新 ID =====
child=I("新的实际ID", {type: "text"})
```

**预防措施**：
- Replace 后必须使用返回的新 ID
- 或者在下一批用 batch_get 获取新 ID
- 永远不要假设 ID 保持不变

---

### 规则3：binding 变量只在当前批次有效

这是规则1的延伸。任何 binding 赋值（如 `container=I(...)`）都只在当前批次中有效。

**为什么失败**：
- binding 是批次的内部引用机制
- 批次完成后，binding 解析为实际 ID
- 下一批次无法访问之前的 binding

**正确做法**：
```javascript
// ===== 批次1 =====
item1=I("parent", {type: "frame"})
item2=I("parent", {type: "frame"})
// 返回：item1="abc123", item2="def456"

// ===== 批次2：使用实际 ID，不使用 binding 名 =====
child1=I("abc123", {type: "text"})
child2=I("def456", {type: "text"})

// ❌ 不要这样
// child3=I("item1", {...})  // item1 未定义
```

**预防措施**：
- 记录每个操作返回的实际 ID
- 后续批次使用实际 ID，不使用 binding 名
- 可以在注释中标记实际 ID 的用途

---

### 规则4：操作前先确认节点存在

不要基于假设编写代码。目标节点可能不存在或 ID 已变更。

**为什么失败**：
- 节点可能已被删除或替换
- ID 可能来自之前的会话
- 设计结构可能已改变

**正确做法**：
```javascript
// ===== 步骤1：用 batch_get 获取实际结构 =====
batch_get({nodeIds: ["parentId"]})
// 返回确认 parentId 存在，返回详细信息

// ===== 步骤2：使用确认的 ID =====
child=I("确认的ID", {type: "text", content: "Hello"})
```

**预防措施**：
- 每次操作前用 batch_get 确认目标节点
- 检查返回的节点信息是否符合预期
- 不要基于假设或记忆编写 ID

---

### 规则5：同一批次只操作已存在的节点或创建独立节点

混合创建和引用是另一个常见错误。

**可以做的**：
```javascript
// ✅ 同一批次创建多个独立的父容器
container1=I("parent", {type: "frame"})
container2=I("parent", {type: "frame"})
container3=I("parent", {type: "frame"})

// ✅ 同一批次向已存在的节点添加子节点
child1=I("existingId1", {type: "text"})
child2=I("existingId2", {type: "text"})
child3=I("existingId3", {type: "text"})
```

**不可以做的**：
```javascript
// ❌ 混合创建和引用
container=I("parent", {type: "frame"})
child=I("container", {type: "text"})  // container 是刚创建的
```

**预防措施**：
- 设计结构时，先创建所有父容器
- 然后逐批向每个父容器添加内容
- 保持批次的"纯净性"：要么全创建，要么全引用

---

## 完整操作流程模板

### 创建复杂 UI 结构的标准流程

```javascript
// ===== 批次1：创建所有父容器 =====
header=I("page", {type: "frame", name: "Header"})
main=I("page", {type: "frame", name: "Main"})
footer=I("page", {type: "frame", name: "Footer"})
// 记录返回的实际 ID：header="xxx", main="yyy", footer="zzz"

// ===== 批次2：向 header 添加内容 =====
logo=I("xxx", {type: "text", content: "Logo"})
nav=I("xxx", {type: "frame", name: "Nav"})

// ===== 批次3：向 nav 添加菜单项 =====
item1=I("nav的实际ID", {type: "text", content: "Home"})
item2=I("nav的实际ID", {type: "text", content: "About"})

// ===== 批次4：向 main 添加内容 =====
hero=I("yyy", {type: "frame", name: "Hero"})
content=I("yyy", {type: "frame", name: "Content"})

// ===== 批次5：验证 =====
get_screenshot()
```

### 替换节点的标准流程

```javascript
// ===== 批次1：替换节点 =====
newContainer=R("oldContainerId", {
  type: "frame",
  name: "New Container",
  layout: "hbox",
  // ... 其他属性
})
// 返回：newContainer="newId123"

// ===== 批次2：向新节点添加子节点 =====
child1=I("newId123", {type: "text", content: "Item 1"})
child2=I("newId123", {type: "text", content: "Item 2"})

// ===== 批次3：验证 =====
get_screenshot()
```

### 批量更新节点的标准流程

```javascript
// ===== 批次1：获取当前状态 =====
batch_get({nodeIds: ["node1", "node2", "node3"]})

// ===== 批次2：逐个更新（使用 Replace） =====
new1=R("node1", {type: "text", content: "Updated 1"})
new2=R("node2", {type: "text", content: "Updated 2"})
new3=R("node3", {type: "text", content: "Updated 3"})
// 记录返回的新 ID

// ===== 批次3：验证 =====
get_screenshot()
```

---

## 调试技巧

### 1. 检查操作返回

每个批次返回的信息包含：
- 每个操作的实际生成 ID
- 操作状态（成功/失败）
- 错误信息（如果有）

### 2. 使用 get_screenshot

在关键步骤后截图检查：
- 确认节点创建在正确位置
- 验证样式和布局符合预期
- 及时发现问题

### 3. 使用 batch_get 验证

在操作前验证节点状态：
- 确认目标节点存在
- 检查节点当前属性
- 了解现有结构

### 4. 处理 fit_content 警告

如果看到 fit_content 警告：
- 检查是否设置了固定尺寸
- 确认内容是否超出容器
- 考虑使用 auto 布局
