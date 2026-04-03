# 画布保存与恢复

excalidraw MCP 没有原生的 save/export/import 工具，通过获取元素数据 + 批量创建实现保存和恢复。

## 文件位置

草图 JSON 统一存放在项目根目录下的 `ui-sketch/` 目录，便于 git 管理。

```
<项目根>/
└── ui-sketch/
    ├── blog.json          # 博客页面草图
    └── dashboard.json     # 后台草图
```

## 快速使用

```bash
# 保存画布到 ui-sketch/<name>.json
python scripts/save_canvas.py blog

# 恢复画布（清空当前画布后写入）
python scripts/restore_canvas.py blog

# 追加恢复，不清空现有内容
python scripts/restore_canvas.py blog --no-clear

# 自定义目录
python scripts/save_canvas.py blog --path ./sketches
```

## 原理

```
保存: get_resource(elements) → 写入 JSON
恢复: 读取 JSON → clear_canvas → 清理只读字段 → 修正类型 → 分批 batch_create_elements
```

`get_resource` 返回的元素含只读字段（id、seed、syncedAt 等），`batch_create_elements` 不接受，恢复时自动清理。

## 踩坑记录

| 问题 | 原因 | 处理 |
|------|------|------|
| `fontFamily` 报错 | 返回数字，API 要求字符串 | 转为 `str` |
| `points` 报错 | 返回 `[[x,y]]`，API 要求 `[{x,y}]` | 转换格式 |
| 批量创建失败 | 每批上限 25 个元素 | 自动分批 |
| 恢复覆盖现有内容 | 默认会先清空画布 | 用 `--no-clear` 追加 |
