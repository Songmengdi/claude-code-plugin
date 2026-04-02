---
name: brainstorming
description: 当需要设计复杂、多步骤的功能时使用。覆盖架构设计、组件规划、需求澄清，在实施前完成完整的设计探索。
disable-model-invocation: true
compatibility:
  requires:
    - supercode:feature-context-loader
    - supercode:code-explorer
    - supercode:code-architect
---

# 将想法转化为设计

通过并行探索代码库和协作对话，将想法转化为完整的设计文档。

**开始时声明**: "我正在使用 brainstorming 技能来探索设计和需求。"

## 核心原则

1. **探索优先** — 先理解代码库和需求，再设计
2. **用户驱动** — 每个设计决策都要与用户确认
3. **边界清晰** — 只做设计，不做实施
4. **告知过渡** — 设计完成后告知用户调用 writing-plans

## 职责边界

### ✅ 你应该做的

- 探索代码库，理解现有架构
- 与用户对话，澄清需求
- 设计架构、组件、数据流
- 产出设计文档（design.md）

### ❌ 你不应该做的

- **不要开始编写任何代码**
- **不要自己制定实施计划**（这是 writing-plans 的职责）
- **不要创建具体的任务列表**
- **不要实现任何功能**
- **不要修改任何文件**（除了设计文档）

---

## 阶段化工作流程

本技能分为 6 个阶段（0-5），每个阶段的具体指令存储在独立文件中。

**当前你只处于一个阶段。禁止猜测其他阶段该做什么。**

| # | 名称 | 详情 |
|---|------|------|
| 0 | 加载功能上下文 | `phases/phase-0.md` |
| 1 | 并行探索项目上下文 | `phases/phase-1.md` |
| 2 | 阅读核心文件并澄清问题 | `phases/phase-2.md` |
| 3 | 架构探索 | `phases/phase-3.md` |
| 4 | 呈现设计选择与批准 | `phases/phase-4.md` |
| 5 | 文档化设计并过渡 | `phases/phase-5.md` |

### 执行规则（强制）

1. **每个阶段的第一步必须是 `Read` 对应的 `phases/phase-N.md`**，未读取前禁止执行任何阶段操作
2. 读取后用 `TodoWrite` 创建该阶段任务清单
3. 阶段完成后标记为 completed，**停止并等待用户回应后再进入下一阶段**
4. 禁止跳过阶段 0，禁止跨阶段执行
5. 子代理调用必须提供明确的任务描述（description 和 prompt）
