---
name: writing-plans
description: 当你有规范或多步骤任务的需求时,在接触代码之前使用。使用并行架构设计和并行代码审查来创建高质量实施计划。
---

# 编写实施计划

## 概述

编写全面的实施计划，通过并行架构设计和并行代码审查，确保计划的质量和可执行性。

**开始时声明:** "我正在使用 writing-plans 技能来创建实施计划。"

**上下文:** 这应该在当前 feature 分支中运行（由 brainstorming 技能创建）。

**计划保存位置:** `docs/plans/YYYY-MM-DD-<feature-name>-plan.md`

**设计文档:** 从 `docs/plans/YYYY-MM-DD-<feature-name>-design.md` 读取已批准的设计

## 检查清单创建

你必须将以下的步骤加入到你的任务清单中并按顺序完成：

1. **读取设计文档** — 理解已批准的设计
2. **并行架构设计** — 启动 2-3 个 supercode:code-architect agents，提供详细实施蓝图
3. **整合实施蓝图** — 选择最佳方案，创建详细的任务分解
4. **并行代码审查计划** — 启动 3 个 supercode:code-reviewer agents，从不同维度审查计划
5. **修复关键问题** — 修复高置信度问题
6. **保存实施计划** — 保存到 `docs/plans/YYYY-MM-DD-<feature-name>-plan.md`
7. **提供执行选项** — 1. 审查计划  2. 直接执行

## 流程图

```dot
digraph writing-plans {
    "Read approved design doc" [shape=box];
    "Parallel architecture design with code-architect agents" [shape=box];
    "Integrate implementation blueprint" [shape=box];
    "Parallel code review of plan with code-reviewer agents" [shape=box];
    "Fix critical issues" [shape=diamond];
    "Save implementation plan" [shape=doublecircle];
    "Provide execution options" [shape=doublecircle];

    "Read approved design doc" -> "Parallel architecture design with code-architect agents";
    "Parallel architecture design with code-architect agents" -> "Integrate implementation blueprint";
    "Integrate implementation blueprint" -> "Parallel code review of plan with code-reviewer agents";
    "Parallel code review of plan with code-reviewer agents" -> "Fix critical issues";
    "Fix critical issues" -> "Save implementation plan" [label="fixed"];
    "Fix critical issues" -> "Integrate implementation blueprint" [label="major revisions"];
    "Save implementation plan" -> "Provide execution options";
}
```

## 过程

### 阶段 1：读取设计文档

**目标：** 理解已批准的设计

**行动：**
- 从 `docs/plans/YYYY-MM-DD-<feature-name>-design.md` 读取设计文档
- 理解架构、组件、数据流、约束、成功标准

### 阶段 2：并行架构设计

**目标：** 创建详细的实施蓝图

**并行启动 2-3 个 supercode:code-architect agents**，每个专注于不同方面：
- **minimal implementation**：最小改动，最快实现
- **clean implementation**：代码质量、可维护性、测试完整性
- **pragmatic balance**：速度 + 质量的平衡

**向每个 code-architect agent 提供设计文档的完整内容**，要求：
- 基于设计文档，创建详细的实施蓝图
- 指定每个要创建或修改的文件、组件职责、集成点和数据流
- 将实现分解为清晰的阶段，每个阶段包含具体任务
- 做出坚定的架构选择，而不是呈现多个选项
- 提供具体文件路径、函数名称和步骤

### 阶段 3：整合实施蓝图

**目标：** 选择最佳方案，创建详细的任务分解

**行动：**
1. 审查所有 code-architect agents 的实施蓝图
2. 针对此特定任务形成你认为最合适的观点
3. 创建详细的任务分解：

#### 计划文档头部

**每个计划必须以这个头部开始：**

```markdown
---
tags: [功能标签1, 功能标签2, feature-id]
related:
  - design: docs/plans/YYYY-MM-DD-<feature-name>-design.md
  - plan: docs/plans/YYYY-MM-DD-xxx-v1-plan.md  # 如有历史版本
status: plan  # plan | executed | completed
---

# [功能名称] 实施计划

> **给 Claude:** 必需子技能:使用 superpowers:executing-plans 逐任务实施此计划。

**目标:** [一句话描述这个计划构建什么]

**架构:** [2-3句话描述方法]

**技术栈:** [关键技术/库]

**参考设计:** docs/plans/YYYY-MM-DD-<feature-name>-design.md

---
```

#### 任务结构

**每个步骤是一个动作（2-5 分钟）：**

````markdown
### 任务 N: [组件名称]

**文件:**
- 创建: `exact/path/to/file.py`
- 修改: `exact/path/to/existing.py:123-145`
- 测试: `tests/exact/path/to/test.py`

**步骤 1: 编写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**步骤 2: 运行测试以验证它失败**

运行: `pytest tests/path/test.py::test_name -v`
预期: FAIL,显示 "function not defined"

**步骤 3: 编写最小实现**

```python
def function(input):
    return expected
```

**步骤 4: 运行测试以验证它通过**

运行: `pytest tests/path/test.py::test_name -v`
预期: PASS

**步骤 5: 提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

### 阶段 4：并行代码审查计划

**目标：** 从不同维度审查计划质量

**并行启动 3 个 code-reviewer agents** 专注于不同方面：
- **implementation feasibility**：实施的可行性、完整性、可执行性
- **code quality & patterns**：代码质量、遵循项目约定、测试完整性
- **architecture & design**：架构一致性、设计模式、可维护性

**向每个 code-reviewer agent 提供实施计划的完整内容**，要求：
- 审查实施计划的各个方面
- 识别可能的问题、遗漏、不合理的设计
- 只报告高置信度问题（置信度 ≥ 80）
- 提供具体的修复建议

### 阶段 5：修复关键问题

**目标：** 提高计划质量

**行动：**
1. 整合所有 code-reviewer agents 的发现
2. 识别高置信度问题
3. 修复这些问题
4. 如果发现重大问题，可能需要回到阶段 2 重新设计
5. 反复审查直到没有高置信度问题

### 阶段 6：保存实施计划

**目标：** 保存最终计划

**行动：**
- 保存最终计划到 `docs/plans/YYYY-MM-DD-<feature-name>-plan.md`
- 确保计划完整、准确、可执行

## 执行交接

保存计划后，提供执行选择：

```
计划完成并保存到 `docs/plans/YYYY-MM-DD-<topic>-plan.md`。

你应该结束本次会话，开启新的会话，并复制以下命令到新的会话窗口：

/executing-plans docs/plans/YYYY-MM-DD-<topic>-plan.md
```

## 关键原则

- **并行优于串行** — 使用多个 agents 并行探索不同维度
- **完整任务分解** — 每个步骤应该是 2-5 分钟的动作
- **精确文件路径** — 始终使用精确的文件路径
- **完整代码** — 计划中包含完整代码（而不是"添加验证"）
- **精确命令** — 包含精确的命令和预期输出
- **DRY, YAGNI, TDD** — 遵循核心原则
- **频繁提交** — 鼓励频繁提交
- **质量第一** — 通过并行审查确保计划质量
