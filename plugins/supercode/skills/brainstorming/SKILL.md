---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---

# 将想法转化为设计

## 概述

通过并行探索代码库和自然的协作对话，帮助将想法转化为完整的设计和规范。

**开始时声明:** "我正在使用 brainstorming 技能来探索设计和需求。"

**目标:** 深入理解代码库 + 用户意图 → 完整设计 → 创建 feature 分支 → 文档化设计 → 调用 writing-plans

## 检查清单创建

你必须将以下的步骤加入到你的任务清单中并按顺序完成：

0. **加载功能上下文（新会话）** — 加载现有功能的文档和历史变更
1. **并行探索项目上下文** — 同时启动 docs-explorer agent 与 code-explorer agents
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

**行动：**
- 并行启动：
  - **docs-explorer agent**    - 任务：根据用户需求，阅读 `docs/` 目录中相关文档
    - 输出：项目规则、业务约束、不能修改的区域、关键决策、已有模式
    - 优先阅读：`invariants.md`、`do_not_touch.md`、`first_30_minutes.md`、与需求相关的业务文档
  - **2–3 个 code-explorer agents**    - 任务：探索代码结构、实现模式、技术细节
    - 输出：核心文件列表、架构理解、代码模式
- 两类 agent **相互独立工作**，不得假设对方的结论
- 允许结论存在冲突或不一致，留待后续澄清阶段处理
- **docs-explorer 的约束优先于 code-explorer 的发现**：当文档说"不能做某事"时，即使代码层面可行也必须遵守

### 阶段 2：澄清性问题

- **每次只问一个问题**
- 尽可能优先使用多选题

### 阶段 3：并行架构探索

**目标：** 设计具有不同权衡的多种实施方案

**行动：**
- 并行启动 2-3 个 code-architect agents，每个专注于不同方面：
  - **minimal changes**：最小变更，最大复用现有代码
  - **clean architecture**：可维护性、优雅抽象
  - **pragmatic balance**：速度 + 质量
- 每个 agent 必须考虑文档约束（invariants、do_not_touch 等）

### 阶段 4：呈现设计选择与批准

**行动：**
1. 基于用户选择，展示完整设计
2. 每个章节的长度与其复杂度成比例：如果简单则几句话，如果复杂则 200-300 字
3. 涵盖：架构、组件、数据流、错误处理、测试
4. 在每个章节后询问目前为止是否正确
5. 准备在某个地方不合理时回溯澄清

**HARD GATE：**
在你展示设计并获得用户批准之前，不得调用任何实施技能、编写任何代码、搭建任何项目或采取任何实施行动。

### 阶段 5：创建 Feature 分支

**行动：**
- 在设计批准后，创建新的本地 feature 分支
- 分支命名规范：`feature/<topic>` 或根据项目约定
- 使用 `git checkout -b feature/<topic>` 创建并切换到新分支

### 阶段 6：文档化设计并过渡

**行动：**
- 将验证后的设计写入 `docs/plans/YYYY-MM-DD-<topic>-design.md` 并提交
- 设计文档必须包含 frontmatter：

```markdown
---
tags: [功能标签1, 功能标签2, feature-id]
related:
  - design: docs/plans/YYYY-MM-DD-xxx-v1-design.md  # 如有历史版本
  - plan: docs/plans/YYYY-MM-DD-xxx-v1-plan.md     # 如有历史版本
status: design  # design | implemented | completed
---

# [功能名称] 设计

> **参考:** 此设计将用于生成实施计划（见对应的 plan 文档）

## 概述
[设计内容...]
```

- 提交信息：`docs: add design for <topic>`
- 调用 writing-plans 技能创建详细的实施计划
