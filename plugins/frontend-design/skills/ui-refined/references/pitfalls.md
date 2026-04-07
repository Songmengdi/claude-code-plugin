# 踩坑点合集

## 布局相关

### 显式 height 导致内容溢出

**现象**：设置 `height: 200` 但子内容超过 200px，内容被裁剪。

**处理**：不设置 height 或使用 `"fit_content"`，让 Pencil 自动计算。

### fit_content 在 U() 中不生效

**现象**：通过 U() 设置 `"fit_content"` 后文件未变化。

**处理**：U() 无法移除已有 height 属性；需删除节点重建，或在创建时（I()）就不设 height。

### text + icon_font 作为独立子节点

**现象**：在 `space_between` 布局中，文本和图标被均匀分布而非紧挨。

**处理**：将文本和图标包裹在一个子 frame 中（如 `{"type": "frame", "gap": 4, "alignItems": "center"}`）。

### space_between 三元素分布错误

**现象**：标签、耗时、按钮三者在父容器中被均匀分布。

**处理**：将耗时+按钮包裹进 Right frame，让 `space_between` 只作用在左标签和右容器之间。

### icon_font 不需要 wrapper frame

**现象**：`layout:none` 的 wrapper frame 内放 icon_font 是多余的。

**处理**：icon_font 可直接放在 flex 容器中，Pencil 会正确布局。

> 详细 Flex 布局规则见 `references/drawing-guide.md`。

## 变量与绑定相关

### 变量绑定引用错误

**现象**：`send.id` 报错 `<MemberExpression>`。

**处理**：绑定变量直接用变量名 `send`，不加 `.id`。

## MCP 连接相关

### MCP "wrong .pen file"

**现象**：batch_design 频繁报错。

**处理**：重新 `open_document` 后重试；始终在 `--args` 中显式传入 `filePath`。

**关键**：此错误具有歧义性——操作可能已经成功写入 .pen 文件，只是返回了连接错误。**重试前必须先通过 Python 读取 .pen 文件验证当前节点状态**，否则可能导致重复创建或遗漏清理。

### batch_design 结果缓存

**现象**：连续调用返回 `identical to result` 但实际未执行。

**处理**：用 `open_document` 刷新连接，或读取 .pen 文件验证。

### batch_design 部分执行（幽灵节点）

**现象**：批量操作第一条成功后报错，产生残留节点。

**处理**：报错后立即调用 `get_editor_state` 检查，用 D() 清理残留节点。

### batch_get 大文件崩溃

**现象**：.pen 文件过大（>200KB）时 batch_get 导致 MCP 进程崩溃。

**处理**：改为直接读 .pen 文件用 Python 处理（见 `references/node-operations.md`）。

## 命令行相关

### mcporter 输出不能直接管道到 Python

**现象**：`mcporter call ... | python3` 解析失败。

**处理**：必须先 `mcporter call ... > /tmp/pencil_output.json`，再 `python3 scripts/xxx.py /tmp/pencil_output.json`。

### 大节点查询导致 MCP 断连

**现象**：一次查询整个设计系统或 50KB+ 节点导致断连。

**处理**：避免一次查询大节点，改为直接读 .pen 文件处理。
