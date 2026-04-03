#!/usr/bin/env python3
"""查看指定节点的直接子节点 ID 列表。

用法:
  mcporter call pencil.batch_get --args '{"ids": ["anyId"]}' --timeout 120000 > /tmp/pencil_output.json
  python3 scripts/node_children.py /tmp/pencil_output.json <node_id>
"""
import json, sys

def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict): continue
        if n.get('id') == tid: return n
        r = find(n.get('children', []), tid)
        if r: return r
    return None

data = json.load(open(sys.argv[1]))
node = find(data, sys.argv[2])
if not node:
    print(f"Node '{sys.argv[2]}' not found", file=sys.stderr)
    sys.exit(1)

children = node.get('children', [])
print(f"{node.get('name', node['id'])} ({len(children)} children):")
for c in children[:30]:
    if isinstance(c, dict):
        print(f"  {c['id']}  {c.get('name', '')}")
if len(children) > 30:
    print(f"  ... +{len(children) - 30} more")
