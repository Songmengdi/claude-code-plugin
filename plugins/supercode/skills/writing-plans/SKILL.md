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

1. **读取设计文档并评估规模** — 理解设计，判断是小型/中型/大型，**检查设计是否已分阶段**
2. **探索现有代码库** — 识别需要修改的现有文件，理解现有代码结构
3. **并行架构设计** — 启动 2 个 supercode:code-architect agents，提供详细实施蓝图（考虑阶段性）
4. **整合实施蓝图** — 根据规模或设计文档的阶段划分创建单一计划或阶段性计划
5. **并行计划审查** — 启动 plan-reviewer agents，验证设计覆盖度、一致性、文件定位准确性和测试完整性
6. **修复关键问题** — 修复高置信度问题
7. **保存实施计划** — 保存计划文件（及路线图和阶段性计划）

## 过程

### 阶段 1：读取设计文档并评估规模

**目标：** 理解已批准的设计，评估实施复杂度

**行动：**
- 从 `docs/plans/YYYY-MM-DD-<feature-name>-design.md` 读取设计文档
- 理解架构、组件、数据流、约束、成功标准
- **检查设计文档是否已经分阶段**：
  - 如果设计文档中已经明确划分了 phases/stages，**必须**按照设计的阶段划分创建对应的阶段性计划
  - 如果设计文档未分阶段，则根据以下标准评估规模：
    - **小型设计**：涉及 ≤5 个核心任务，可在一个会话中完成
    - **中型设计**：涉及 6-10 个核心任务，建议拆分为 2-3 个阶段
    - **大型设计**：涉及 >10 个核心任务，必须拆分为多个独立阶段
- **探索现有代码库**：
  - 识别需要修改的现有文件
  - 理解现有代码结构和模式
  - 确定新文件的放置位置

**规模判断标准：**
- 功能点数量和复杂度
- 涉及的文件和组件数量
- 是否有明确的功能边界可以划分
- 每个阶段是否能独立测试和验证
- **设计文档中是否已经分阶段（优先级最高）**

### 阶段 2：探索现有代码库

**目标：** 理解现有代码结构，识别需要修改的文件

**行动：**
- 使用 Glob 和 Grep 工具搜索相关文件和代码
- 识别需要修改的现有文件
- 理解现有代码结构和模式
- 确定新文件的放置位置
- 记录现有代码中的关键函数、类和模块

**输出：**
- 需要修改的文件列表
- 现有代码结构说明
- 关键代码位置（函数、类、模块）

### 阶段 3：并行架构设计

**目标：** 创建详细的实施蓝图（考虑阶段性）

**并行启动 2 个 supercode:code-architect agents**，每个专注于不同方面：
- **clean implementation**：代码质量、可维护性、测试完整性
- **pragmatic balance**：速度 + 质量的平衡

**向每个 agent 提供设计文档路径和规模评估结果**

让 agent 自己读取设计文档内容，要求：
- **如果设计规模为中/大型，或设计文档已分阶段**：将实施划分为 2-5 个独立阶段，每个阶段：
  - 包含 3-6 个相关任务
  - 有明确的验收标准和交付物
  - 可独立测试和验证
  - 完成后能提供增量价值
- 基于设计文档，为每个阶段创建详细的实施蓝图
- **每个任务必须明确**：
  - 所有要创建或修改的文件（完整路径）
  - 每个文件的修改类型（创建/修改/删除）
  - 修改的具体位置（函数名、类名或行号范围）
  - 实现要点：要做什么、核心思路、关键接口
  - 测试方式：单元测试、集成测试或用户协助验证
- 做出坚定的架构选择，而不是呈现多个选项
- 提供具体文件路径、函数名称和步骤

### 阶段 4：整合实施蓝图

**目标：** 选择最佳方案，创建详细的任务分解

**行动：**
1. 审查所有 code-architect agents 的实施蓝图
2. 针对此特定任务形成你认为最合适的观点
3. **根据设计规模创建计划**：
   - **如果设计文档已经分阶段**：必须按照设计文档的阶段划分创建对应的阶段性计划
   - **如果设计文档未分阶段**：根据评估的规模创建单一计划或阶段性计划

#### 小型设计：创建单一计划

如果设计规模为小型，创建一个完整的计划文档：
- 文件名：`docs/plans/YYYY-MM-DD-<feature-name>-plan.md`
- 包含所有任务（≤5 个）

#### 中/大型设计：创建阶段性计划

如果设计规模为中/大型，**必须拆分为多个阶段性计划**：

**阶段划分原则：**
1. **功能独立性**：每个阶段实现一个相对独立的功能模块或子系统能力
2. **可验证性**：每个阶段完成后可通过自动化测试或用户验证
3. **增量价值**：每个阶段都能交付可用的功能增量
4. **合理粒度**：每个阶段 3-6 个任务，能在 1-2 小时内完成

**阶段性计划命名：**
- 阶段1：`docs/plans/YYYY-MM-DD-<feature-name>-phase1-plan.md`
- 阶段2：`docs/plans/YYYY-MM-DD-<feature-name>-phase2-plan.md`
- 阶段3：`docs/plans/YYYY-MM-DD-<feature-name>-phase3-plan.md`

**阶段性计划索引：**
创建索引文件 `docs/plans/YYYY-MM-DD-<feature-name>-roadmap.md`，记录所有阶段：

```markdown
---
tags: [功能标签1, 功能标签2, feature-id]
related:
  - design: docs/plans/YYYY-MM-DD-<feature-name>-design.md
status: planning  # planning | in-progress | completed
---

# [功能名称] 实施路线图

> **给 Claude:** 这是一个分阶段的大型功能，请按顺序执行各阶段计划。

**设计文档:** docs/plans/YYYY-MM-DD-<feature-name>-design.md

**总览:** [简要描述整体目标和架构]

---

## 阶段划分

### 阶段 1: [阶段名称]
- **计划:** docs/plans/YYYY-MM-DD-<feature-name>-phase1-plan.md
- **目标:** [这个阶段构建什么]
- **验收标准:** [如何验证这个阶段完成]
- **状态:** [pending | in-progress | completed]

### 阶段 2: [阶段名称]
- **计划:** docs/plans/YYYY-MM-DD-<feature-name>-phase2-plan.md
- **目标:** [这个阶段构建什么]
- **验收标准:** [如何验证这个阶段完成]
- **前置依赖:** 阶段1完成
- **状态:** [pending | in-progress | completed]

### 阶段 3: [阶段名称]
...

---

## 执行指南

1. 按顺序执行每个阶段的计划
2. 每个阶段完成后运行验收测试
3. 只有当前阶段通过验收后，才进入下一阶段
4. 使用 `/supercode:executing-plans <phase-plan-path>` 执行各阶段
```

**现在开始创建具体计划文档：**

#### 计划文档头部

**每个计划必须以这个头部开始：**

**小型设计（单一计划）：**

```markdown
---
tags: [功能标签1, 功能标签2, feature-id]
related:
  - design: docs/plans/YYYY-MM-DD-<feature-name>-design.md
status: plan  # plan | executed | completed
---

# [功能名称] 实施计划

> **给 Claude:** 必需子技能:使用 supercode:executing-plans 逐任务实施此计划。

**目标:** [一句话描述这个计划构建什么]

**架构:** [2-3句话描述方法]

**技术栈:** [关键技术/库]

**参考设计:** docs/plans/YYYY-MM-DD-<feature-name>-design.md

**验收标准:**
- [ ] **单元测试通过**: `[具体的测试命令]` — 预期结果
- [ ] **集成测试通过**: `[具体的测试命令]` — 预期结果
- [ ] **用户协助验证**: [详细验证步骤]
- [ ] [其他具体的验证方式]

---
```

**中/大型设计（阶段性计划）：**

```markdown
---
tags: [功能标签1, 功能标签2, feature-id]
related:
  - design: docs/plans/YYYY-MM-DD-<feature-name>-design.md
  - roadmap: docs/plans/YYYY-MM-DD-<feature-name>-roadmap.md
  - prev_phase: docs/plans/YYYY-MM-DD-<feature-name>-phase(N-1)-plan.md  # 如有前一阶段
  - next_phase: docs/plans/YYYY-MM-DD-<feature-name>-phase(N+1)-plan.md  # 如有后一阶段
phase: N  # 阶段编号
status: plan  # plan | executed | completed
---

# [功能名称] 实施计划 - 阶段 N: [阶段名称]

> **给 Claude:** 必需子技能:使用 supercode:executing-plans 逐任务实施此计划。

**阶段目标:** [一句话描述这个阶段构建什么]

**架构:** [2-3句话描述这个阶段的方法]

**技术栈:** [关键技术/库]

**参考设计:** docs/plans/YYYY-MM-DD-<feature-name>-design.md

**验收标准:**
- [ ] **单元测试通过**: `[具体的测试命令]` — 预期结果
- [ ] **集成测试通过**: `[具体的测试命令]` — 预期结果
- [ ] **用户协助验证**: [详细验证步骤]
- [ ] [性能或质量指标]

**前置条件:** [如果需要前一阶段完成，说明需要什么]

---
```

#### 任务结构

**每个任务是一个完整的、不破坏代码的最小功能变更（5-15 分钟）：**

**动作设计原则：**
1. **完整性**：一个动作包含实现某个最小功能所需的所有变更（类型声明、函数实现、测试等），是一个完整的单元
2. **原子性**：每个动作实现后代码处于可工作状态，不破坏现有功能
3. **最小变更**：一个动作对应一个最小的功能点或前置准备，不要过度拆分
4. **多文件支持**：一个动作可能涉及多个文件的修改
5. **测试明确**：每个任务必须包含明确的测试方式和验证步骤
6. **指挥棒原则**：描述要做什么、怎么做，而不是写完整代码

**每个任务必须包含以下部分：**

**1. 变更文件清单**（必须）
- 列出所有需要修改的文件，使用完整路径
- 明确每个文件的修改类型：`创建` | `修改` | `删除`
- 对于修改的文件，说明修改位置（函数名、类名或行号范围）
- 说明每个文件的作用和修改原因

**2. 实现要点**（必须）
- 描述要实现什么功能，而不是写完整代码
- 提供关键的接口定义、类型声明或函数签名
- 说明修改的核心思路和要点
- 列出需要引入的依赖或模块
- 对于复杂逻辑，提供伪代码或流程说明

**3. 测试方式**（必须）
- 明确测试类型：单元测试 | 集成测试 | 用户协助验证
- 提供具体的测试命令
- 描述验证步骤和预期结果
- 如果需要用户协助验证，详细描述验证步骤

**4. 提交信息**（必须）
- 提供明确的 git commit 命令
- commit message 遵循约定式提交规范

**任务模板：**

````markdown
### 任务 N: [最小功能描述，如：添加用户认证功能]

**变更文件：**
- 创建: `src/auth/user-auth.ts` — 用户认证核心逻辑
- 创建: `tests/auth/user-auth.test.ts` — 单元测试
- 修改: `src/api/router.ts:45-52` (函数: setupAuthRoutes) — 集成认证路由
  - 修改原因: 添加认证端点
  - 修改内容: 在路由配置中添加 /auth/login 端点

**实现要点：**

**文件 1: src/auth/user-auth.ts** (新文件)
- 创建用户认证模块，导出以下接口和函数：
  - `UserCredentials` 接口：包含 username 和 password
  - `AuthResult` 接口：包含 success、token、error 字段
  - `authenticateUser(credentials)` 异步函数：
    - 验证 credentials 是否为空
    - 返回 AuthResult 对象
    - 暂时返回 mock token，后续实现真实验证

**文件 2: src/api/router.ts** (修改)
- 修改位置: 第 45-52 行，setupAuthRoutes 函数内
- 实现要点:
  - 导入 authenticateUser 和相关类型
  - 添加 POST /auth/login 路由
  - 从 request.body 获取 credentials
  - 调用 authenticateUser 并返回结果

**文件 3: tests/auth/user-auth.test.ts** (新文件)
- 测试用例:
  - 有效凭证返回成功和 token
  - 空凭证返回错误信息
- 使用 jest 测试框架

**测试：**

**单元测试:**
```bash
pnpm test tests/auth/user-auth.test.ts
```
预期输出: 
```
PASS tests/auth/user-auth.test.ts
  authenticateUser
    ✓ valid credentials return success
    ✓ empty credentials return error
```

**集成测试:**
```bash
pnpm test tests/api/auth.integration.test.ts
```
预期: 认证端点返回正确的 token

**用户协助验证:**
1. 启动服务: `pnpm dev`
2. 发送测试请求: `curl -X POST http://localhost:3000/auth/login -d '{"username":"test","password":"test"}'`
3. 验证返回的 token

**提交：**
```bash
git add src/auth/user-auth.ts src/api/router.ts tests/auth/user-auth.test.ts
git commit -m "feat(auth): add user authentication with username/password

- Add authenticateUser function with credential validation
- Integrate auth endpoint to router
- Add unit tests for authentication logic"
```
````

**示例：正确的动作划分**

✅ **正确的任务**（一个任务内）：
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

**测试方式分类说明：**

1. **单元测试** - 自动化测试，提供具体的测试命令和预期输出
   ```bash
   pnpm test tests/unit/some-module.test.ts
   ```

2. **集成测试** - 测试多个组件的协作，提供测试命令
   ```bash
   pnpm test tests/integration/api.test.ts
   ```

3. **用户协助验证** - 需要用户手动验证的场景，必须详细描述验证步骤
   ```markdown
   **用户协助验证:**
   1. 启动开发服务器: `pnpm dev`
   2. 打开浏览器访问: http://localhost:3000
   3. 点击登录按钮，输入用户名和密码
   4. 验证是否成功跳转到首页
   5. 验证是否显示用户信息
   ```

### 阶段 5：并行计划审查

**目标：** 确保计划完整覆盖设计要求，验证一致性、文件定位准确性和测试完整性

**小型设计：审查单一计划**

**并行启动 4 个 plan-reviewer agents**，每个提供不同的审查重点：
- **agent 1 (design coverage)**：审查计划是否完整覆盖设计文档中的所有功能、组件和约束
- **agent 2 (consistency & quality)**：审查计划与设计的一致性、任务划分合理性、可执行性
- **agent 3 (completeness & gaps)**：审查是否有遗漏的功能点、缺失的边界情况、未考虑的错误处理
- **agent 4 (file location & testing)**：审查文件路径是否准确、修改位置是否明确、测试方式是否完整

**使用 Task 工具调用 plan-reviewer agent，在 prompt 中明确提供文档路径：**

```
Task({
  subagent_type: "plan-reviewer",
  prompt: `审查实施计划，重点：[design coverage / consistency & quality / completeness & gaps]

计划文档：docs/plans/YYYY-MM-DD-<feature-name>-plan.md
设计文档：docs/plans/YYYY-MM-DD-<feature-name>-design.md

请读取这两个文档，审查计划是否完整覆盖了设计要求。只报告高置信度问题（≥80）。`
})
```

**中/大型设计：审查阶段性计划**

**首先审查路线图：**
- 审查阶段划分是否合理
- 审查每个阶段的验收标准是否明确
- 审查阶段之间的依赖关系是否正确

**然后分阶段审查每个计划：**
对于每个阶段计划，并行启动 3 个 plan-reviewer agents：
- **agent 1**：审查该阶段是否完整覆盖了设计中的相关部分
- **agent 2**：审查该阶段的验收标准是否可执行、测试是否充分
- **agent 3**：审查文件路径是否准确、修改位置是否明确、测试方式是否完整

**审查提示词示例：**

```
Task({
  subagent_type: "plan-reviewer",
  prompt: `审查阶段性计划

计划文档：docs/plans/YYYY-MM-DD-<feature-name>-phase1-plan.md
设计文档：docs/plans/YYYY-MM-DD-<feature-name>-design.md
路线图：docs/plans/YYYY-MM-DD-<feature-name>-roadmap.md

请审查：
1. 这个阶段是否完整覆盖了设计中相关的功能点
2. 验收标准是否具体、可执行
3. 是否有遗漏的功能或边界情况

只报告高置信度问题（≥80）。`
})
```

要求 agent：
- 从 prompt 中获取文档路径，读取文档内容
- 只报告高置信度问题（置信度 ≥ 80）
- 重点关注设计覆盖度、一致性和可执行性
- 对于阶段性计划，特别关注验收标准的可执行性
- 提供具体的修复建议

### 阶段 6：修复关键问题

**目标：** 提高计划质量，确保完整覆盖设计要求

**行动：**
1. 整合所有 plan-reviewer agents 的发现
2. 识别高置信度问题（特别是设计覆盖度、一致性、文件定位和测试问题）
3. 修复这些问题
4. 如果发现重大遗漏或设计偏离，可能需要回到阶段 3 重新设计
5. 反复审查直到没有高置信度问题

### 阶段 7：保存实施计划

**目标：** 保存最终计划

**小型设计：保存单一计划**
- 保存最终计划到 `docs/plans/YYYY-MM-DD-<feature-name>-plan.md`
- 确保计划完整、准确、可执行

**中/大型设计：保存阶段性计划**
- 保存路线图到 `docs/plans/YYYY-MM-DD-<feature-name>-roadmap.md`
- 保存每个阶段的计划到对应文件：
  - `docs/plans/YYYY-MM-DD-<feature-name>-phase1-plan.md`
  - `docs/plans/YYYY-MM-DD-<feature-name>-phase2-plan.md`
  - ...
- 确保每个阶段的验收标准明确、可执行
- 提交所有计划文件：`git add docs/plans/YYYY-MM-DD-<feature-name>-*.md`

## 执行交接

**小型设计：直接执行**

```
计划完成并保存到 `docs/plans/YYYY-MM-DD-<topic>-plan.md`。

你应该结束本次会话，开启新的会话，并复制以下命令到新的会话窗口：

/supercode:executing-plans docs/plans/YYYY-MM-DD-<topic>-plan.md
```

**中/大型设计：分阶段执行**

```
阶段性计划完成！

路线图：docs/plans/YYYY-MM-DD-<topic>-roadmap.md

**执行步骤：**

1. 结束本次会话，开启新的会话
2. 从阶段1开始执行：
   /supercode:executing-plans docs/plans/YYYY-MM-DD-<topic>-phase1-plan.md

3. 阶段1完成后，运行验收测试，确认通过后继续下一阶段
4. 执行阶段2：
   /supercode:executing-plans docs/plans/YYYY-MM-DD-<topic>-phase2-plan.md

5. 依次执行所有阶段

**重要提醒：**
- 每个阶段完成后必须运行验收测试
- 只有当前阶段通过验收后，才进入下一阶段
- 如果某个阶段验收失败，修复问题后重新运行验收测试
```

## 关键原则

- **阶段性优先** — 大型设计或设计文档已分阶段的，必须拆分为独立阶段，每个阶段可验证、可交付
- **验收标准明确** — 每个阶段必须有具体的验收标准和测试方式
- **并行优于串行** — 使用多个 agents 并行探索不同维度
- **完整任务分解** — 每个步骤应该是 5-15 分钟的动作
- **精确文件路径** — 每个任务必须列出所有变更文件的完整路径、修改类型和位置
- **实现要点清晰** — 描述要做什么、核心思路和关键接口，而不是写完整代码
- **测试明确** — 每个任务必须包含明确的测试方式：单元测试（命令）、集成测试（命令）、用户协助验证（步骤）
- **精确命令** — 包含精确的命令和预期输出
- **DRY, YAGNI, TDD** — 遵循核心原则
- **频繁提交** — 鼓励频繁提交
- **质量第一** — 通过并行审查确保计划质量
- **代码库探索** — 在编写计划前必须探索现有代码库，理解现有结构
- **指挥棒原则** — 计划是指挥棒，让编码变简单，而不是替代编码
