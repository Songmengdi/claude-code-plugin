# 功能上下文加载器（Feature Context Loader）

## 概述

在新会话中快速加载和总结功能的完整上下文，包括设计文档、计划文档和历史变更。

**调用方式**：由 `brainstorming` skill 通过 Task 工具调用
**辅助 skill**：`supercode:plan-docs-finder`

## 输入

从 brainstorming skill 接收以下信息之一：
- 功能描述（如"登录功能"、"用户导出"）
- 具体文档路径（如 `docs:plans/2024-01-15-login-design.md`）

## 探索流程

### 1. 获取文档元数据

调用 `plan-docs-finder` skill 获取所有文档的 frontmatter 元数据：

```javascript
const metadata = await Skill({
  skill: "supercode:plan-docs-finder"
});
```

### 2. 匹配相关文档

根据用户输入进行匹配：

**场景 A：功能描述**
- 提取关键词（移除"功能"、"模块"等后缀）
- 匹配 tags 或文件名中包含关键词的设计文档
- 取最匹配的前 3 个

**场景 B：具体文档路径**
- 精确匹配文档路径

### 3. 递归追溯关联文档

通过文档的 `related` 字段追溯关联的 plan/design 文档：
- 避免循环引用（使用 visited Set）
- 构建完整的文档链

### 4. 读取与总结

读取文档内容并提取关键信息：
- 从 design 文档末尾提取变更历史表格
- 总结设计核心内容（2-3 句话）
- 总结 plan 文档的任务状态

### 5. 格式化输出

生成 Markdown Table 格式的上下文摘要

## 输出

返回 Markdown Table 格式的上下文摘要：

```markdown
## 功能上下文

### 当前状态
| 项目 | 路径 | 状态 |
|------|------|------|
| 功能名称 | 登录功能 | - |
| Design 文档 | docs/plans/2024-01-15-login-design.md | design |
| Plan 文档 | docs/plans/2024-01-15-login-plan.md | executed |

### 历史变更
| 日期 | 变更描述 | Plan 文档 |
|------|----------|-----------|
| 2024-01-20 | 添加OAuth登录支持 | docs/plans/2024-01-20-login-oauth-plan.md |
| 2024-01-15 | 初始登录功能 | docs/plans/2024-01-15-login-plan.md |

### 已知问题/待办
- [从 design/plan 文档中提取]

### 设计摘要
[从最新的 design 文档中提取 2-3 句话的核心设计概述]

### 实施摘要
[从最新的 plan 文档中提取已完成/未完成的任务摘要]
```

## 未找到文档

```markdown
## 功能上下文

⚠️ 未找到相关文档

根据你的输入，未在 `docs/plans/` 目录中找到匹配的设计文档。

这可能意味着：
- 这是一个新功能
- 相关文档位于其他目录
- 文档命名不符合预期

请确认：
1. 这是否是一个新功能？
2. 是否有其他文档路径需要我加载？
```

## 记住

- **先元数据后内容** - 用 plan-docs-finder 批量获取 frontmatter，再按需读取全文
- **递归追溯** - 通过 related 字段构建完整的文档关系链
- **避免循环** - 使用 visited Set 防止循环引用
- **输出 Markdown Table** - 便于向用户展示
