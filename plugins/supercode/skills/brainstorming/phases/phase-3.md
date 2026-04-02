# 阶段 3：架构探索

**前提：阶段 2 已完成。**

## 目标

设计实施方案。

**重要提醒：探索架构方向，不要制定具体实施计划或开始编码。**

## 执行方式

### 1. 询问用户架构偏好

使用 `AskUserQuestion` 选择架构方向：

- **minimal changes**：最小变更，最大复用现有代码
- **clean architecture**：可维护性、优雅抽象
- **pragmatic balance**：速度 + 质量

### 2. 启动 code-architect 子代理

使用 `Agent` 工具并行调用 2-3 个 code-architect 子代理：

```yaml
subagent_type: "supercode:code-architect"
description: "设计架构方案"
prompt: |
  设计功能架构：
  - 功能名称：[功能名称]
  - 需求：[澄清后的需求]
  - 架构方向：[用户选择的方向]
  - 约束：[文档约束，如 invariants、do_not_touch 等]
  - 输出：架构方案、组件设计、技术选型
```

**关键原则**：
- 每个子代理必须考虑文档约束（invariants、do_not_touch 等）
- 子代理专注于用户选择的架构方向

### 3. 整合架构方案

- 综合各个子代理的建议
- 形成统一的架构方案
- **不要制定具体任务列表**（这是 writing-plans 的职责）

## 任务清单

```markdown
[
  {"content": "询问用户架构偏好", "status": "in_progress", "activeForm": "正在询问用户架构偏好"},
  {"content": "启动 code-architect 子代理 #1", "status": "pending", "activeForm": "正在启动 code-architect 子代理 #1"},
  {"content": "启动 code-architect 子代理 #2", "status": "pending", "activeForm": "正在启动 code-architect 子代理 #2"},
  {"content": "整合架构方案", "status": "pending", "activeForm": "正在整合架构方案"}
]
```

## 本阶段输出

- 统一的架构方案
- 组件设计
- 技术选型建议

## 完成条件

架构方案已整合，用户确认后进入阶段 4。
