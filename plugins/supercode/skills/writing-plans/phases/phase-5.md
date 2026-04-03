# 阶段 5：计划审查

**前提：阶段 4 已完成。**

## 目标

确保计划完整覆盖设计要求，验证一致性和可执行性。

## 执行方式

### 启动 plan-reviewer 子代理

并行启动 2-3 个 plan-reviewer 子代理，提供不同的审查重点：

```yaml
subagent_type: "supercode:plan-reviewer"
description: "审查设计覆盖度"
prompt: |
  审查实施计划的设计覆盖度：
  - 计划文档：[计划路径]
  - 设计文档：[设计路径]

  请审查计划是否完整覆盖了设计中的所有功能、组件和约束。
  只报告高置信度问题（置信度 ≥ 80）。
```

```yaml
subagent_type: "supercode:plan-reviewer"
description: "审查任务质量"
prompt: |
  审查实施计划的任务质量：
  - 计划文档：[计划路径]
  - 设计文档：[设计路径]

  请审查：
  1. 任务划分合理性、可执行性、验收标准是否明确
  2. 每个任务是否包含必要的参考链接（文档、代码片段）
  3. 类型定义是否明确给出或有明确的查找位置
  4. 是否有足够的信息防止 AI 猜测

  只报告高置信度问题（置信度 ≥ 80）。
```

```yaml
subagent_type: "supercode:plan-reviewer"
description: "审查完整性"
prompt: |
  审查实施计划的完整性：
  - 计划文档：[计划路径]
  - 设计文档：[设计路径]

  请审查是否有遗漏的功能点、缺失的边界情况。
  只报告高置信度问题（置信度 ≥ 80）。
```

### 中/大型设计

对于阶段性计划，每个阶段独立审查上述内容。

## 任务清单

```markdown
[
  {"content": "启动 plan-reviewer #1", "status": "in_progress", "activeForm": "正在启动 plan-reviewer #1"},
  {"content": "启动 plan-reviewer #2", "status": "pending", "activeForm": "正在启动 plan-reviewer #2"},
  {"content": "启动 plan-reviewer #3（可选）", "status": "pending", "activeForm": "正在启动 plan-reviewer #3"}
]
```

## 本阶段输出

- 审查报告
- 高置信度问题列表

## 完成条件

所有子代理完成，**停止并等待用户回应**。
