---
name: optimize-history
description: 查看提示词优化历史记录
argument-hint: [--detail|--file <path>]
allowed-tools: ["Read", "Grep"]
---

显示提示词优化的历史记录。

**显示内容:**

- 优化时间戳
- 目标文件路径
- 文件类型（command/skill/agent）
- 优化摘要
- 主要变更点

**参数说明:**

- 无参数：显示所有优化记录的摘要列表
- `--detail`：显示详细的优化前后对比
- `--file <path>`：显示特定文件的优化历史

**输出格式:**

```
=== Optimization History ===

[2025-01-29 12:00:00] commands/review.md (command)
Summary: Improved description clarity and added output format

[2025-01-29 11:30:00] agents/code-reviewer.md (agent)
Summary: Enhanced triggering examples and structured system prompt

Total: 2 optimizations
```

**详细格式 (--detail):**

```
=== File: commands/review.md ===
Type: command
Time: 2025-01-29 12:00:00

Changes:
1. description
   Before: "Review code"
   After: "Review code for syntax errors, security vulnerabilities, and code quality issues. Supports Python, JavaScript, and TypeScript."

2. output-format
   Before: (not specified)
   After: "Return JSON with 'file', 'issues' fields"

Summary: Improved description clarity and added output format
```

**优化历史文件:**

历史记录存储在 `prompt-optimizer/.optimization-history.json`:

```json
{
  "optimizations": [
    {
      "file": "commands/review.md",
      "timestamp": "2025-01-29T12:00:00Z",
      "type": "command",
      "changes": [...],
      "summary": "..."
    }
  ]
}
```

**使用示例:**

```bash
/optimize-history                    # 摘要列表
/optimize-history --detail           # 详细记录
/optimize-history --file commands/review.md  # 特定文件
```
