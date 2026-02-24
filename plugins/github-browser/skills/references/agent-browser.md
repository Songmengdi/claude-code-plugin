# agent-browser 直接操作指南

当脚本工具（get-info.sh、get-tree.py、get-file.sh）不可用时，使用 agent-browser 直接操作。

## 基本操作

```bash
# 打开仓库
agent-browser open https://github.com/owner/repo
agent-browser wait 2000

# 获取页面快照
agent-browser snapshot -i

# 关闭浏览器
agent-browser close
```

## 导航命令

```bash
# 打开 URL
agent-browser open <url>

# 后退/前进
agent-browser back
agent-browser forward

# 刷新
agent-browser reload
```

## 获取信息

```bash
# 可访问性快照（包含元素引用）
agent-browser snapshot -i

# 截图
agent-browser screenshot /path/to.png
agent-browser screenshot --full /path/to.png

# 获取 URL
agent-browser get url
```

## 交互操作

```bash
# 点击元素引用
agent-browser click @ref

# 填写输入框
agent-browser fill @selector "text"

# 按键
agent-browser press Enter
agent-browser press Tab

# 滚动
agent-browser scroll down
agent-browser scroll up
```

## 查找元素

```bash
# 按角色查找
agent-browser find role button click

# 按文本查找
agent-browser find text "Click me" click

# 按占位符查找
agent-browser find placeholder "Search" fill "query"
```

## 导航文件

```bash
# 打开仓库
agent-browser open https://github.com/owner/repo
agent-browser wait 2000

# 获取快照找到引用
agent-browser snapshot -i > snapshot.txt

# 使用 @ref 点击目录或文件
agent-browser click @ref_number
agent-browser wait 1000

# 返回上级
agent-browser back
```

## 获取文件内容

```bash
# 方法 1: 使用 curl（推荐）
curl -s https://raw.githubusercontent.com/owner/repo/main/file.js

# 方法 2: 使用浏览器
agent-browser open https://github.com/owner/repo/blob/main/file.js
agent-browser wait 2000
agent-browser screenshot --full screenshot.png
```
