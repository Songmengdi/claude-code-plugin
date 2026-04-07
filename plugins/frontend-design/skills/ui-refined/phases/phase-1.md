# 阶段 1：规划

## 目标

检查画布状态，定义 Design Token，规划组件规范，计算坐标防止页面覆盖。

## 步骤

### 1.1 检查画布

```bash
mcporter call pencil.get_editor_state
```

确认当前已有节点的位置。也可以用 `find_empty_space_on_canvas` 辅助判断，但不能替代手动计算。

### 1.2 计算画布坐标

按画布布局规则计算所有页面的坐标位置，防止页面互相覆盖。

### 1.3 定义 Design Token

**实现页面之前，必须使用 `set_variables` 工具在 Pencil 中定义设计变量。** 不要用文本节点展示——`set_variables` 创建的变量才能被组件引用。

建议至少定义：主色、背景、卡片、边框、文字、辅助文字、强调色、圆角。

定义后用 `get_variables` 验证。

### 1.4 规划组件变体规范

同类组件的不同变体之间**只改必要属性**，其余继承基础样式。通用组件标记为可复用，命名格式 `ComponentName/Variant`。

## 完成条件

画布坐标计算完成，Design Token 已在 Pencil 中创建，**停止并等待用户回应**。
