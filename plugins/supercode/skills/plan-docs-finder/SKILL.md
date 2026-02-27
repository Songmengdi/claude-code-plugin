---
name: plan-docs-finder
description: 专属 skill，扫描 docs/plans 目录提取所有文档的 frontmatter 元数据
---

# Plan 文档查找器

## 概述

**辅助工具**：快速扫描 `docs/plans/` 目录，提取所有文档的 frontmatter 元数据。

用于加速 `feature-context-loader` 的探索流程，避免逐个读取文档。

## 执行命令

```bash
node scripts/plan-docs-finder.js
```

## 返回格式

```json
[
  {
    "path": "docs/plans/2024-01-15-login-design.md",
    "type": "design",
    "tags": ["auth", "login", "user-management"],
    "related": {
      "design": "docs/plans/2024-01-10-login-v1-design.md",
      "plan": "docs/plans/2024-01-10-login-v1-plan.md"
    },
    "status": "design"
  },
  {
    "path": "docs/plans/2024-01-15-login-plan.md",
    "type": "plan",
    "tags": ["auth", "login"],
    "related": {
      "design": "docs/plans/2024-01-15-login-design.md"
    },
    "status": "executed"
  }
]
```

## 使用方式

```javascript
// 1. 执行脚本获取所有文档元数据
const metadata = await executeCommand('node scripts/plan-docs-finder.js');

// 2. 按 type 过滤
const designs = metadata.filter(m => m.type === 'design');
const plans = metadata.filter(m => m.type === 'plan');

// 3. 按 tags 匹配
const matched = designs.filter(d =>
    d.tags?.includes(keyword) || d.path.includes(keyword)
);

// 4. 按 related 递归追溯
function getRelatedDocs(doc, allDocs) {
    const result = [doc];
    for (const key of Object.keys(doc.related || {})) {
        const relatedPath = doc.related[key];
        const relatedDoc = allDocs.find(d => d.path === relatedPath);
        if (relatedDoc) {
            result.push(...getRelatedDocs(relatedDoc, allDocs));
        }
    }
    return result;
}
```

## 注意事项

- 目录不存在时返回空数组 `[]`
- 缺少 frontmatter 的文档被跳过
- 文档类型通过文件名后缀识别：`-design.md` / `-plan.md`
