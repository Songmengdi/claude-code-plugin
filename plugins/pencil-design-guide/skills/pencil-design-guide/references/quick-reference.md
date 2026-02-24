# Pencil 快速参考

## 图标设置

### Lucide 图标（推荐）

Pencil 使用 Lucide 图标库，这是最常用的图标系统。

```javascript
{
  type: "icon_font",
  iconFontFamily: "lucide",
  iconFontName: "chevron-down",  // 具体图标名称
  width: 16,
  height: 16,
  fill: "#9CA3AF"  // 图标颜色
}
```

### 常用 Lucide 图标

| 图标名称 | 用途 |
|---------|------|
| chevron-down | 下拉箭头 |
| chevron-up | 上拉箭头 |
| chevron-left | 左箭头 |
| chevron-right | 右箭头 |
| search | 搜索图标 |
| plus | 添加按钮 |
| minus | 删除按钮 |
| x | 关闭按钮 |
| check | 确认/成功 |
| settings | 设置 |
| user | 用户 |
| home | 首页 |
| menu | 菜单（汉堡图标） |
| bell | 通知 |
| calendar | 日期 |
| clock | 时间 |
| mail | 邮件 |
| phone | 电话 |
| info | 信息 |
| alert-circle | 警告 |
| trash | 删除 |

完整图标列表：https://lucide.dev/icons/

### 图标容器对齐

图标容器必须居中对齐：

```javascript
{
  // ... 图标属性
  justifyContent: "center",  // 水平居中
  alignItems: "center"       // 垂直居中
}
```

完整示例：
```javascript
I("parentId", {
  type: "frame",
  name: "icon-container",
  width: 24,
  height: 24,
  justifyContent: "center",
  alignItems: "center",
  children: [
    {
      type: "icon_font",
      iconFontFamily: "lucide",
      iconFontName: "chevron-down",
      width: 16,
      height: 16,
      fill: "#9CA3AF"
    }
  ]
})
```

---

## 对齐速查表

### Flexbox 容器对齐

| 需求 | 主轴属性 | 交叉轴属性 |
|------|---------|-----------|
| 水平居中 | justifyContent: "center" | - |
| 垂直居中 | - | alignItems: "center" |
| 完全居中 | justifyContent: "center" | alignItems: "center" |
| 左对齐 | justifyContent: "flex_start" | - |
| 右对齐 | justifyContent: "flex_end" | - |
| 顶部对齐 | - | alignItems: "flex_start" |
| 底部对齐 | - | alignItems: "flex_end" |
| 两端对齐 | justifyContent: "space_between" | - |
| 均匀分布 | justifyContent: "space_evenly" | - |
| 间距分布 | justifyContent: "space_around" | - |
| 基线对齐（文本） | - | alignItems: "baseline" |
| 拉伸填充 | - | alignItems: "stretch" |

### 文本对齐

| 需求 | 属性 |
|------|------|
| 左对齐（默认） | textAlign: "left" |
| 右对齐 | textAlign: "right" |
| 居中对齐 | textAlign: "center" |
| 两端对齐 | textAlign: "justify" |

### 布局方向

| 需求 | 属性 |
|------|------|
| 水平排列 | layout: "hbox" |
| 垂直排列 | layout: "vbox" |
| 自动布局 | layout: "auto" |

---

## 检查清单

### 操作前检查

使用此清单确保操作不会失败：

- [ ] **目标节点 ID 已确认存在**
  - 使用 `batch_get` 获取当前状态
  - 验证目标节点确实存在
  - 确认节点结构符合预期

- [ ] **没有在同一批次中引用刚创建的节点**
  - 检查批次中的所有操作
  - 新创建节点的 binding 只在当前批次有效
  - 下一批次必须使用实际 ID

- [ ] **如果使用了 Replace，已准备好使用新 ID**
  - Replace 会返回新的节点 ID
  - 旧 ID 立即失效
  - 后续操作必须使用新 ID

- [ ] **每批操作数 ≤ 25**
  - 计数批次中的操作数量
  - 如果超过 25 个，拆分成多个批次

- [ ] **了解当前设计结构**
  - 如果不熟悉结构，先用 batch_get 查看
  - 确认父节点和子节点的关系

### 操作后检查

- [ ] **立即用 get_screenshot 验证**
  - 检查节点是否出现在正确位置
  - 验证样式和布局符合预期
  - 及时发现并修复问题

- [ ] **检查返回结果中的实际 ID**
  - 记录每个操作返回的 ID
  - 用于后续批次的引用
  - 在注释中标记 ID 的用途

- [ ] **确认没有 fit_content 警告**
  - fit_content 警告表示尺寸可能不正确
  - 检查是否设置了合适的尺寸
  - 考虑调整布局或内容

- [ ] **验证节点层级结构**
  - 使用 batch_get 检查父子关系
  - 确认节点在正确的容器中

---

## 批次操作提示

### 批次大小

- **最大值**：每批不超过 25 个操作
- **推荐值**：每批 10-15 个操作，便于调试
- **拆分策略**：按逻辑分组（如创建所有父容器一批，添加子节点一批）

### 批次组织

**好的批次组织**：
```javascript
// 批次1：创建所有父容器
header=I("page", {type: "frame"})
main=I("page", {type: "frame"})
footer=I("page", {type: "frame"})

// 批次2：添加 header 内容
logo=I("header的实际ID", {type: "text"})
nav=I("header的实际ID", {type: "frame"})

// 批次3：添加 nav 子项
home=I("nav的实际ID", {type: "text"})
about=I("nav的实际ID", {type: "text"})
```

**不好的批次组织**：
```javascript
// 混合创建和引用 - 容易出错
header=I("page", {type: "frame"})
logo=I("header", {type: "text"})  // 可能失败
main=I("page", {type: "frame"})
content=I("main", {type: "text"})  // 可能失败
```

---

## 常见节点类型

| 类型 | 用途 | 常用属性 |
|------|------|---------|
| frame | 容器、布局 | layout, padding, gap |
| text | 文本 | content, fontSize, textAlign |
| rectangle | 矩形、背景 | fill, stroke, cornerRadius |
| icon_font | 图标 | iconFontFamily, iconFontName |
| image | 图片 | src, width, height |
| vector | 矢量图形 | pathData, fill |

---

## 常用颜色

```javascript
// 灰度
"#000000"  // 黑色
"#FFFFFF"  // 白色
"#9CA3AF"  // 中灰（常用图标色）
"#6B7280"  // 深灰
"#E5E7EB"  // 浅灰（边框）

// 常用主题色
"#3B82F6"  // 蓝色
"#10B981"  // 绿色
"#F59E0B"  // 黄色
"#EF4444"  // 红色
"#8B5CF6"  // 紫色
"#EC4899"  // 粉色
```
