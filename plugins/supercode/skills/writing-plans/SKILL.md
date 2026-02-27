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

**向每个 agent 提供设计文档路径**：`docs/plans/YYYY-MM-DD-<feature-name>-design.md`

让 agent 自己读取设计文档内容，要求：
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

**每个任务是一个完整的、不破坏代码的最小功能变更（5-15 分钟）：**

**动作设计原则：**
1. **完整性**：一个动作包含实现某个最小功能所需的所有变更（类型声明、函数实现、测试等），是一个完整的单元
2. **原子性**：每个动作实现后代码处于可工作状态，不破坏现有功能
3. **最小变更**：一个动作对应一个最小的功能点或前置准备，不要过度拆分
4. **多文件支持**：一个动作可能涉及多个文件的修改

````markdown
### 任务 N: [最小功能描述，如：添加用户认证功能]

**变更文件：**
- 创建: `src/auth/user-auth.ts`
- 创建: `tests/auth/user-auth.test.ts`
- 修改: `src/api/router.ts:45-52`  # 集成认证路由

**实现：**

类型定义 (`src/auth/user-auth.ts`):
```typescript
export interface UserCredentials {
  username: string;
  password: string;
}

export interface AuthResult {
  success: boolean;
  token?: string;
  error?: string;
}
```

认证函数 (`src/auth/user-auth.ts`):
```typescript
export async function authenticateUser(
  credentials: UserCredentials
): Promise<AuthResult> {
  if (!credentials.username || !credentials.password) {
    return { success: false, error: 'Invalid credentials' };
  }
  // TODO: 实际验证逻辑
  return { success: true, token: 'mock-token' };
}
```

路由集成 (`src/api/router.ts:45-52`):
```typescript
import { authenticateUser, UserCredentials } from '../auth/user-auth';

router.post('/auth/login', async (ctx) => {
  const credentials: UserCredentials = ctx.request.body;
  const result = await authenticateUser(credentials);
  ctx.body = result;
});
```

测试 (`tests/auth/user-auth.test.ts`):
```typescript
import { authenticateUser } from '../../src/auth/user-auth';

test('valid credentials return success', async () => {
  const result = await authenticateUser({
    username: 'test',
    password: 'password'
  });
  expect(result.success).toBe(true);
});
```

**验证：**
运行: `pnpm test tests/auth/user-auth.test.ts`
预期: PASS

**提交：**
```bash
git add src/auth/user-auth.ts src/api/router.ts tests/auth/user-auth.test.ts
git commit -m "feat: add user authentication with username/password"
```
````

**示例：正确的动作划分**

✅ **正确的动作**（一个任务内）：
- 添加完整的用户认证功能（类型 + 实现 + 路由集成 + 测试）
- 重构函数签名并更新所有调用点（类型声明 + 所有调用处修改）
- 添加缓存层并集成到现有服务（缓存实现 + 服务修改 + 测试）

❌ **错误的拆分**（不要这样分多个任务）：
- 任务1：添加类型定义
- 任务2：添加函数实现
- 任务3：编写测试
- 任务4：集成到路由
- 任务5：运行测试

**注意：** 对于简单的小变更，保持为单个任务；只有当变更确实独立且可分割时才拆分为多个任务。

### 阶段 4：并行代码审查计划

**目标：** 从不同维度审查计划质量

**并行启动 3 个 code-reviewer agents**，每个提供不同的审查重点：
- **agent 1 (implementation feasibility)**：审查实施的可行性、完整性、可执行性
- **agent 2 (code quality & patterns)**：审查代码质量、遵循项目约定、测试完整性
- **agent 3 (architecture & design)**：审查架构一致性、设计模式、可维护性

**向每个 agent 提供计划文档路径**：`docs/plans/YYYY-MM-DD-<feature-name>-plan.md`

让 agent 自己读取文档内容并进行审查，要求：
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
