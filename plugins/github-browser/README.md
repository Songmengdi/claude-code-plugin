# GitHub Browser Plugin

通过 git clone 将 GitHub 仓库克隆到本地，使用本地文件系统工具高效探索代码库。

## 安装

### 方式一：通过市场安装（推荐）

```bash
# 1. 添加市场
/plugin marketplace add Songmengdi/claude-code-plugin

# 2. 安装插件
/plugin install github-browser
```

### 方式二：本地安装

将此插件目录复制到 Claude Code 的 plugins 目录：

```bash
cp -r plugins/github-browser ~/.claude/plugins/
```

## 配置自动清理

克隆的仓库默认保存在 `/tmp/github-browser-*` 目录。为了在 session 结束时自动清理这些目录，需要配置 hook。

### 方法一：项目级配置

在项目根目录创建 `.claude/settings.json`：

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

### 方法二：全局配置

在用户目录 `~/.claude/settings.json` 中添加相同配置，对所有项目生效。

### Hook 事件说明

- `SessionEnd`：当 Claude Code 会话结束时运行，适合清理临时文件

更多 hook 配置详见 [Claude Code Hooks 文档](https://code.claude.com/docs/zh-CN/hooks)。

## 手动清理

随时可以手动清理克隆的仓库：

```bash
# 查看当前克隆的仓库
ls -la /tmp/github-browser-*

# 清理所有
rm -rf /tmp/github-browser-*
```

## 使用方式

在 Claude Code 中说：

- "浏览 GitHub 仓库 facebook/react"
- "查看 https://github.com/vercel/next.js 的代码结构"
- "探索某个 GitHub 项目"
