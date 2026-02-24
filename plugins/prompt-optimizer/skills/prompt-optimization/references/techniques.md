# Advanced Prompt Optimization Techniques

## Chain-of-Thought Prompting

Force explicit reasoning steps before final output.

```
Think step by step:
1. First, analyze the request
2. Then, identify relevant information
3. Next, formulate a solution
4. Finally, present the answer
```

**Best for:** Complex reasoning, multi-step problems

## Few-Shot Learning

Provide examples to guide behavior.

```
Example 1:
Input: "3 + 5"
Output: "8"

Example 2:
Input: "10 - 4"
Output: "6"

Now solve:
Input: "7 + 2"
Output:
```

**Best for:** Pattern matching, format consistency

## Role Prompting

Adopt a specific persona or expertise.

```
You are a senior software engineer with 10 years of experience.
Focus on maintainability, performance, and security.
```

**Best for:** Domain-specific tasks, quality standards

## Constraint-Based Optimization

Add explicit constraints to narrow solution space.

```
Constraints:
- Maximum length: 100 characters
- Must include error handling
- Use only Python standard library
- Return type: dict
```

**Best for:** Output format control, resource limits

## Self-Consistency

Generate multiple solutions and select best.

```
Consider 3 different approaches:
1. Approach A: [describe]
2. Approach B: [describe]
3. Approach C: [describe]

Evaluate each and recommend the best.
```

**Best for:** Ambiguous problems, trade-off analysis

## Iterative Refinement

Improve through multiple passes.

```
Draft 1: Create initial solution
Review: Check against requirements
Refine: Address issues in draft 1
Final: Present refined solution
```

**Best for:** Quality-critical outputs, creative tasks

## Meta-Cognition

Explicitly consider the task requirements.

```
Before starting, verify:
1. All inputs are provided
2. Required format is understood
3. Constraints are documented
4. Edge cases are considered

Proceed only after verification.
```

**Best for:** Complex workflows, reliability

## Decomposition Strategy

Break complex tasks into subtasks.

```
Decompose the task:
1. Parse input
2. Validate data
3. Process core logic
4. Format output
5. Return result

Handle each subtask independently.
```

**Best for:** Multi-step processes, error isolation
