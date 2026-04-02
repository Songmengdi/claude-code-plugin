# 计划文档模板

本文档包含实施计划文档的详细模板。

---

## 小型设计：单一计划头部

```markdown
---
tags: [功能标签1, 功能标签2, feature-id]
related:
  - design: docs/plans/YYYY-MM-DD-<feature-name>-design.md
status: plan  # plan | executed | completed
---

# [功能名称] 实施计划

> **给 Claude:** 必需子技能:使用 executing-plans 逐任务实施此计划。

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

---

## 中/大型设计：阶段性计划头部

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

> **给 Claude:** 必需子技能:使用 executing-plans 逐任务实施此计划。

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

---

## 路线图模板

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
4. 使用 `/executing-plans <phase-plan-path>` 执行各阶段
```

---

## 任务结构模板

每个任务是一个完整的、不破坏代码的最小功能变更（5-15 分钟）。

### 动作设计原则

1. **完整性**：一个动作包含实现某个最小功能所需的所有变更
2. **原子性**：每个动作实现后代码处于可工作状态
3. **最小变更**：一个动作对应一个最小的功能点
4. **多文件支持**：一个动作可能涉及多个文件的修改
5. **测试明确**：每个任务必须包含明确的测试方式
6. **指挥棒原则**：描述要做什么、怎么做，而不是写完整代码

### 任务必须包含的部分

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

**3. 测试方式**（必须）
- 明确测试类型：单元测试 | 集成测试 | 用户协助验证
- 提供具体的测试命令
- 描述验证步骤和预期结果

### 任务模板示例

````markdown
### 任务 N: [最小功能描述]

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

> **测试策略**：本任务包含纯逻辑（单元测试）、API 对接（集成测试）和端到端验证（用户协助）

**单元测试** — 验证核心逻辑:
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
````

### 正确的动作划分示例

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

### 测试方式分类说明

**测试策略选择原则**：根据阶段/任务的特点选择合适的测试类型

| 任务类型 | 推荐测试 | 原因 |
|---------|---------|------|
| 纯逻辑/算法 | 单元测试 | 快速验证逻辑正确性 |
| 函数/类重构 | 单元测试 | 确保行为不变 |
| 对接外部服务 | 集成测试 | 验证接口兼容性 |
| 数据库操作 | 集成测试 | 验证数据读写 |
| API 端点 | 集成测试 | 验证请求响应 |
| UI/交互 | 用户协助验证 | 需要人工判断体验 |
| 性能优化 | 性能测试 | 验证性能指标 |
| 边界情况 | 单元/集成 | 覆盖特殊场景 |

**1. 单元测试** - 验证纯逻辑和算法
```bash
pnpm test tests/unit/some-module.test.ts
```

**2. 集成测试** - 测试多个组件的协作
```bash
pnpm test tests/integration/api.test.ts
```

**3. 用户协助验证** - 需要用户手动验证
```markdown
**用户协助验证:**
1. 启动开发服务器: `pnpm dev`
2. 打开浏览器访问: http://localhost:3000
3. 点击登录按钮，输入用户名和密码
4. 验证是否成功跳转到首页
```
