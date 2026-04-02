# 阶段 5：文档化设计并过渡

**前提：阶段 4 已完成，用户已批准设计。**

## 目标

保存设计文档，然后告知用户调用 writing-plans skill。

## 执行方式

### 1. 创建设计文档

路径：`docs/plans/YYYY-MM-DD-<topic>-design.md`

```markdown
---
tags: [功能标签1, 功能标签2, feature-id]
related:
  - design: docs/plans/YYYY-MM-DD-xxx-v1-design.md  # 如有历史版本
  - plan: docs/plans/YYYY-MM-DD-xxx-v1-plan.md     # 如有历史版本
status: design  # design | executed | completed
---

# [功能名称] 设计

> **参考:** 此设计将用于生成实施计划（见对应的 plan 文档）

## 概述
[设计内容...]

## 架构
[架构设计...]

## 组件
[组件设计...]

## 数据流
[数据流设计...]

## 错误处理
[错误处理策略...]

## 测试策略
[测试策略...]
```

### 2. 设计文档已保存

设计文档已保存到 `docs/plans/YYYY-MM-DD-<topic>-design.md`。

完成设计后，你必须明确告知用户：

```
设计文档已保存到 docs/plans/YYYY-MM-DD-<topic>-design.md。

接下来需要创建实施计划。请使用以下命令：

/writing-plans docs/plans/YYYY-MM-DD-<topic>-design.md
```

## 注意事项

- **不要自己开始制定实施计划**
- **不要开始编写任何代码**
- **必须由用户调用 writing-plans skill**
- brainstorming skill 的职责到此结束

## 本阶段输出

- 保存的设计文档
- 用户的确认

## 完成条件

设计文档已保存并提交，用户已知晓下一步操作。
