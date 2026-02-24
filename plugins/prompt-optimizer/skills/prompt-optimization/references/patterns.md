# Common Prompt Patterns and Anti-Patterns

## Anti-Patterns to Avoid

### 1. "Whatever You Think Best"

**Problem:** Removes constraints, leads to unpredictable behavior
**Solution:** Specify criteria for decision-making

**Anti-pattern:**
```
"Format the output however you think is best"
```

**Better:**
```
"Format output as JSON with 'fields' array. Include 'name', 'type', and 'required' for each field"
```

### 2. Implicit Expectations

**Problem:** Assumes knowledge or inference of unstated requirements
**Solution:** Make all requirements explicit

**Anti-pattern:**
```
"Handle the file"
```

**Better:**
```
"Read the file, validate UTF-8 encoding, parse as JSON, extract 'data' field"
```

### 3. Ambiguous Success Criteria

**Problem:** Success conditions unclear
**Solution:** Define explicit success criteria

**Anti-pattern:**
```
"Make it work correctly"
```

**Better:**
```
"Function should return true if file exists and is readable, false otherwise. Throw exception for permission errors"
```

### 4. Overly General Instructions

**Problem:** Too broad, leads to context bloat
**Solution:** Narrow scope to specific domain

**Anti-pattern:**
```
"Help the user with their request"
```

**Better:**
```
"Diagnose and fix syntax errors in Python files. Focus on common issues: missing colons, indentation, and unclosed brackets"
```

## Best Practice Patterns

### 1. The S.M.A.R.T. Framework

**Specific:** Precise, unambiguous requirements
**Measurable:** Observable outcomes or metrics
**Achievable:** Within capabilities
**Relevant:** Aligned with purpose
**Time-boxed:** Scope boundaries

### 2. The Context-Action-Output Template

```markdown
**Context:** What situation or context applies
**Action:** What should be done
**Output:** What result to provide
```

### 3. The Example-Guided Approach

Provide examples for:
- Expected input format
- Desired output format
- Edge case behavior
- Error handling

### 4. The Progressive Constraints Pattern

Start with core requirements, then add constraints:

1. Base requirement: "Process the file"
2. Add format: "Process JSON files"
3. Add validation: "Validate schema before processing"
4. Add error handling: "Report validation errors to user"

## Domain-Specific Patterns

### For Code Generation

1. Specify language, framework, and version
2. Include import statements and structure
3. Define function signatures
4. Show example usage

### For Data Analysis

1. Define input data schema
2. Specify transformation rules
3. Define output format
4. Handle null/invalid data

### For Troubleshooting

1. Reproduction steps
2. Expected vs. actual behavior
3. Environment details
4. Error messages and logs
