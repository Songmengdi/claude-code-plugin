---
name: optimize-prompt
description: 优化指定文件中的提示词，支持命令、SKILL、Agent的提示词优化
argument-hint: <file-path>
allowed-tools: ["Read", "Write", "Grep", "Glob", "Edit"]
---

分析并优化指定文件中的提示词。

**工作流程:**

1. 读取目标文件，识别文件类型（命令/SKILL/Agent）
2. 分析当前提示词的质量问题
3. 基于提示词优化知识生成改进建议
4. 直接修改文件，应用优化后的提示词
5. 记录优化历史到 .optimization-history.json

**优化维度:**

- **清晰度**: 消除模糊表达，增加具体指令
- **完整性**: 补充缺失的上下文和约束
- **结构化**: 定义清晰的输出格式
- **示例性**: 添加必要的示例和使用场景

**支持的文件类型:**

- `commands/*.md` - 命令提示词（description、argument-hint）
- `skills/*/SKILL.md` - SKILL提示词（description、body）
- `agents/*.md` - Agent提示词（description、system prompt）

**优化历史记录格式:**

```json
{
  "file": "path/to/file.md",
  "timestamp": "2025-01-29T12:00:00Z",
  "type": "command|skill|agent",
  "changes": [
    {
      "section": "description",
      "before": "...",
      "after": "..."
    }
  ],
  "summary": "Optimization summary"
}
```

**使用示例:**

```bash
/optimize-prompt commands/review.md
/optimize-prompt agents/code-reviewer.md
/optimize-prompt skills/api-testing/SKILL.md
```

**注意事项:**

- 始终保留 YAML frontmatter 结构
- 保持原有的核心意图和功能
- 添加的示例应符合实际使用场景
- 优化后提示词应通过可读性测试
