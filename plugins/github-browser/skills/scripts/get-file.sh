#!/bin/bash

# 从 GitHub 仓库获取单个文件内容
# 用法: ./get-file.sh <owner> <repo> <file-path> [branch]
# 说明: 文件<=300行直接打印到控制台，>300行保存到/tmp并显示信息

if [ $# -lt 3 ]; then
  echo "用法: $0 <owner> <repo> <file-path> [branch]"
  echo "示例: $0 supermemoryai opencode-supermemory scripts/release.sh"
  echo "示例: $0 supermemoryai opencode-supermemory src/index.ts main"
  exit 1
fi

OWNER="$1"
REPO="$2"
FILE_PATH="$3"
BRANCH=${4:-"main"}
LINE_LIMIT=300

echo "获取: ${OWNER}/${REPO}/${BRANCH}/${FILE_PATH}"

# 优先使用 raw.githubusercontent.com（最快）
RAW_URL="https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/${FILE_PATH}"
content=$(curl -s -f "${RAW_URL}" 2>&1)

if [ -n "$content" ]; then
  LINES=$(echo "$content" | wc -l)
  
  if [ "$LINES" -le "$LINE_LIMIT" ]; then
    echo "$content"
    echo "✓ 成功获取 (${LINES} lines)"
    exit 0
  else
    TEMP_FILE="/tmp/${FILE_PATH##*/}.$$"
    echo "$content" > "$TEMP_FILE"
    SIZE=$(wc -c < "$TEMP_FILE")
    echo "✓ 文件较大，已保存到: $TEMP_FILE"
    echo "  大小: ${SIZE} bytes, 行数: ${LINES}"
    exit 0
  fi
fi

# 尝试使用 GitHub API（备选）
API_URL="https://api.github.com/repos/${OWNER}/${REPO}/contents/${FILE_PATH}?ref=${BRANCH}"
api_response=$(curl -s -f "${API_URL}" 2>&1)

if [ $? -eq 0 ]; then
  if ! echo "$api_response" | grep -q '"message"'; then
    content=$(echo "$api_response" | jq -r '.content' | base64 -d 2>/dev/null)
    if [ -n "$content" ]; then
      LINES=$(echo "$content" | wc -l)
      
      if [ "$LINES" -le "$LINE_LIMIT" ]; then
        echo "$content"
        echo "✓ 成功获取 (${LINES} lines)"
        exit 0
      else
        TEMP_FILE="/tmp/${FILE_PATH##*/}.$$"
        echo "$content" > "$TEMP_FILE"
        SIZE=$(wc -c < "$TEMP_FILE")
        echo "✓ 文件较大，已保存到: $TEMP_FILE"
        echo "  大小: ${SIZE} bytes, 行数: ${LINES}"
        exit 0
      fi
    fi
  fi
fi

echo "✗ 无法获取文件内容"
exit 1
