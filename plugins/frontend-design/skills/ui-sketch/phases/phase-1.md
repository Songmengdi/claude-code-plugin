# 阶段 1：了解工具

## 目标

掌握 excalidraw MCP 提供的工具能力。

## 执行

```bash
mcporter list excalidraw
```

确认核心工具可用：

| 工具 | 用途 |
|------|------|
| `batch_create_elements` | 批量创建元素（主力工具） |
| `create_element` | 创建单个元素 |
| `update_element` | 修改已有元素 |
| `delete_element` | 删除元素 |
| `get_resource` | 获取画布资源（`elements` 查看所有元素） |
| `query_elements` | 按条件查询元素 |

调用格式：
```bash
mcporter call excalidraw.<tool> --args '{"key": "value"}'
```

## 完成条件

确认工具列表无误，进入阶段 2。
