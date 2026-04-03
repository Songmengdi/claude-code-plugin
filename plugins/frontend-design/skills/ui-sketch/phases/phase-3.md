# 阶段 3：检查画布

## 目标

了解画布已有内容，确定新页面的放置位置，避免覆盖。

## 执行

**始终用 `jq` 管道过滤 MCP 输出，只保留当前决策所需的最少字段。禁止直接使用原始 MCP 返回数据。**

根据目的选择合适的查询方式：

### 放置新页面（防覆盖）

只需边界框和说明卡片位置（~1.6KB）：

```bash
mcporter call excalidraw.get_resource --args '{"resource": "elements"}' \
  | jq '{
    total: (.elements | length),
    "y_max": ([.elements[] | .y + .height] | max),
    "x_max": ([.elements[] | .x + .width] | max),
    pages: [.elements[] | select(.type == "rectangle" and .width >= 300 and .height >= 300)
      | {id, x: (.x | floor), y: (.y | floor), w: (.width | floor), h: (.height | floor), bg: .backgroundColor}],
    labels: [.elements[] | select(.type == "text" and (.text | test("说明|页面|移动端|PC")))
      | {id, text, x: (.x | floor), y: (.y | floor)}]
  }'
```

用 `y_max` 和 `x_max` 计算新页面起始位置。

### 理解已有内容（恢复/继续编辑）

需要所有元素的类型、位置和文字（~11KB）：

```bash
mcporter call excalidraw.get_resource --args '{"resource": "elements"}' \
  | jq '[.elements[] | {id, type, x: (.x | floor), y: (.y | floor), w: (.width | floor), h: (.height | floor),
    text: (if .type == "text" then .text else empty end)}]'
```

### 定位特定元素（修改/删除）

按类型或位置精确查询：

```bash
# 按类型查
mcporter call excalidraw.query_elements --args '{"type": "rectangle"}' \
  | jq '[.[] | {id, x: (.x | floor), y: (.y | floor), w: (.width | floor), h: (.height | floor)}]'

# 按位置范围查（示例：查 y > 1000 的元素）
mcporter call excalidraw.get_resource --args '{"resource": "elements"}' \
  | jq '[.elements[] | select(.y > 1000) | {id, type, x: (.x | floor), y: (.y | floor), w: (.width | floor), h: (.height | floor)}]'
```

## 判断

- 画布为空 → 直接从 (0, 0) 开始
- 画布有内容 → 根据查询结果计算新位置

## 完成条件

确定新页面的起始坐标，进入阶段 4。
