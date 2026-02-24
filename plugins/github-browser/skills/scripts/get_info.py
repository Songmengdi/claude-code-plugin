#!/usr/bin/env python3
import subprocess
import sys
import re
import time

def run_agent_browser(cmd):
    """运行 agent-browser 命令并返回输出"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def get_repo_info(url):
    """获取代码库信息"""
    # 打开浏览器
    run_agent_browser(f'agent-browser open {url}')
    
    snapshot = run_agent_browser("agent-browser snapshot")
    
    # 获取名称 ref (查找第一个 heading level=1)
    name_ref = re.search(r'- heading "[^"]*" \[ref=(e\d+)\] \[level=1\]', snapshot)
    name = ""
    if name_ref:
        name = run_agent_browser(f"agent-browser get text @{name_ref.group(1)}")
    
    # 获取描述 (直接从 article 中获取)
    description = run_agent_browser("agent-browser eval \"document.querySelector('article').querySelector('p').textContent.trim()\"")
    
    # 获取默认分支 ref (查找包含 branch 的按钮)
    branch_ref = re.search(r'- button "[^"]*branch[^"]*" \[ref=(e\d+)\]:', snapshot)
    default_branch = ""
    if branch_ref:
        default_branch = run_agent_browser(f"agent-browser get text @{branch_ref.group(1)}")
    
    # 获取 Languages 信息 - 通过快照解析
    languages = []
    
    # 从快照中找到 Languages heading 的位置
    lang_heading_match = re.search(r'- heading "Languages" \[ref=(e\d+)\] \[level=2\]', snapshot)
    if lang_heading_match:
        lang_start = lang_heading_match.end()
        # 找到 Languages heading 后面的 listitem 中的链接
        pattern = r'- link "[^"]+%\s*[^"]*" \[ref=(e\d+)\]:'
        for match in re.finditer(pattern, snapshot[lang_start:]):
            lang_ref = match.group(1)
            lang_text = run_agent_browser(f"agent-browser get text @{lang_ref}")
            if lang_text.strip():
                languages.append(' '.join(lang_text.strip().split()))
            # 只取前3个语言
            if len(languages) >= 3:
                break
    
    languages_str = ", ".join(languages)
    
    tags_url = url + "/tags"
    run_agent_browser(f'agent-browser --headed open {tags_url}')
    time.sleep(2)  # 等待页面加载
    
    # 获取 tag 标题 ref
    tags_snapshot = run_agent_browser("agent-browser snapshot")
    tag_title_ref = re.search(r'- heading "v[0-9.]+" \[ref=(e\d+)\] \[level=2\]', tags_snapshot)
    latest_tag = ""
    if tag_title_ref:
        latest_tag = run_agent_browser(f"agent-browser get text @{tag_title_ref.group(1)}")
    
    run_agent_browser("agent-browser close")
    
    return {
        "name": name,
        "description": description,
        "languages": languages_str,
        "default_branch": default_branch,
        "latest_tag": latest_tag
    }

def print_repo_info(info):
    """按照指定格式打印信息"""
    print("**名称：**", info["name"])
    print()
    print("**描述：**", info["description"])
    print()
    print("**语言：**", info["languages"])
    print()
    print("**默认分支：**", info["default_branch"])
    print()
    print("**最新 tag：**", info["latest_tag"])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python get_info.py <owner> <repo>")
        sys.exit(1)
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    url = f"https://github.com/{owner}/{repo}"
    
    info = get_repo_info(url)
    print_repo_info(info)
