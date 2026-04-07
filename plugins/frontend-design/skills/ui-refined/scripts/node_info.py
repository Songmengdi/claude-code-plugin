#!/usr/bin/env python3
"""节点摘要：快速查看节点的关键信息（类型、尺寸、布局、子节点数、父路径）。

支持一次查询多个节点，减少重复读取文件。

用法:
  python3 scripts/node_info.py file.pen id1
  python3 scripts/node_info.py file.pen id1 id2 id3
"""
import json, sys


def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict):
            continue
        if n.get("id") == tid:
            return n
        r = find(n.get("children", []), tid)
        if r:
            return r
    return None


def find_parent_path(nodes, tid, path=None):
    if path is None:
        path = []
    for n in nodes:
        if not isinstance(n, dict):
            continue
        if n.get("id") == tid:
            return path
        r = find_parent_path(n.get("children", []), tid, path + [f"{n['id']}({n.get('name', '')})"])
        if r is not None:
            return r
    return None


def summarize(node, data):
    children = node.get("children", [])
    child_ids = [c["id"] for c in children if isinstance(c, dict)]
    parent_path = find_parent_path(data.get("children", []), node["id"])
    return {
        "id": node["id"],
        "name": node.get("name", ""),
        "type": node.get("type"),
        "width": node.get("width"),
        "height": node.get("height"),
        "layout": node.get("layout", "none"),
        "fill": node.get("fill"),
        "children_count": len(child_ids),
        "children": child_ids[:10],
        "parent_path": " > ".join(parent_path) if parent_path else "(root)",
    }


def main():
    if len(sys.argv) < 3:
        print("用法: python3 scripts/node_info.py file.pen id1 [id2 ...]", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        data = json.load(f)

    for tid in sys.argv[2:]:
        node = find(data.get("children", []), tid)
        if node:
            info = summarize(node, data)
            print(json.dumps(info, indent=2, ensure_ascii=False))
        else:
            print(f"Node '{tid}' not found", file=sys.stderr)


if __name__ == "__main__":
    main()
