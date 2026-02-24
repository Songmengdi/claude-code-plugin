# Prompt Optimizer Plugin

基于任务执行经验优化命令、SKILL、Agent的提示词，让提示词在后续使用中更好地辅助完成工作。

## 功能

- 分析现有提示词的质量和效果
- 根据历史执行经验生成优化建议
- 支持命令、SKILL、Agent提示词的优化
- 直接修改文件应用优化
- 记录优化历史以便追踪改进

## 组件

- **Commands (2)**: `optimize-prompt`, `optimize-history`
- **Agents (1)**: `prompt-analyzer` - 分析提示词质量
- **Skills (1)**: `prompt-optimization` - 提示词优化知识库

## 安装

### 方法1: 项目本地安装

将插件复制到项目的 `.claude-plugin/` 目录：

```bash
cp -r prompt-optimizer /path/to/your/project/.claude-plugin/
```

### 方法2: 临时测试

使用 `--plugin-dir` 选项临时加载插件：

```bash
cc --plugin-dir /path/to/prompt-optimizer
```

### 方法3: 全局安装

复制到全局插件目录：

```bash
cp -r prompt-optimizer ~/.claude/plugins/
```

## 使用

### 优化提示词

优化指定文件中的提示词：

```bash
/optimize-prompt commands/review.md
/optimize-prompt agents/code-reviewer.md
/optimize-prompt skills/api-testing/SKILL.md
```

命令会：
1. 分析提示词质量
2. 生成优化建议
3. 直接修改文件应用优化
4. 记录优化历史

### 查看优化历史

显示所有优化记录的摘要：

```bash
/optimize-history
```

显示详细记录：

```bash
/optimize-history --detail
```

查看特定文件的优化历史：

```bash
/optimize-history --file commands/review.md
```

### 使用 Agent 分析

Agent 会在以下场景自动触发：
- 用户要求分析提示词质量
- 用户请求提示词优化建议
- 用户想要改进命令/SKILL/Agent

## 文件结构

```
prompt-optimizer/
├── .claude-plugin/
│   └── plugin.json          # 插件清单
├── agents/
│   └── prompt-analyzer.md    # 提示词分析 Agent
├── commands/
│   ├── optimize-prompt.md    # 优化命令
│   └── optimize-history.md   # 历史查看命令
├── skills/
│   └── prompt-optimization/
│       ├── SKILL.md         # 优化知识库
│       ├── references/
│       │   ├── patterns.md  # 常见模式
│       │   └── techniques.md # 高级技巧
│       └── examples/
│           └── before-after.md # 优化示例
├── .gitignore
└── README.md
```

## 版本

- **Version**: 0.1.0
- **Author**: User
