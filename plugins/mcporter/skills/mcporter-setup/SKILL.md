---
name: mcporter-setup
description: "Use this skill whenever the user needs to install mcporter or use mcporter to install/configure MCP servers. 用中文表达时也会触发：当用户说「用mcporter安装MCP」「使用mcporter添加配置」「mcporter配置」「设置mcporter」「通过mcporter安装server」「mcporter帮忙配置」「配置mcporter服务器」「安装MCP server」「添加MCP配置」「mcporter配置错误」「mcporter配置问题」「mcporter配置文件」「项目级配置」「全局配置」「从cursor导入配置」「从claude导入配置」「从vscode导入配置」「迁移MCP配置」等中文表达时必须触发。Trigger when: user asks to install mcporter itself, install/add/configure/setup an MCP server with mcporter, wants to set up mcporter.json config, encounters mcporter config errors, asks about mcporter config scope (project vs home), or needs to import/convert MCP configs from editors (Cursor, Claude, VS Code, etc) to mcporter format."
disable-model-invocation: true
---

# mcporter — 安装与配置指南

**本 SKILL 职责**：
1. 检查并安装 mcporter（若不存在）
2. 使用 mcporter 安装全局或项目级 MCP 服务器
3. 从其他编辑器导入 MCP 配置并转换为 mcporter 格式

**日常使用**（调用工具、查看工具列表）不在本 SKILL 范围内，用户可自行通过 `mcporter --help` 和 `mcporter list <server>` 了解。


## 职责一：检查并安装 mcporter

### 检查 mcporter 是否已安装

```bash
mcporter --version
```

若命令不存在，执行全局安装：

```bash
npm install -g mcporter
# 或
pnpm add -g mcporter
```

安装后验证：
```bash
mcporter --version  # 应显示版本号
mcporter --help     # 查看完整命令参考
```

---

## 职责二：使用 mcporter 安装 MCP 服务器

### 配置作用域选择

- **`--scope project`**（默认）：写入 `<root>/config/mcporter.json`，随项目共享，**推荐优先使用**
- **`--scope home`**：写入 `~/.mcporter/mcporter.json`，仅当前用户生效

不要主动切换到全局配置，除非用户明确要求。

### 添加 HTTP server

```bash
mcporter config add <name> <url>
```

示例：
```bash
mcporter config add mcp-server https://api.example.com/mcp
```

### 添加 STDIO server

STDIO server 需指定命令和参数：

```bash
mcporter config add <name> --transport stdio --command <executable> --arg <arg1> --arg <arg2>
```

示例：
```bash
mcporter config add myserver --transport stdio --command node --arg ./dist/index.js
```

添加到全局配置：
```bash
mcporter config add myserver --transport stdio --command node --arg ./dist/index.js --scope home
```

### 验证配置

```bash
mcporter config doctor      # 验证配置语法
mcporter list               # 列出所有已配置的 server
mcporter list <name>        # 查看特定 server 的工具列表
```

### 删除配置

```bash
mcporter config remove <name>
```

---

## 职责三：从其他编辑器导入配置

mcporter 支持从以下编辑器导入现有 MCP 配置：

### 支持的编辑器

- `cursor` — Cursor
- `claude` — Claude Desktop / Claude Code
- `vscode` — VS Code
- `codex` — Codex
- `windsurf` — Windsurf
- `opencode` — OpenCode

### 导入命令

```bash
mcporter config import cursor --copy       # 从 .cursor/mcp.json 导入
mcporter config import claude --copy       # 从 Claude 导入配置
mcporter config import vscode --copy       # 从 VS Code 导入配置
```

### 配置转换说明

导入时 mcporter 会自动将编辑器配置转换为其格式：

**编辑器格式示例**（Cursor/Claude Code）：
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    }
  }
}
```

**mcporter 转换后**：
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    }
  },
  "imports": []
}
```

---

## 已知陷阱与解决方案

### 陷阱1：`--config` 参数冲突

若 server 的参数包含 `--config`，`--arg --config` 会被 mcporter 解析器误认为其自身全局标志。

**解决方案**：直接编辑配置文件

项目级配置位置：
```bash
<root>/config/mcporter.json
```

全局配置位置：
```bash
~/.mcporter/mcporter/mcporter.json
```

手动添加配置：
```json
{
  "mcpServers": {
    "myserver": {
      "command": "node",
      "args": ["./dist/index.js", "--config", "./config.json", "--secrets", "./secrets.json"]
    }
  },
  "imports": []
}
```

### 陷阱2：server 名称含连字符

调用时使用点分隔语法会解析异常（如 `vcp-memory.memory.add`）。

**解决方案**：使用 `--server` 和 `--tool` 分开指定
```bash
mcporter call --server vcp-memory --tool memory.get_stats
```

### 陷阱3：配置文件查找顺序

mcporter 按以下顺序查找配置（命中第一个即停止）：

1. `--config <path>` 命令行参数
2. `MCPORTER_CONFIG` 环境变量
3. `<root>/config/mcporter.json`（项目级）
4. `~/.mcporter/mcporter/mcporter.json`（用户级）

未设置 `--config`/`MCPORTER_CONFIG` 时，用户级和项目级会合并（项目级覆盖同名条目）。

---

## 临时试用 server（无需改配置）

```bash
mcporter list --http-url <url> --name <name>     # HTTP server
mcporter list --stdio "command"                  # STDIO server
```

---

## 故障排查

- **进程挂起诊断**：`MCPORTER_DEBUG_HANG=1 mcporter call ...`
- **STDIO 日志**：`MCPORTER_STDIO_LOGS=1 mcporter list <name>`
- **OAuth 认证**：`mcporter auth <name>` 或 `mcporter config login <name>`
- **生成独立 CLI**：`mcporter generate-cli <name> --bundle dist/cli.js`

---

## 版本与仓库

版本: 0.8.1 | 仓库: https://github.com/steipete/mcporter | 许可: MIT

