# 节点查询与脚本

## 默认方式：直接读 .pen 文件

`.pen` 文件就是 JSON，结构与 `batch_get` 返回值相同，用 Python 直接处理。

```python
import json
data = json.load(open('/path/to/file.pen'))

# 递归查找节点
def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict): continue
        if n.get('id') == tid: return n
        r = find(n.get('children', []), tid)
        if r: return r
    return None

node = find(data.get('children', []), 'TARGET_ID')
print(json.dumps(node, indent=2, ensure_ascii=False))
```

**注意**：直接读文件拿到的是**磁盘上的快照**，如果刚通过 `batch_design` 修改过节点，需要等 Pencil 保存后再读取才能看到最新状态。

## scripts/ 目录工具

所有脚本支持直接传入 .pen 文件路径：

```bash
python3 scripts/node_tree.py /path/to/file.pen TARGET_ID
python3 scripts/node_props.py /path/to/file.pen ID1 ID2
python3 scripts/node_children.py /path/to/file.pen ID
python3 scripts/extract_tokens.py /path/to/file.pen
python3 scripts/diff_variants.py /path/to/file.pen ID1 ID2
```

## batch_get（仅小文件可用）

仅当 .pen 文件很小时才使用 `batch_get`。返回 `list`（不是 `{"nodes": [...]}`），且 `ids` 参数**不起过滤作用**——始终返回所有顶层节点。必须加 `--timeout 120000`。

```bash
mcporter call pencil.batch_get --args '{"ids": ["anyId"]}' --timeout 120000 > /tmp/pencil_output.json
python3 scripts/node_tree.py /tmp/pencil_output.json TARGET_ID
```

## 查找画布空白区域

```bash
mcporter call pencil.find_empty_space_on_canvas --args '{"width": 1920, "height": 1080, "direction": "bottom", "padding": 200}' --timeout 120000
```

## 自动布局脚本（auto_layout.py）

绘制完所有变体后，使用 `auto_layout.py` 自动计算紧凑间距，替代手动 y 坐标计算。

```bash
# 多组变体排列（每组逗号分隔 ID）
python3 scripts/auto_layout.py /path/to/file.pen \
  --groups "collapsed_id,expanded_id" "variant1_id,variant2_id" \
  --start-y 2460 --gap 24 --group-gap 60
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--nodes` | 单组 ID 列表 | — |
| `--groups` | 多组，每组逗号分隔 ID | — |
| `--start-y` | 起始 y 坐标 | 0 |
| `--gap` | 组内间距 (px) | 24 |
| `--group-gap` | 组间距 (px) | 60 |

脚本会递归估算每个节点的渲染高度，输出可直接执行的 `batch_design` 命令。

## 导出图片

```bash
mcporter call pencil.export_nodes --args '{"filePath": "绝对路径", "nodeIds": ["frameId"], "format": "png", "scale": 1, "outputDir": "/tmp"}'
```

## 自动化分析

**仅在用户主动要求时才使用。**

```bash
mcporter call analysis-images.analysis_images --args '{"paths": ["/tmp/exported.png"], "prompts": ["检查是否有重复元素、布局重叠、对齐问题、文字截断、间距不一致等常见UI异常"]}' --timeout 120000
```

**不要完全信任分析结果。** analysis-images 可能漏报，关键问题应以用户判断为准。

## 关键注意事项

- **mcporter 输出不能直接管道到 Python**，必须先 `> /tmp/pencil_output.json`
- **大节点（50KB+）会导致 MCP 断连**，避免一次查询整个设计系统
