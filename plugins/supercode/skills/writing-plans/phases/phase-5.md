# 阶段 5：并行计划审查

**前提：阶段 4 已完成。**

## 目标

确保计划完整覆盖设计要求，验证一致性、文件定位准确性和测试完整性。

## 执行方式

### 小型设计：审查单一计划

并行启动 4 个 plan-reviewer 子代理，每个提供不同的审查重点：

```yaml
subagent_type: "supercode:plan-reviewer"
description: "审查设计覆盖度"
prompt: |
  审查实施计划的设计覆盖度：
  - 计划文档：docs/plans/YYYY-MM-DD-<feature-name>-plan.md
  - 设计文档：docs/plans/YYYY-MM-DD-<feature-name>-design.md

  请读取这两个文档，审查计划是否完整覆盖了设计中的所有功能、组件和约束。
  只报告高置信度问题（置信度 ≥ 80）。
```

```yaml
subagent_type: "supercode:plan-reviewer"
description: "审查一致性和质量"
prompt: |
  审查实施计划的一致性和质量：
  - 计划文档：docs/plans/YYYY-MM-DD-<feature-name>-plan.md
  - 设计文档：docs/plans/YYYY-MM-DD-<feature-name>-design.md

  审查计划与设计的一致性、任务划分合理性、可执行性。
  只报告高置信度问题（置信度 ≥ 80）。
```

```yaml
subagent_type: "supercode:plan-reviewer"
description: "审查完整性和遗漏"
prompt: |
  审查实施计划的完整性和遗漏：
  - 计划文档：docs/plans/YYYY-MM-DD-<feature-name>-plan.md
  - 设计文档：docs/plans/YYYY-MM-DD-<feature-name>-design.md

  审查是否有遗漏的功能点、缺失的边界情况、未考虑的错误处理。
  只报告高置信度问题（置信度 ≥ 80）。
```

```yaml
subagent_type: "supercode:plan-reviewer"
description: "审查文件定位和测试"
prompt: |
  审查实施计划的文件定位和测试：
  - 计划文档：docs/plans/YYYY-MM-DD-<feature-name>-plan.md

  审查文件路径是否准确、修改位置是否明确、测试方式是否完整。
  只报告高置信度问题（置信度 ≥ 80）。
```

### 中/大型设计：审查阶段性计划

**首先审查路线图**（1 个子代理）：
- 审查阶段划分是否合理
- 审查每个阶段的验收标准是否明确
- 审查阶段之间的依赖关系是否正确

**然后分阶段审查每个计划**（每个阶段 3 个子代理）：
- **agent 1**：审查该阶段是否完整覆盖了设计中的相关部分
- **agent 2**：审查该阶段的验收标准是否可执行、测试是否充分
- **agent 3**：审查文件路径是否准确、修改位置是否明确

## 任务清单

```markdown
[
  {"content": "启动 plan-reviewer #1", "status": "in_progress", "activeForm": "正在启动 plan-reviewer #1"},
  {"content": "启动 plan-reviewer #2", "status": "pending", "activeForm": "正在启动 plan-reviewer #2"},
  {"content": "启动 plan-reviewer #3", "status": "pending", "activeForm": "正在启动 plan-reviewer #3"},
  {"content": "启动 plan-reviewer #4", "status": "pending", "activeForm": "正在启动 plan-reviewer #4"}
]
```

## 要求子代理

- 从 prompt 中获取文档路径，读取文档内容
- 只报告高置信度问题（置信度 ≥ 80）
- 重点关注设计覆盖度、一致性和可执行性
- 提供具体的修复建议

## 本阶段输出

- 各子代理的审查报告
- 高置信度问题列表

## 完成条件

所有子代理完成，用户确认后进入阶段 6。
