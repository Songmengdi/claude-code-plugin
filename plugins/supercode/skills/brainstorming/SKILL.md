---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---

# 将想法转化为设计

## 概述

**核心职责：** 通过并行探索代码库和协作对话，帮助将想法转化为完整的设计文档。

**开始时声明:** "我正在使用 brainstorming 技能来探索设计和需求。"

**目标:** 深入理解代码库 + 用户意图 → 完整设计 → 创建 feature 分支 → 文档化设计 → **调用 writing-plans**

## 职责边界

### ✅ 你应该做的：
- 探索代码库，理解现有架构
- 与用户对话，澄清需求
- 设计架构、组件、数据流
- 产出设计文档（design.md）
- **调用 writing-plans skill** 来创建实施计划

### ❌ 你不应该做的：
- **不要开始编写任何代码**
- **不要自己制定实施计划**（必须调用 writing-plans skill）
- **不要创建具体的任务列表**（这是 writing-plans 的职责）
- **不要实现任何功能**（这是 executing-plans 的职责）
- **不要修改任何文件**（除了设计文档）

### 🔴 HARD GATE（强制约束）：
**在设计获得用户批准之前，你绝对不能：**
1. 调用任何实施技能
2. 编写任何代码
3. 创建任何文件（除了设计文档）
4. 修改任何现有代码
5. 自己制定实施计划

**唯一允许的输出：**
- 设计文档（design.md）
- 调用 writing-plans skill

## 检查清单创建

你必须将以下的步骤通过 `TaskCreate` 加入到你的任务清单中并按顺序完成：

0. **加载功能上下文（新会话）** — 加载现有功能的文档和历史变更
1. **并行探索项目上下文** — 启动code-explorer agents
2. **阅读核心文件** — 综合文档与代码 agent 识别的关键文件
3. **提出澄清性问题** — 每次一个问题，优先多选题
4. **并行架构探索** — 启动 2-3 个 code-architect agents
5. **呈现设计选择与批准** — 每个章节后获得用户批准
6. **创建 feature 分支** — 创建新的本地 feature 分支
7. **文档化设计并过渡** — 保存设计文档，调用 writing-plans

## 过程

### 阶段 0：加载功能上下文（新会话）

**目标：** 在新会话中快速了解现有功能的状态和历史变更

**行动：**

如果用户说明要改的功能或提供文档路径：

**使用 Task 工具调用 feature-context-loader agent：**
```
Task({
  subagent_type: "feature-context-loader",
  prompt: "加载功能上下文：[功能描述或文档路径]"
})
```

**展示 agent 返回的 Markdown Table 格式上下文摘要**，并确认：
- 上下文是否正确？
- 是否需要加载其他功能？
- 这是新功能还是现有功能的变更？

### 阶段 1：并行探索项目上下文

**目标：** 在早期同时获取文档视角与代码视角，避免单一信息源导致的误判

**重要提醒：** 此阶段只探索和理解，**不要开始设计或编码**。

**行动：**
- 并行启动 2–3 个 code-explorer agents
- 任务：探索代码结构、实现模式、技术细节
- 输出：核心文件列表、架构理解、代码模式
- Agents 相互独立工作，不得假设对方的结论
- 允许结论存在冲突或不一致，留待后续澄清阶段处理

### 阶段 2：澄清性问题

**目标：** 通过提问澄清需求和约束

**重要提醒：** 只提问和澄清，**不要开始设计方案或编码**。

**行动：**
- 使用 AskUserQuestion 询问用户问题
- **每次只问一个问题**
- 尽可能优先使用多选题
- 记录用户的回答，用于后续设计

### 阶段 3：架构探索

**目标：** 设计实施方案

**重要提醒：** 探索架构方向，**不要制定具体实施计划或开始编码**。

**行动：**

1. **询问用户架构偏好：**
   - **minimal changes**：最小变更，最大复用现有代码
   - **clean architecture**：可维护性、优雅抽象
   - **pragmatic balance**：速度 + 质量

2. **启动 code-architect agents**（2-3个）：
   - 每个专注于用户选择的架构方向
   - Agent 必须考虑文档约束（invariants、do_not_touch 等）
   - 输出：架构方案、组件设计、技术选型

3. **整合架构方案**：
   - 综合各个 agent 的建议
   - 形成统一的架构方案
   - **不要制定具体任务列表**（这是 writing-plans 的职责）

### 阶段 4：呈现设计选择与批准

**目标：** 向用户展示设计并获得批准

**🔴 关键约束：** 在用户批准设计之前，**绝对不要**：
- 调用 writing-plans
- 创建 feature 分支
- 编写任何代码
- 创建任何文件

**行动：**

1. **展示完整设计**：
   - 每个章节的长度与其复杂度成比例
   - 简单功能：几句话
   - 复杂功能：200-300 字

2. **设计内容应涵盖**：
   - 架构概述
   - 核心组件及其职责
   - 数据流和交互
   - 错误处理策略
   - 测试策略

3. **逐步获得批准**：
   - 在每个章节后询问："这部分设计是否正确？"
   - 准备在某个地方不合理时回溯澄清
   - **只有用户明确批准后才能继续**

4. **最终确认**：
   - 展示完整设计摘要
   - 询问："整体设计是否批准？可以进入实施计划阶段吗？"
   - **只有获得明确的"批准"或"可以"后，才能进入阶段 5**

### 阶段 5：创建 Feature 分支

**前置条件：** 用户已明确批准设计。

**目标：** 使用`AskUserQuestion` 询问用户,是否创建独立分支

**行动：**
1. 创建新的本地 feature 分支：
   ```bash
   git checkout -b feature/<topic>
   ```
2. 分支命名规范：`feature/<topic>` 或根据项目约定
3. **不要在此分支上编写任何代码**（只创建分支）

### 阶段 6：文档化设计并过渡到 writing-plans

**前置条件：** 
- 用户已批准设计
- feature 分支已创建

**目标：** 保存设计文档，然后**必须调用 writing-plans skill**

**行动：**

1. **创建设计文档** `docs/plans/YYYY-MM-DD-<topic>-design.md`：

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

2. **提交设计文档**：
   ```bash
   git add docs/plans/YYYY-MM-DD-<topic>-design.md
   git commit -m "docs: 添加 <topic> 设计文档"
   ```

3. **🔴 必须调用 writing-plans skill**：
   
   **完成设计后，你必须明确告知用户：**
   
   ```
   设计文档已保存到 docs/plans/YYYY-MM-DD-<topic>-design.md。
   
   接下来需要创建实施计划。请使用以下命令：
   
   /supercode:writing-plans docs/plans/YYYY-MM-DD-<topic>-design.md
   ```
   
   **注意：**
   - **不要自己开始制定实施计划**
   - **不要开始编写任何代码**
   - **必须由用户调用 writing-plans skill**
   - brainstorming skill 的职责到此结束

## 常见错误及纠正

### ❌ 错误：自己开始编写代码
**正确做法：** 只输出设计文档，然后调用 writing-plans

### ❌ 错误：自己制定任务列表
**正确做法：** 任务列表由 writing-plans skill 创建，不是 brainstorming 的职责

### ❌ 错误：在设计未批准前创建分支或文件
**正确做法：** 必须等待用户明确批准设计后才能创建分支

### ❌ 错误：跳过用户批准环节
**正确做法：** 每个设计章节都要询问用户是否正确，整体设计要获得明确批准

## 关键原则

- **探索优先**：先理解代码库和需求，再设计
- **用户驱动**：每个设计决策都要与用户确认
- **边界清晰**：只做设计，不做实施
- **强制过渡**：必须调用 writing-plans，不能自己制定计划
- **文档化**：所有设计决策都要记录在设计文档中
