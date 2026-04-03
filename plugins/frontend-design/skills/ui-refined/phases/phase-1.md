# 阶段 1：规划

## 目标

检查画布状态，定义 Design Token，规划组件规范，计算坐标防止页面覆盖。

## 步骤

### 1.1 检查画布

```bash
mcporter call pencil.get_editor_state
```

确认当前已有节点的位置。也可以用 `find_empty_space_on_canvas` 辅助判断，但不能替代手动计算。

### 1.2 画布布局规则

**防止页面互相覆盖，这是最关键的位置规则。**

#### 固定尺寸

| 设备 | 尺寸 |
|------|------|
| PC 端 | 1920 × 1080 |
| 移动端 | 375 × 812 |

#### 排列公式

横向：**页面 → 说明卡片**，纵向按组排列。每组间距 200px。

**风格卡片**（如果存在）放在 y=0。

**仅 PC**：

| 元素 | x | y |
|------|---|---|
| 第 N 组 PC | 0 | (N+1) × 1280 |
| 第 N 组 PC 说明 | 2020 | (N+1) × 1280 |

**仅 Phone**：

| 元素 | x | y |
|------|---|---|
| 第 N 组 Phone | 0 | (N+1) × 1012 |
| 第 N 组 Phone 说明 | 475 | (N+1) × 1012 |

**PC + Phone**：

| 元素 | x | y |
|------|---|---|
| 第 N 组 PC | 0 | (N+1) × 1280 |
| 第 N 组 PC 说明 | 2020 | (N+1) × 1280 |
| 第 N 组 Phone | 2400 | (N+1) × 1280 |
| 第 N 组 Phone 说明 | 2880 | (N+1) × 1280 |

> N 从 0 开始。(N+1) 是因为 y=0 预留给风格卡片。1280 = 1080 + 200，1012 = 812 + 200。

### 1.3 定义 Design Token

**实现页面之前，先建立统一的设计变量。** 用 `$--` 前缀变量统一管理颜色、圆角等属性值：

```
tokens = I("", {"type": "frame", "name": "DesignTokens"})
I(tokens.id, {"type": "text", "content": "$--primary", "name": "$--primary", "fill": "#6366f1"})
I(tokens.id, {"type": "text", "content": "$--background", "name": "$--background", "fill": "#0f1117"})
I(tokens.id, {"type": "text", "content": "$--border", "name": "$--border", "fill": "#2d333b"})
I(tokens.id, {"type": "text", "content": "$--card", "name": "$--card", "fill": "#161b22"})
I(tokens.id, {"type": "text", "content": "$--radius-m", "name": "$--radius-m", "fill": "#8b949e"})
```

使用时直接引用：`fill: $--primary`、`cornerRadius: $--radius-m`。

建议至少定义：主色、背景、卡片、边框、文字、强调色、圆角。

### 1.4 组件变体规范

同类组件的不同变体之间**只改必要属性**，其余继承基础样式：

| 变体类型 | 差异维度 | 示例（Button） |
|----------|----------|---------------|
| 类型变体 | `fill` + `stroke` | Default: `fill: $--primary`; Ghost: 无 fill，只有 stroke |
| 尺寸变体 | `height` + `padding` | standard: height 40, padding [10,16]; Large: height 48, padding [12,24] |

通用组件标记为可复用，命名格式 `ComponentName/Variant`：

```
btn = I("", {"type": "frame", "name": "Button/Default", "reusable": true, ...})
btnGhost = I("", {"type": "frame", "name": "Button/Ghost", "reusable": true, ...})
```

## 完成条件

画布坐标计算完成，Design Token 已定义，**停止并等待用户回应**。
