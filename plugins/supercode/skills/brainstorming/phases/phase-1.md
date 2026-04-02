# 阶段 1：并行探索项目上下文

**前提：阶段 0 已完成。**

## 目标

在早期同时获取文档视角与代码视角，避免单一信息源导致的误判。

**重要提醒：此阶段只探索和理解，不要开始设计或编码。**

## 执行方式

使用 `Agent` 工具并行调用 2-3 个 code-explorer 子代理：

```yaml
subagent_type: "supercode:code-explorer"
description: "探索代码结构和模式"
prompt: |
  探索项目代码库：
  - 目标功能：[功能名称]
  - 关注点：[代码结构/实现模式/技术细节/具体方面]
  - 输出：核心文件列表、架构理解、代码模式
```

**关键原则**：
- 子代理相互独立工作，不得假设对方的结论
- 允许结论存在冲突或不一致，留待后续澄清阶段处理

## 任务清单

使用 `TodoWrite` 创建任务：

```markdown
[
  {"content": "启动 code-explorer 子代理 #1", "status": "in_progress", "activeForm": "正在启动 code-explorer 子代理 #1"},
  {"content": "启动 code-explorer 子代理 #2（可选）", "status": "pending", "activeForm": "正在启动 code-explorer 子代理 #2"},
  {"content": "启动 code-explorer 子代理 #3（可选）", "status": "pending", "activeForm": "正在启动 code-explorer 子代理 #3"},
  {"content": "综合子代理输出，提取核心文件列表", "status": "pending", "activeForm": "正在综合子代理输出"}
]
```

## 本阶段输出

- 各子代理的探索报告
- 综合后的核心文件列表
- 对代码架构的初步理解

## 完成条件

所有子代理完成，核心文件列表已确定，用户确认后进入阶段 2。
