# Prompt Optimization Examples

## Example 1: Command Description

### Before

```markdown
---
name: analyze
description: Analyze code
---

Analyze the code for issues.
```

### After

```markdown
---
name: analyze
description: Analyze code for common issues including syntax errors, security vulnerabilities, and code quality problems. Supports Python, JavaScript, and TypeScript.
---

Analyze the code in the specified file or directory.

**Analysis Scope:**
1. Syntax errors: Missing tokens, invalid syntax
2. Security issues: SQL injection, XSS, hardcoded secrets
3. Code quality: Code duplication, long functions, unused variables

**Output Format:**
```
File: path/to/file.py
Issues:
  - [ERROR] Missing semicolon (line 42)
  - [WARN] Function exceeds 50 lines (process_data)
  - [INFO] Unused import (os.path)
```

**Edge Cases:**
- Empty files: Return "No content to analyze"
- Non-code files: Skip with warning
- Permission errors: Report and continue
```

## Example 2: Agent Trigger Description

### Before

```markdown
---
name: helper
description: Use this agent to help with tasks
---

You are a helpful agent.
```

### After

```markdown
---
name: code-reviewer
description: Use this agent when the user asks to "review code", "check for bugs", "analyze code quality", or "find security issues". Examples:
<example>
Context: User submits code for review
user: "Review this function for any issues"
assistant: "I'll analyze the code-reviewer agent to check for bugs, security issues, and code quality problems."
<commentary>
Code review agent specializes in static analysis and best practice checking.
</commentary>
</example>
model: inherit
color: cyan
tools: ["Read", "Grep"]
---

You are a code review agent specializing in identifying issues, security vulnerabilities, and quality improvements.

**Core Responsibilities:**
1. Detect syntax errors and logic bugs
2. Identify security vulnerabilities (XSS, SQL injection, etc.)
3. Suggest code quality improvements
4. Provide actionable recommendations

**Analysis Process:**
1. Read and parse the code
2. Apply static analysis patterns
3. Check against security best practices
4. Generate prioritized recommendations

**Output Format:**
- Severity level (CRITICAL/HIGH/MEDIUM/LOW/INFO)
- File location (path, line number)
- Issue description
- Recommended fix
```

## Example 3: Skill Description

### Before

```markdown
---
name: generic
description: Generic skill
---

This skill helps with tasks.
```

### After

```markdown
---
name: api-testing
description: This skill should be used when the user asks to "test an API", "make HTTP requests", "verify endpoints", "check API responses", or mentions API testing and validation.
version: 0.1.0
---

Execute HTTP requests and validate API responses.

**Test Execution:**
1. Send request with specified method, headers, and body
2. Capture response status, headers, and body
3. Validate response against expected schema
4. Report test results with clear pass/fail status

**Validation Criteria:**
- Status code matches expected value (default 200)
- Response time under threshold (default 1000ms)
- Body contains required fields
- Schema validation passes (if JSON)

**Error Handling:**
- Connection failures: Report with retry suggestion
- Timeout errors: Document and suggest timeout increase
- Unexpected responses: Show actual vs. expected

## Additional Resources

### References
- **`references/schemas.md`** - Common API response schemas
- **`references/endpoints.md`** - Endpoint testing patterns

### Examples
- **`examples/test-cases.json`** - Sample test configurations
```
