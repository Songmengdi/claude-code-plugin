---
name: github-browser
description: This skill should be used when the user asks to "browse GitHub", "view GitHub code", "explore GitHub projects", "clone GitHub repository", or wants to access/analyze code from GitHub repositories using local git clone and file system tools.
---

# GitHub Browser

使用 git clone 将 GitHub 代码库克隆到本地，然后用本地文件系统工具进行高效探索。

## 核心工作流

### 1. 克隆仓库

使用 git clone 将 GitHub 仓库克隆到本地临时目录：

```bash
# 克隆仓库到临时目录（只克隆最新提交，速度快）
git clone --depth 1 https://github.com/<owner>/<repo>.git /tmp/github-browser-<repo>
```

使用 `--depth 1` 只克隆最新提交，文件完整但无历史记录，显著提升速度。

### 2. 探索目录结构

使用 Glob 工具获取目录结构：

```
# 获取根目录文件和目录
Glob: pattern="*" in /tmp/github-browser-<repo>

# 获取特定目录（如 src）
Glob: pattern="**/*" in /tmp/github-browser-<repo>/src
```

### 3. 搜索关键内容

使用 Grep 工具搜索代码内容：

```
# 搜索关键词
Grep: pattern="function main" in /tmp/github-browser-<repo>

# 按文件类型搜索
Grep: pattern="TODO" type="js" in /tmp/github-browser-<repo>
```

### 4. 读取文件内容

使用 Read 工具读取具体文件：

```
# 读取配置文件
Read: /tmp/github-browser-<repo>/package.json

# 读取源码文件
Read: /tmp/github-browser-<repo>/src/index.ts
```

## 探索代码库工作流

### 标准流程

```bash
# 1. 克隆仓库
git clone --depth 1 https://github.com/<owner>/<repo>.git /tmp/github-browser-<repo>

# 2. 查看根目录结构（使用 Glob）
# 找到主要目录：src/, lib/, tests/, etc.

# 3. 读取关键配置文件（使用 Read）
# package.json, requirements.txt, Cargo.toml, go.mod, etc.

# 4. 深入主要代码目录
# 使用 Glob 查看目录结构

# 5. 搜索特定功能或模式
# 使用 Grep 搜索代码

# 6. 读取关键文件进行深入分析

# 7. 完成后清理
rm -rf /tmp/github-browser-<repo>
```

### 示例：探索 React 项目

```bash
# 1. 克隆仓库
git clone --depth 1 https://github.com/facebook/react.git /tmp/github-browser-react

# 2. 查看根目录结构
# Glob: "*" in /tmp/github-browser-react

# 3. 读取 package.json 了解项目结构
# Read: /tmp/github-browser-react/package.json

# 4. 进入 packages 目录
# Glob: "*/" in /tmp/github-browser-react/packages

# 5. 搜索核心组件
# Grep: "export function" type="ts" in /tmp/github-browser-react/packages/react

# 6. 清理
rm -rf /tmp/github-browser-react
```

## Additional Resources

### 本地工具参考

| 工具 | 用途 | 示例 |
|------|------|------|
| `Bash` | 执行 git clone | `git clone --depth 1 <url>` |
| `Glob` | 查找文件和目录 | `pattern="**/*.ts"` |
| `Grep` | 搜索代码内容 | `pattern="TODO" type="js"` |
| `Read` | 读取文件内容 | 读取配置或源码 |

### 目录命名规范

临时目录统一使用前缀 `/tmp/github-browser-<repo>`，便于识别和清理。
