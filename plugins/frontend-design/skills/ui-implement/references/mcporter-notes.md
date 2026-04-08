# mcporter 调用注意事项

## stderr 干扰

`mcporter call` 偶尔向 stderr 输出信息，管道到 Python 时必须加 `2>/dev/null`：

```bash
mcporter call pencil.batch_get --args '...' --timeout 120000 2>/dev/null | python3 -c '...'
```

不加会导致 `json.load` 解析失败（stdin 混入了非 JSON 内容）。

## Python 内联脚本

用单引号 `'...'` 包裹 Python 代码，内部用双引号。

**f-string 中不能用 `\"`**（Python 3.10 限制），需先将值赋给临时变量：

```python
# 错误
print(f"{node[\"id\"]}")  # SyntaxError

# 正确
nid = node["id"]
print(f"{nid}")
```

## 并发限制

不可同时发起多个 `batch_get` 调用，MCP 不支持并发，会导致 JSON 解析失败或返回空数据。每次只调用一个，等返回后再发起下一个。

## 错误处理

- **"wrong .pen file"**：操作可能已成功写入内存。先验证结果，再决定是否重试
- **JSON 解析失败**：检查是否漏了 `2>/dev/null`，或是否有并发调用
- **返回空数据**：检查 `filePath` 是否为绝对路径，确认 Pencil 编辑器已打开对应文件
- **超时**：加大 `--timeout` 值（大文件用 120000）
