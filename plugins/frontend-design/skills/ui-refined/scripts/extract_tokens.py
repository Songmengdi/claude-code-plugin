#!/usr/bin/env python3
"""从 batch_get 结果中提取 $-- Design Token。

用法:
  mcporter call pencil.batch_get --args '{"ids": ["anyId"]}' --timeout 120000 > /tmp/pencil_output.json
  python3 scripts/extract_tokens.py /tmp/pencil_output.json
"""
import json, sys

def walk(nodes):
    for n in nodes:
        if not isinstance(n, dict): continue
        name = n.get('name', '')
        if name.startswith('$--'):
            fill = n.get('fill', '')
            print(f"{name}: {fill}")
        walk(n.get('children', []))

data = json.load(open(sys.argv[1]))
walk(data)
