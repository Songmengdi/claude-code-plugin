---
name: prompt-optimization
description: This skill should be used when the user asks to "optimize a prompt", "improve prompt quality", "analyze prompt effectiveness", "refine agent instructions", "enhance command descriptions", "improve system prompts", or mentions prompt engineering and optimization techniques.
version: 0.1.0
---

# Prompt Optimization

Prompt optimization improves the effectiveness of commands, SKILLs, and Agent prompts through systematic analysis and refinement based on execution experience.

## Core Principles

### Clarity Over Brevity

Clear, specific instructions outperform clever but vague directives. Use explicit requirements rather than implicit expectations.

**Weak:** "Handle errors appropriately"
**Strong:** "Catch exceptions, log error details, return user-friendly message, and exit gracefully"

### Contextual Completeness

Include all necessary context upfront rather than relying on follow-up questions or inference.

**Weak:** "Process the data"
**Strong:** "Process JSON files in ./data/, validate schema, transform to CSV, output to ./output/"

### Structured Output Format

Define expected output format precisely to enable reliable parsing and downstream processing.

**Weak:** "Return results"
**Strong:** "Return JSON array with 'id', 'name', 'status' fields; null for missing values"

## Optimization Checklist

### For Commands

- **Description clarity**: Does the description clearly state what the command does?
- **Argument specificity**: Are argument hints precise about expected input format?
- **Tool restrictions**: Does `allowed-tools` list only necessary tools?
- **Example coverage**: Do examples cover typical use cases and edge cases?
- **Error guidance**: Does the command provide guidance for common error scenarios?

### For SKILLs

- **Trigger specificity**: Does the description include concrete user phrases?
- **Progressive disclosure**: Is SKILL.md lean (~1,500-2,000 words)? Are details in references/?
- **Third-person description**: Is the description in third person?
- **Imperative body**: Does the body use imperative/infinitive form?
- **Resource references**: Are all referenced scripts/examples documented?

### For Agents

- **Strong triggering**: Does the description include 2-4 concrete examples?
- **Clear responsibilities**: Are agent responsibilities explicit and specific?
- **Process definition**: Is the analysis process step-by-step?
- **Output format**: Is the expected output clearly defined?
- **Tool limitation**: Are tools restricted to minimum necessary?

## Common Improvement Patterns

### Add Specific Examples

Add `<example>` blocks to agent descriptions or command documentation showing concrete triggering scenarios.

```yaml
<example>
Context: User needs to analyze code quality
user: "Review this file for issues"
assistant: "I'll use the code-reviewer agent..."
<commentary>
Agent handles code analysis with detailed reporting
</commentary>
</example>
```

### Clarify Vague Instructions

Replace vague language with specific directives.

**Before:** "Try to be helpful"
**After:** "Provide actionable recommendations prioritized by impact"

### Add Context Requirements

Explicitly state what context is needed for the task.

**Before:** "Optimize the function"
**After:** "Read the function file first, analyze performance bottlenecks, then implement optimizations"

### Define Edge Case Handling

Specify behavior for edge cases.

**Before:** "Process the input"
**After:** "Process input; handle null/empty by returning empty result; handle invalid format with error message"

## Optimization History Management

### Storage Location

**Critical**: Store optimization history in the **plugin directory**, not the project directory:

```
# ✅ Correct - Plugin directory
<plugin-root>/.optimization-history.json

# ❌ Incorrect - Project directory
echo "ERROR: Don't store plugin metadata in project directory"
<project-dir>/.claude/.optimization-history.json
```

**Why?** Plugin metadata belongs with the plugin, not scattered across projects. This ensures:
- Single source of truth for optimization history
- No conflicts when the plugin is used across multiple projects
- Clear separation between plugin functionality and project data

### History Format

```json
{
  "optimizations": [
    {
      "file": "path/to/file.md",
      "timestamp": "2025-01-29T12:00:00Z",
      "type": "command|skill|agent",
      "trigger": "what prompted this optimization",
      "changes": [
        {
          "section": "section name",
          "before": "previous content",
          "after": "new content",
          "reason": "why this change was made"
        }
      ],
      "lessons": "key takeaways for future optimizations"
    }
  ]
}
```

## Additional Resources

### Reference Files

For detailed optimization techniques and patterns:
- **`references/patterns.md`** - Common prompt patterns and anti-patterns
- **`references/techniques.md`** - Advanced optimization techniques

### Example Files

Working examples in `examples/`:
- **`before-after.md`** - Comparison of optimized prompts
