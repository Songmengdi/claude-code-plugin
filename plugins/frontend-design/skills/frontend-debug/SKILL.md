---
name: frontend-debug
description: |
  使用 Chrome DevTools MCP 调试前端问题。支持页面导航、交互操作、控制台日志、网络请求监控、性能分析、**视觉分析**等能力。

  触发场景：
  - 调试网页、检查页面行为、查看控制台错误
  - "调试这个页面"、"控制台有什么错误"、"测试登录流程"
  - "前端为什么不工作"、"检查网络请求"、"帮我操作这个页面"
  - **"页面布局有问题"、"UI 显示不正确"、"帮我看看这个页面的样式"**

disable-model-invocation: true
---

# 前端调试 Skill

使用 Chrome DevTools MCP 进行前端调试，支持页面交互、日志分析、网络监控、**视觉分析**等。

## 前置条件

```bash
mcporter list chrome-devtools
mcporter list analysis-images
```

若未配置，参考 mcporter-setup skill 进行安装。

---

## 使用方式

1. 执行 `mcporter list chrome-devtools` 获取所有可用工具及参数说明
2. 按需调用工具完成调试任务

> **注意**：`take_snapshot` 输出基于 a11y 树，每个元素带 uid，用于后续交互操作。每次页面更新后 uid 会变化，需重新获取快照。

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
