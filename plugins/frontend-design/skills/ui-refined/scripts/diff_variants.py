#!/usr/bin/env python3
"""对比多个组件变体的属性差异。

用法:
  mcporter call pencil.batch_get --args '{"ids": ["anyId"]}' --timeout 120000 > /tmp/pencil_output.json
  python3/scripts/diff_variants.py /tmp/pencil_output.json <node_id1> <node_id2> [...]
"""
import json, sys

STYLE_KEYS = ('fill', 'stroke', 'cornerRadius', 'height', 'width', 'padding', 'opacity', 'layout', 'gap')

def find(nodes, tid):
    for n in nodes:
        if not isinstance(n, dict): continue
        if n.get('id') == tid: return n
        r = find(n.get('children', []), tid)
        if r: return r
    return None

data = json.load(open(sys.argv[1]))
results = []
for tid in sys.argv[2:]:
    node = find(data, tid)
    if node:
        props = {k: v for k, v in node.items() if k in STYLE_KEYS}
        results.append({'name': node.get('name', tid), **props})
    else:
        print(f"Node '{tid}' not found", file=sys.stderr)

print(json.dumps(results, indent=2, ensure_ascii=False))
