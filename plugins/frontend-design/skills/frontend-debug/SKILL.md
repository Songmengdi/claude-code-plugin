---
name: frontend-debug
description: |
  使用 Chrome DevTools MCP 调试前端问题。支持页面导航、交互操作、控制台日志、网络请求监控、性能分析、**视觉分析**等能力。

  触发场景：
  - 调试网页、检查页面行为、查看控制台错误
  - "调试这个页面"、"控制台有什么错误"、"测试登录流程"
  - "前端为什么不工作"、"检查网络请求"、"帮我操作这个页面"
  - **"页面布局有问题"、"UI 显示不正确"、"帮我看看这个页面的样式"**

  需要 chrome-devtools 和 analysis-images MCP 已配置。
---

# 前端调试 Skill

使用 Chrome DevTools MCP 进行前端调试，支持页面交互、日志分析、网络监控、**视觉分析**等。

## 前置条件

确保已安装以下 MCP：

```bash
# 检查 chrome-devtools
mcporter list chrome-devtools

# 检查 analysis-images（视觉分析）
mcporter list analysis-images
```

若未配置，参考 mcporter-setup skill 进行安装。

---

## 调试流程

### 1. 打开页面

```bash
# 新开标签页
mcporter call chrome-devtools.new_page --args '{"url": "http://localhost:5173"}'

# 或在当前页导航
mcporter call chrome-devtools.navigate_page --args '{"type": "url", "url": "http://example.com"}'
```

### 2. 获取页面快照

快照基于 a11y 树，提供元素 uid 用于后续操作：

```bash
mcporter call chrome-devtools.take_snapshot
```

输出示例：
```
uid=1_0 RootWebArea "Page Title"
  uid=1_1 heading "Welcome"
  uid=1_2 textbox "Username"
  uid=1_3 button "Submit"
```

### 3. 页面交互

```bash
# 填写表单
mcporter call chrome-devtools.fill --args '{"uid": "1_2", "value": "test@example.com"}'

# 点击元素
mcporter call chrome-devtools.click --args '{"uid": "1_3"}'

# 按键操作
mcporter call chrome-devtools.press_key --args '{"key": "Enter"}'

# 等待文本出现
mcporter call chrome-devtools.wait_for --args '{"text": ["Success", "Welcome"]}'
```

### 4. 查看控制台日志

```bash
# 列出所有日志
mcporter call chrome-devtools.list_console_messages

# 获取特定日志详情
mcporter call chrome-devtools.get_console_message --args '{"msgid": 23}'

# 过滤错误日志
mcporter call chrome-devtools.list_console_messages --args '{"types": ["error", "warn"]}'
```

### 5. 网络请求监控

```bash
# 列出所有请求
mcporter call chrome-devtools.list_network_requests

# 获取特定请求详情
mcporter call chrome-devtools.get_network_request --args '{"reqid": 1}'

# 过滤请求类型
mcporter call chrome-devtools.list_network_requests --args '{"resourceTypes": ["xhr", "fetch"]}'
```

### 6. 视觉分析（看图分析）

> **结合 analysis-images MCP，你可以"看"截图并分析视觉问题**

```bash
# 1. 截图保存到文件
mcporter call chrome-devtools.take_screenshot --args '{"filePath": "/tmp/page.png"}'

# 2. AI 分析图片
mcporter call analysis-images.analysis_image --args '{
  "prompt": "分析这个页面的布局结构，指出可能存在的 UI 问题",
  "path": "/tmp/page.png"
}'
```

**适用场景**：
- 检查布局是否正确
- 分析 CSS 样式问题
- 验证响应式设计
- 发现视觉 bug
- 对比预期效果

**分析提示词示例**：
```json
// 布局分析
"描述页面的整体布局结构，header、content、footer 的排列是否合理"

// 样式检查
"检查按钮、表单、卡片等组件的样式是否一致，有无明显的视觉问题"

// 响应式检查
"分析当前视口下的布局是否有溢出、重叠等问题"

// 对比分析
"对比设计稿，列出页面上与设计不符的地方"
```

### 7. 性能分析

```bash
# 开始性能追踪
mcporter call chrome-devtools.performance_start_trace --args '{"reload": true, "autoStop": true}'

# 停止追踪
mcporter call chrome-devtools.performance_stop_trace

# Lighthouse 审计
mcporter call chrome-devtools.lighthouse_audit --args '{"mode": "navigation"}'
```

---

## 常见调试场景

### 场景1: 调试登录流程

```bash
# 1. 打开登录页
mcporter call chrome-devtools.new_page --args '{"url": "http://localhost:5173/login"}'

# 2. 获取快照
mcporter call chrome-devtools.take_snapshot

# 3. 填写凭证
mcporter call chrome-devtools.fill --args '{"uid": "<input-uid>", "value": "user@example.com"}'
mcporter call chrome-devtools.fill --args '{"uid": "<password-uid>", "value": "password123"}'

# 4. 提交
mcporter call chrome-devtools.click --args '{"uid": "<submit-uid>"}'

# 5. 检查结果
mcporter call chrome-devtools.list_console_messages
mcporter call chrome-devtools.list_network_requests --args '{"resourceTypes": ["xhr", "fetch"]}'
```

### 场景2: 查找 JavaScript 错误

```bash
# 1. 打开页面
mcporter call chrome-devtools.new_page --args '{"url": "http://localhost:5173"}'

# 2. 等待页面加载
sleep 2

# 3. 查看错误日志
mcporter call chrome-devtools.list_console_messages --args '{"types": ["error"]}'

# 4. 获取错误详情
mcporter call chrome-devtools.get_console_message --args '{"msgid": <error-msgid>}'
```

### 场景3: 检查 API 请求

```bash
# 1. 执行操作触发请求
mcporter call chrome-devtools.click --args '{"uid": "<button-uid>"}'

# 2. 查看请求
mcporter call chrome-devtools.list_network_requests --args '{"resourceTypes": ["xhr", "fetch"]}'

# 3. 获取请求详情
mcporter call chrome-devtools.get_network_request --args '{"reqid": <reqid>}'

# 4. 保存请求/响应体
mcporter call chrome-devtools.get_network_request --args '{"reqid": <reqid>, "requestFilePath": "/tmp/request.json", "responseFilePath": "/tmp/response.json"}'
```

### 场景4: 视觉/布局问题调试

```bash
# 1. 打开页面
mcporter call chrome-devtools.new_page --args '{"url": "http://localhost:5173/dashboard"}'

# 2. 等待渲染完成
sleep 2

# 3. 截图
mcporter call chrome-devtools.take_screenshot --args '{"filePath": "/tmp/dashboard.png"}'

# 4. AI 分析布局
mcporter call analysis-images.analysis_image --args '{
  "prompt": "分析这个仪表板页面的布局：1) 整体结构是否合理 2) 卡片间距是否一致 3) 有无元素溢出或重叠",
  "path": "/tmp/dashboard.png"
}'

# 5. 如果发现问题，检查相关 CSS
# 结合 take_snapshot 获取元素 uid，定位具体元素
```

---

## 调试方法选择指南

| 问题类型 | 推荐方法 |
|---------|---------|
| JS 错误、逻辑问题 | `list_console_messages` + 源码分析 |
| 网络请求问题 | `list_network_requests` + `get_network_request` |
| 交互流程问题 | `take_snapshot` + `click`/`fill` |
| **布局/样式问题** | `take_screenshot` + `analysis_image` |
| 性能问题 | `performance_start_trace` + `lighthouse_audit` |
| 页面结构问题 | `take_snapshot`（a11y 树） |

---

## 注意事项

1. **元素 uid 会变化** - 每次页面更新后，需要重新获取快照
2. **消息 ID 递增** - 控制台消息 ID 随新消息增加
3. **请求保留** - 最近 3 次导航的请求会被保留
4. **超时设置** - 复杂操作可设置 timeout 参数（毫秒）
5. **视觉分析** - 截图后用 analysis-images 分析，你才能"看"到图片内容
