# Claude Code Plugins

Claude Code 插件集合，扩展 Claude Code 的能力。

## 插件列表

### Skills

| 插件 | 说明 |
|------|------|
| [github-browser](./plugins/github-browser) | 通过 git clone 浏览 GitHub 仓库，使用本地文件系统工具高效探索代码 |

### MCP Servers

| 插件 | 说明 |
|------|------|
| mcp-excalidraw | Excalidraw 集成 |
| mcp-img-enhance | 图像增强处理 |
| mcp-pencil | Pencil 设计工具 |
| mcp-web-fetch | 网页抓取 |
| mcp-web-search | 网页搜索 |

### 其他

| 插件 | 说明 |
|------|------|
| pencil-design-guide | Pencil 设计指南 |
| prompt-optimizer | Prompt 优化器 |
| supercode | 超级代码工具 |
| vcp-memory | VCP 记忆模块 |

## 安装插件

### 添加市场

使用 `/plugin marketplace add` 命令添加此插件市场：

```bash
/plugin marketplace add Songmengdi/claude-code-plugin
```

### 安装插件

添加市场后，使用 `/plugin install` 安装所需插件：

```bash
/plugin install github-browser
```

## 配置 Hook（可选）

以 `github-browser` 为例，克隆的仓库会在 `/tmp/github-browser-*` 目录累积。可配置 hook 在 session 结束时自动清理。

在 `~/.claude/settings.json`（全局）或项目 `.claude/settings.json` 中添加：

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "rm -rf /tmp/github-browser-*"
          }
        ]
      }
    ]
  }
}
```

## 使用

安装 `github-browser` 后，在 Claude Code 中说：

- "浏览 GitHub 仓库 facebook/react"
- "查看 https://github.com/vercel/next.js 的代码结构"

详细配置见各插件的 README.md。
