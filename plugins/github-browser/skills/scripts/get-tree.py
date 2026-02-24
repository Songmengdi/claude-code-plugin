#!/usr/bin/env python3

import subprocess
import sys
import argparse
from typing import List, Dict, Optional
import json
import re

def run_browser_command(cmd: List[str]) -> str:
    """执行 agent-browser 命令并返回输出"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {' '.join(cmd)}")
        print(f"错误: {e.stderr}")
        sys.exit(1)

def get_tree_json(path: str = '', base_level: int = 1, max_level: Optional[int] = None) -> Optional[Dict]:
    """获取树形JSON结构
    
    Args:
        path: 指定的路径（如 'src'），为空则获取全部
        base_level: 起始层级（path=''时为1，path='src'时为2）
        max_level: 最大层级限制
    
    Returns:
        树形结构或None
    """
    js_code = f'''(function(){{
        const treeitems = document.querySelectorAll("[role=treeitem]");
        let items = [];
        
        treeitems.forEach((item, i) => {{
            const labelId = item.getAttribute("aria-labelledby");
            const labelEl = document.getElementById(labelId);
            const name = labelEl ? labelEl.querySelector("span")?.textContent.trim() : "";
            const level = parseInt(item.getAttribute("aria-level") || "1");
            const expanded = item.getAttribute("aria-expanded");
            const isDir = item.hasAttribute("aria-expanded");
            
            items.push({{ 
                name, 
                level, 
                isDir, 
                expanded,
                index: i 
            }});
        }});
        
        // 过滤目标路径的节点
        let filteredItems = [];
        if('{path}') {{
            // 查找path节点
            let pathParts = '{path}'.split('/');
            let started = false;
            let pathLevel = 0;
            let pathIndex = -1;
            
            for(let i = 0; i < items.length; i++) {{
                let item = items[i];
                if(item.name === pathParts[pathParts.length - 1] && item.level === {base_level} - 1) {{
                    started = true;
                    pathLevel = item.level;
                    pathIndex = i;
                }}
                
                if(started) {{
                    // 检查是否超出最大层级
                    if({max_level} && item.level > {max_level}) {{
                        break;
                    }}
                    
                    filteredItems.push(item);
                    
                    // 如果回到同级或更低，且不是起始节点，则停止
                    if(item.level <= pathLevel && item.index > pathIndex) {{
                        filteredItems.pop();
                        break;
                    }}
                }}
            }}
        }} else {{
            // 获取全部
            for(let i = 0; i < items.length; i++) {{
                let item = items[i];
                if({max_level} && item.level > {max_level}) {{
                    break;
                }}
                filteredItems.push(item);
            }}
        }}
        
        // 构建树形结构
        let root = {{ children: [] }};
        let stack = [root];
        
        for(let i = 0; i < filteredItems.length; i++) {{
            let item = filteredItems[i];
            
            // 找到父级
            while(stack.length > 1 && stack[stack.length - 1].level >= item.level) {{
                stack.pop();
            }}
            
            let node = {{
                name: item.name,
                level: item.level,
                isDir: item.isDir,
                expanded: item.expanded === "true",
                children: []
            }};
            
            stack[stack.length - 1].children.push(node);
            stack.push(node);
        }}
        
        return root.children;
    }})()'''
    
    result = run_browser_command(['agent-browser', 'eval', js_code])
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return None

def get_unexpanded_dirs(tree: List[Dict], max_level: int) -> List[Dict]:
    """获取未展开且需要展开的目录
    
    Args:
        tree: 树形结构
        max_level: 最大层级
    
    Returns:
        未展开目录列表
    """
    unexpanded = []
    
    def traverse(nodes: List[Dict]):
        for node in nodes:
            if node['isDir'] and not node['expanded']:
                if node['level'] < max_level:
                    unexpanded.append(node)
            traverse(node.get('children', []))
    
    traverse(tree)
    return unexpanded

def expand_directory_by_name(name: str) -> None:
    """通过名称展开目录"""
    snapshot = run_browser_command(['agent-browser', 'snapshot', '-i'])
    match = re.search(rf'treeitem "{re.escape(name)}" \[ref=(\w+)\]', snapshot)
    if match:
        ref = match.group(1)
        run_browser_command(['agent-browser', 'click', f'@{ref}'])
        run_browser_command(['agent-browser', 'wait', '1000'])

def expand_to_depth(path: str, base_level: int, max_depth: int) -> List[Dict]:
    """递归展开到指定深度
    
    Args:
        path: 指定路径
        base_level: 起始层级
        max_depth: 最大深度
    
    Returns:
        最终的树形结构
    """
    max_level = base_level + max_depth - 1
    
    while True:
        # 获取当前树
        tree = get_tree_json(path, base_level, max_level)
        if not tree or not isinstance(tree, list):
            print("无法获取目录树")
            return []
        
        # 查找未展开的目录
        unexpanded_dirs = get_unexpanded_dirs(tree if isinstance(tree, list) else [tree], max_level)
        
        if not unexpanded_dirs:
            # 所有需要展开的目录都已展开
            break
        
        # 展开所有未展开的目录
        for dir_node in unexpanded_dirs:
            print(f"展开 {dir_node['name']}...")
            expand_directory_by_name(dir_node['name'])
    
    return tree

def print_tree(tree: List[Dict], base_level: int) -> None:
    """打印目录树"""
    def print_node(node: Dict, prefix: str, is_last: bool):
        connector = '└── ' if is_last else '├── '
        name = node['name']
        if node['isDir']:
            name += '/'
        print(f"{prefix}{connector}{name}")
        
        children = node.get('children', [])
        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            new_prefix = prefix + ('    ' if is_last else '│   ')
            print_node(child, new_prefix, is_last_child)
    
    for i, node in enumerate(tree):
        is_last = i == len(tree) - 1
        print_node(node, '', is_last)

def main():
    parser = argparse.ArgumentParser(description='获取 GitHub 项目的目录树结构')
    parser.add_argument('owner', help='GitHub 仓库所有者')
    parser.add_argument('repo', help='GitHub 仓库名称')
    parser.add_argument('deep', type=int, help='目录树深度')
    parser.add_argument('path', nargs='?', default='', help='起始路径（可选，默认为根目录）')
    
    args = parser.parse_args()
    
    # 计算起始层级
    path_parts = args.path.split('/') if args.path else []
    base_level = 1 + len(path_parts)
    
    # 构造 URL
    if args.path:
        url = f"https://github.com/{args.owner}/{args.repo}/tree/main/{args.path}"
    else:
        url = f"https://github.com/{args.owner}/{args.repo}/blob/main/README.md"
    
    print(f"正在访问: {url}")
    
    # 打开页面
    run_browser_command(['agent-browser', 'open', url])
    run_browser_command(['agent-browser', 'wait', '1000'])
    
    # 检查是否需要展开文件树（只有无path时）
    if not args.path:
        snapshot = run_browser_command(['agent-browser', 'snapshot', '-i'])
        if 'Expand file tree' in snapshot:
            match = re.search(r'button "Expand file tree" \[ref=(\w+)\]', snapshot)
            if match:
                expand_ref = match.group(1)
                run_browser_command(['agent-browser', 'click', f'@{expand_ref}'])
                run_browser_command(['agent-browser', 'wait', '1000'])
    
    # 递归展开到指定深度
    tree = expand_to_depth(args.path, base_level, args.deep)
    
    if not tree:
        print("无法获取文件树")
        run_browser_command(['agent-browser', 'close'])
        sys.exit(1)
    
    # 打印目录树
    print("\n目录树:")
    print_tree(tree, base_level)
    
    # 关闭浏览器
    run_browser_command(['agent-browser', 'close'])

if __name__ == '__main__':
    main()
