# 阶段 0：准备

## 目标

了解工具能力，读取 Excalidraw 草图结构，与用户确认设计风格。

## 步骤

### 0.1 认识工具

```bash
mcporter list pencil && mcporter list analysis-images
```

核心工具速查：

| 工具 | 用途 |
|------|------|
| `batch_design` | 批量操作节点（I/C/U/R/M/D/G） |
| `batch_get` | 获取节点详细信息 |
| `get_editor_state` | 获取当前编辑器状态（轻量） |
| `export_nodes` | 导出节点为图片 |
| `open_document` | 打开 .pen 文件 |
| `find_empty_space_on_canvas` | 查找画布空白区域 |

调用格式：
```bash
mcporter call pencil.batch_design --args '{"operations": "..."}' --timeout 120000
```

### 0.2 读取草图

**必须通过 MCP 读取 Excalidraw 草图**，不要直接读取 JSON 文件。

```bash
mcporter call excalidraw.get_resource --args '{"resource": "elements"}' \
  | jq '[.elements[] | {id, type, x: (.x | floor), y: (.y | floor), w: (.width | floor), h: (.height | floor),
    text: (if .type == "text" then .text else empty end)}]'
```

从草图中提取：
1. **页面列表** — 大矩形（width ≥ 300, height ≥ 300）为页面边界
2. **组件结构** — 内部矩形为功能区域（导航栏、侧边栏、内容区等）
3. **文字标注** — text 元素为标签和说明
4. **说明卡片** — 草图的说明卡片包含布局行为、交互说明等关键信息

### 0.3 风格讨论

通过 AskUserQuestion 与用户头脑风暴，确定设计风格。**不要直接给预设风格表让用户选**——根据草图类型和用户回答，自行引导对话、提炼色板（背景/卡片/边框/文字/强调色/字体/圆角），确认后再进入实现。

#### 风格预览

确认风格后，创建风格预览卡片让用户最终确认：

```
风格预览卡片布局（放在画布 y=0 位置）：
┌─────────────────────────────────┐
│  风格名称                        │
│  ─────────────────────────────── │
│  色板展示（背景/卡片/边框/文字色块）│
│  字体示例文字                    │
│  典型组件预览（按钮/卡片/标签）   │
└─────────────────────────────────┘
```

**用户确认风格后，立即删除未选中的风格预览帧。** 不要让多个风格帧残留在画布上。

## 完成条件

草图结构分析完成，设计风格已确认，**停止并等待用户回应**。
