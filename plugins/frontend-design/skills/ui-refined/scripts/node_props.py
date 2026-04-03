#!/usr/bin/env python3
"""查询指定节点的关键样式属性。

用法:
  mcporter call pencil.batch_get --args '{"ids": ["anyId"]}' --timeout 120000 > /tmp/pencil_output.json
  python3 scripts/node_props.py /tmp/pencil_output.json <node_id> [node_id2 ...]
"""
import json, sys

STYLE_KEYS = ('id', 'name', 'type', 'fill', 'stroke', 'cornerRadius', 'height', 'width', 'padding', 'opacity', 'layout', 'gap')

def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict): continue
        if n.get('id') == tid: return n
        r = find(n.get('children', []), tid)
        if r: return r
    return None

data = json.load(open(sys.argv[1]))
for tid in sys.argv[2:]:
    node = find(data, tid)
    if node:
        props = {k: v for k, v in node.items() if k in STYLE_KEYS}
        print(json.dumps(props, ensure_ascii=False))
    else:
        print(f"Node '{tid}' not found", file=sys.stderr)
