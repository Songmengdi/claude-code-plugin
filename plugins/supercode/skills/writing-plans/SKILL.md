---
name: writing-plans
description: 当你有规范或多步骤任务的需求时,在接触代码之前使用。使用并行架构设计和并行代码审查来创建高质量实施计划。
disable-model-invocation: true
compatibility:
  requires:
    - supercode:code-architect
    - supercode:plan-reviewer
---

# 编写实施计划

通过并行架构设计和并行代码审查，创建高质量的实施计划。

**开始时声明**: "我正在使用 writing-plans 技能来创建实施计划。"

**上下文**: 这应该在当前 feature 分支中运行（由 brainstorming 技能创建）。

## 核心原则

1. **阶段性优先** — 大型设计或设计文档已分阶段的，必须拆分为独立阶段
2. **验收标准明确** — 每个阶段必须有具体的验收标准和测试方式
3. **并行优于串行** — 使用多个 agents 并行探索不同维度
4. **完整任务分解** — 每个步骤应该是 5-15 分钟的动作
5. **质量第一** — 通过并行审查确保计划质量
6. **指挥棒原则** — 计划是指挥棒，让编码变简单，而不是替代编码

## 输入输出

**输入：** `docs/plans/YYYY-MM-DD-<feature-name>-design.md`

**输出：**
- 小型设计：单一计划 `docs/plans/YYYY-MM-DD-<feature-name>-plan.md`
- 中/大型设计：路线图 + 多个阶段性计划

---

## 阶段化工作流程

本技能分为 8 个阶段（1-8），每个阶段的具体指令存储在独立文件中。

**当前你只处于一个阶段。禁止猜测其他阶段该做什么。**

| # | 名称 | 详情 |
|---|------|------|
| 1 | 读取设计文档并评估规模 | `phases/phase-1.md` |
| 2 | 探索现有代码库 | `phases/phase-2.md` |
| 3 | 并行架构设计 | `phases/phase-3.md` |
| 4 | 整合实施蓝图 | `phases/phase-4.md` |
| 5 | 并行计划审查 | `phases/phase-5.md` |
| 6 | 修复关键问题 | `phases/phase-6.md` |
| 7 | 保存实施计划 | `phases/phase-7.md` |
| 8 | 执行交接 | `phases/phase-8.md` |

### 执行规则（强制）

1. **每个阶段的第一步必须是 `Read` 对应的 `phases/phase-N.md`**，未读取前禁止执行任何阶段操作
2. 读取后用 `TodoWrite` 创建该阶段任务清单
3. 阶段完成后标记为 completed，**等待用户确认**后再进入下一阶段
4. 禁止跳过阶段，禁止跨阶段执行
5. 子代理调用必须使用 `Agent` 工具，提供明确的 `description` 和 `prompt`

## 计划文档模板

详细的计划文档模板（头部格式、任务结构等）存储在 `references/` 目录。
