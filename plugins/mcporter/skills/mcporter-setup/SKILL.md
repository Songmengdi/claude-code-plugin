---
name: mcporter-setup
description: "Use this skill whenever the user needs to install, configure, or set up mcporter MCP servers. Trigger when: user asks to install/add/configure an MCP server with mcporter, wants to set up mcporter.json config, encounters mcporter config errors, asks about mcporter config scope (project vs home), or needs to troubleshoot mcporter configuration issues. Also trigger when user mentions mcporter STDIO server setup, mcporter config add failures, or wants to import MCP configs from editors (Cursor, Claude Code, VS Code, etc)."
---

# mcporter — MCP 配置指南

版本: 0.8.1 | 仓库: https://github.com/steipete/mcporter | 许可: MIT

mcporter 是 MCP (Model Context Protocol) 的 CLI 工具。日常使用（查看工具、调用工具）通过 `mcporter --help` 和 `mcporter list <server>` 即可了解，本 SKILL 聚焦于**配置阶段**的已知陷阱和最佳实践。

## 快速查阅

- `mcporter list` — 列出所有已配置的 server
- `mcporter list <name> --schema` — 查看工具签名和示例
- `mcporter call --server <name> --tool <tool> --args '<json>'` — 调用工具
- `mcporter --help` — 完整命令参考

## 配置管理

### 添加 server

```bash
mcporter config add <name> <url>                          # HTTP server（默认写入项目级配置）
mcporter config add <name> --transport stdio --command node --arg ./s.js  # STDIO
mcporter config add <name> --transport stdio --command node --arg ./s.js --scope home  # 全局配置
mcporter config remove <name>                             # 删除
mcporter config doctor                                    # 验证配置
mcporter config import cursor --copy                      # 从编辑器导入
```

### 配置作用域

- `--scope project`（默认）：写入 `<root>/config/mcporter.json`，随项目共享，**推荐优先使用**
- `--scope home`：写入 `~/.mcporter/mcporter.json`，仅当前用户生效
- 不要主动切换到全局配置，除非用户明确要求

### STDIO 参数传递

`--command` 只接受可执行文件名，参数通过 `--arg` 逐个传递。对于不含 `--config` 的参数（如 `--secrets`、`--port`），`--arg` 可正常使用：

```bash
mcporter config add myserver --transport stdio --command node \
  --arg ./dist/index.js \
  --arg --secrets \
  --arg ./secrets.json
```

### 已知陷阱：`--config` 参数冲突

如果 server 的参数以 `--config` 开头，`--arg --config` 会被 mcporter 解析器误认为自身全局标志 `--config <path>`，导致命令失败。`--` 分隔符也无法绕过。

**解决方案**：直接编辑配置文件（项目级 `config/mcporter.json` 或全局 `~/.mcporter/mcporter.json`）：

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

### 调用含连字符的 server 名称

server 名称含连字符时（如 `vcp-memory`），点分隔语法 `vcp-memory.memory.add` 会解析异常。使用 `--server` 和 `--tool` 分开指定：

```bash
mcporter call --server vcp-memory --tool memory.get_stats
```

### 配置文件位置

查找顺序（命中第一个即停止）：

1. `--config <path>` 命令行参数
2. `MCPORTER_CONFIG` 环境变量
3. `<root>/config/mcporter.json`（项目级）
4. `~/.mcporter/mcporter/mcporter.json`（用户级）

未设置 `--config`/`MCPORTER_CONFIG` 时，用户级和项目级会合并（项目级覆盖同名条目）。

### 从编辑器导入配置

```bash
mcporter config import cursor --copy      # .cursor/mcp.json
mcporter config import claude-code --copy  # .claude/ 下的 MCP 配置
mcporter config import vscode --copy       # Code/User/mcp.json
```

支持：cursor, claude-code, claude-desktop, codex, windsurf, opencode, vscode。详见 `mcporter config import --help`。

## 其他

- **临时试用 server 无需改配置**：`mcporter list --http-url <url> --name <name>` 或 `--stdio "command"`
- **进程挂起诊断**：`MCPORTER_DEBUG_HANG=1 mcporter call ...`
- **STDIO 日志**：`MCPORTER_STDIO_LOGS=1 mcporter list <name>`
- **如果 `mcporter` 命令不存在**：执行 `npm install -g mcporter` 安装后重试
- **OAuth 认证**：`mcporter auth <name>` 或 `mcporter config login <name>`
- **生成独立 CLI**：`mcporter generate-cli <name> --bundle dist/cli.js`
