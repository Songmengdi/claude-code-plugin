---
name: github-browser
description: This skill should be used when the user asks to "browse GitHub", "view GitHub code", "search GitHub repositories", "explore GitHub projects", "explore codebase", or wants to access/analyze code from GitHub repositories using the browser automation tool.
---

# GitHub Browser

探索 GitHub 代码库的核心工具。

## 核心脚本

### 1. get-info.py - 仓库概览

获取仓库的基本信息、依赖配置、语言统计等。

```bash
./scripts/get-info.py <owner> <repo>
```

**输出内容：**
- 基本信息：名称、描述、Stars、Forks、默认分支
- README 预览
- 主要文件检测
- 依赖信息（package.json/requirements.txt 等）
- 语言分布
- 最近提交

**示例：**
```bash
./scripts/get-info.py supermemoryai opencode-supermemory
```

### 2. get-tree.py - 目录结构

获取目录树结构，支持递归展开子目录。

```bash
./scripts/get-tree.py <owner> <repo> <depth> [path]
```

**参数说明：**
- `owner` - GitHub 仓库所有者
- `repo` - 仓库名称
- `depth` - 目录树深度（推荐 2-3）
- `path` - 可选，指定起始路径（如 `src`）

**示例：**
```bash
# 获取根目录 2 层
./scripts/get-tree.py supermemoryai opencode-supermemory 2

# 获取 src 目录 3 层
./scripts/get-tree.py supermemoryai opencode-supermemory 3 src
```

**输出格式：**
```
├── src/
│   ├── services/
│   ├── types/
│   ├── cli.ts
│   ├── config.ts
│   └── index.ts
└── package.json
```

### 3. get-file.sh - 获取单个文件

```bash
./scripts/get-file.sh <owner> <repo> <file-path> [branch]
```

**说明：**
- 文件 ≤300 行：直接打印到控制台
- 文件 >300 行：保存到 `/tmp/` 并显示文件信息

**示例：**
```bash
./scripts/get-file.sh supermemoryai opencode-supermemory src/index.ts
./scripts/get-file.sh supermemoryai opencode-supermemory package.json
```

## 探索代码库工作流

### 标准流程

```bash
# 1. 获取仓库概览
./scripts/get-info.py <owner> <repo>

# 2. 查看目录结构（2-3层）
./scripts/get-tree.py <owner> <repo> 2

# 3. 根据需要深入特定目录
./scripts/get-tree.py <owner> <repo> 3 src

# 4. 获取关键文件内容
./scripts/get-file.sh <owner> <repo> src/index.ts
./scripts/get-file.sh <owner> <repo> package.json
```

### 示例：探索 OpenCode 插件

```bash
# 1. 获取插件仓库信息
./scripts/get-info.py supermemoryai opencode-supermemory

# 2. 查看目录结构
./scripts/get-tree.py supermemoryai opencode-supermemory 2

# 3. 进入 src 目录查看
./scripts/get-tree.py supermemoryai opencode-supermemory 3 src

# 4. 读取主要入口文件
./scripts/get-file.sh supermemoryai opencode-supermemory src/index.ts

# 5. 查看 package.json 了解依赖
./scripts/get-file.sh supermemoryai opencode-supermemory package.json
```

## 降级方案

当脚本工具不可用时，参考 **`references/agent-browser.md`** 使用 agent-browser 直接操作。

## Additional Resources

### Reference Files

- **`references/agent-browser.md`** - agent-browser 直接操作指南（降级方案）

### Scripts 目录

| 脚本 | 用途 |
|-------|-------|
| `get-info.py` | 仓库完整信息 |
| `get-tree.py` | 目录树结构 |
| `get-file.sh` | 获取单个文件 |
