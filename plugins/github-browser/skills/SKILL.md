---
name: github-browser
description: This skill should be used when the user asks to "browse GitHub", "view GitHub code", "explore GitHub projects", "clone GitHub repository", or wants to access/analyze code from GitHub repositories using local git clone and file system tools.
---

# GitHub Browser

使用 git clone 将 GitHub 代码库克隆到本地，然后用本地文件系统工具进行高效探索。

## 重要：仓库生命周期管理

### 核心原则

1. **不自动删除**：克隆的仓库在 session 期间保持存在，供后续探索使用
2. **复用优先**：每次操作前先检查仓库是否已存在本地
3. **手动清理**：仅当用户明确要求时才删除仓库

### 仓库目录规范

所有克隆的仓库统一存放在 `/tmp/github-browser-<owner>-<repo>`

## 核心工作流

### 1. 检查并克隆仓库（第一步必须执行）

```bash
# 定义仓库路径
REPO_PATH="/tmp/github-browser-<owner>-<repo>"

# 先检查是否已存在
if [ -d "$REPO_PATH" ]; then
  echo "仓库已存在，复用现有仓库: $REPO_PATH"
else
  echo "仓库不存在，开始克隆..."
  git clone --depth 1 https://github.com/<owner>/<repo>.git "$REPO_PATH"
fi
```

**重要**：每次开始探索 GitHub 仓库时，必须先执行上述检查逻辑，避免重复克隆。

### 2. 探索目录结构

使用 Glob 工具获取目录结构：

```
# 获取根目录文件和目录
Glob: pattern="*" in /tmp/github-browser-<owner>-<repo>

# 获取特定目录（如 src）
Glob: pattern="**/*" in /tmp/github-browser-<owner>-<repo>/src
```

### 3. 搜索关键内容

使用 Grep 工具搜索代码内容：

```
# 搜索关键词
Grep: pattern="function main" in /tmp/github-browser-<owner>-<repo>

# 按文件类型搜索
Grep: pattern="TODO" type="js" in /tmp/github-browser-<owner>-<repo>
```

### 4. 读取文件内容

使用 Read 工具读取具体文件：

```
# 读取配置文件
Read: /tmp/github-browser-<owner>-<repo>/package.json

# 读取源码文件
Read: /tmp/github-browser-<owner>-<repo>/src/index.ts
```

## 仓库清理策略

### Session 期间保持仓库

克隆的仓库在整个 session 期间保持存在，允许：
- 多轮探索同一仓库
- 深入分析后继续查询
- 无需重复网络请求

### 清理时机

**仅以下情况删除仓库：**

1. **用户明确要求**：当用户说"删除仓库"、"清理"、"不需要了"等
2. **Session 结束时**：通过 Claude Code 的 `SessionEnd` hook 自动清理（需用户配置，参见 README.md）

### 手动清理命令

当用户要求清理时执行：

```bash
# 清理特定仓库
rm -rf /tmp/github-browser-<owner>-<repo>

# 清理所有 github-browser 仓库
rm -rf /tmp/github-browser-*
```

## 探索代码库完整工作流

### 标准流程

```bash
# 1. 检查并克隆仓库
REPO_PATH="/tmp/github-browser-<owner>-<repo>"
if [ ! -d "$REPO_PATH" ]; then
  git clone --depth 1 https://github.com/<owner>/<repo>.git "$REPO_PATH"
fi

# 2. 查看根目录结构（使用 Glob）
# 找到主要目录：src/, lib/, tests/, etc.

# 3. 读取关键配置文件（使用 Read）
# package.json, requirements.txt, Cargo.toml, go.mod, etc.

# 4. 深入主要代码目录
# 使用 Glob 查看目录结构

# 5. 搜索特定功能或模式
# 使用 Grep 搜索代码

# 6. 读取关键文件进行深入分析

# 注意：不要在这里删除仓库！保留供后续使用
```

### 示例：探索 React 项目

```bash
# 1. 检查并克隆
REPO_PATH="/tmp/github-browser-facebook-react"
if [ ! -d "$REPO_PATH" ]; then
  git clone --depth 1 https://github.com/facebook/react.git "$REPO_PATH"
fi

# 2. 查看根目录结构
# Glob: "*" in /tmp/github-browser-facebook-react

# 3. 读取 package.json 了解项目结构
# Read: /tmp/github-browser-facebook-react/package.json

# 4. 进入 packages 目录
# Glob: "*/" in /tmp/github-browser-facebook-react/packages

# 5. 搜索核心组件
# Grep: "export function" type="ts" in /tmp/github-browser-facebook-react/packages/react

# 仓库保留，不删除
```

## Additional Resources

### 本地工具参考

| 工具 | 用途 | 示例 |
|------|------|------|
| `Bash` | 检查目录/执行 git clone | `git clone --depth 1 <url>` |
| `Glob` | 查找文件和目录 | `pattern="**/*.ts"` |
| `Grep` | 搜索代码内容 | `pattern="TODO" type="js"` |
| `Read` | 读取文件内容 | 读取配置或源码 |

### 目录命名规范

临时目录统一使用前缀 `/tmp/github-browser-<owner>-<repo>`，便于：
- 识别来源
- 批量清理
- 避免命名冲突

### 常见问题

**Q: 为什么要复用已存在的仓库？**
A: 避免重复网络请求，提升多轮探索效率。

**Q: 什么时候仓库会被删除？**
A: 仅当用户明确要求，或 session 结束时通过 hook 自动清理。

**Q: 如何查看当前有哪些克隆的仓库？**
```bash
ls -la /tmp/github-browser-*
```
