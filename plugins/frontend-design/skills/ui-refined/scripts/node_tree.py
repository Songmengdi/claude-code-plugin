#!/usr/bin/env python3
"""查询指定节点的树结构（轻量，含子节点）。

用法:
  mcporter call pencil.batch_get --args '{"ids": ["anyId"]}' --timeout 120000 > /tmp/pencil_output.json
  python3 scripts/node_tree.py /tmp/pencil_output.json <node_id> [node_id2 ...]
"""
import json, sys

def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict): continue
        if n.get('id') == tid: return n
        r = find(n.get('children', []), tid)
        if r: return r
    return None

def ext(n):
    if not isinstance(n, dict): return None
    return {'id': n['id'], 'type': n.get('type'), 'name': n.get('name'),
            'w': n.get('width'), 'h': n.get('height'),
            'children': [ext(c) for c in n.get('children', []) if isinstance(c, dict)]}

data = json.load(open(sys.argv[1]))
for tid in sys.argv[2:]:
    node = find(data, tid)
    if node:
        print(json.dumps(ext(node), indent=2, ensure_ascii=False))
    else:
        print(f"Node '{tid}' not found", file=sys.stderr)
