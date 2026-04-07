#!/usr/bin/env python3
"""根据 node ID 列表自动排列节点间距。

用法:
  # 单组：所有节点紧凑排列
  python3 scripts/auto_layout.py file.pen --nodes id1 id2 id3

  # 多组：逗号分隔每组 ID，组间有更大间距
  python3 scripts/auto_layout.py file.pen --groups "id1,id2,id3" "id4,id5"

  # 指定起始 y 和间距
  python3 scripts/auto_layout.py file.pen --nodes id1 id2 --start-y 2460 --gap 24 --group-gap 60

输出 batch_design 命令，可直接执行。
"""

import json
import sys
import argparse

LINE_HEIGHT_RATIO = 1.4


def find_node(root: list, tid: str) -> dict | None:
    for n in root:
        if not isinstance(n, dict):
            continue
        if n.get("id") == tid:
            return n
        r = find_node(n.get("children", []), tid)
        if r:
            return r
    return None


def estimate_height(node: dict) -> float:
    if not node or not isinstance(node, dict):
        return 0

    h = node.get("height")
    if isinstance(h, (int, float)) and h > 0:
        return h

    layout = node.get("layout", "")
    children = [c for c in node.get("children", []) if isinstance(c, dict)]

    if not children:
        if node.get("type") == "text" and node.get("content"):
            return node.get("fontSize", 14) * LINE_HEIGHT_RATIO
        return 0

    pad = node.get("padding", [0, 0, 0, 0])
    if isinstance(pad, (int, float)):
        pad_top = pad_bottom = pad
    elif len(pad) == 2:
        pad_top = pad_bottom = pad[0]
    else:
        pad_top, _, pad_bottom, _ = pad[0], pad[1], pad[2], pad[3]

    gap = node.get("gap", 0)

    if layout == "vertical":
        children_h = sum(estimate_height(c) for c in children)
        total_gap = gap * (len(children) - 1) if len(children) > 1 else 0
        return children_h + total_gap + pad_top + pad_bottom
    elif layout == "horizontal":
        return max(estimate_height(c) for c in children) + pad_top + pad_bottom
    else:
        max_bottom = 0
        for c in children:
            bottom = c.get("y", 0) + estimate_height(c)
            if bottom > max_bottom:
                max_bottom = bottom
        return max_bottom + pad_top + pad_bottom


def main():
    parser = argparse.ArgumentParser(description="根据 node ID 自动排列间距")
    parser.add_argument("file", help=".pen 文件路径")
    parser.add_argument("--nodes", nargs="+", help="单组 node ID 列表")
    parser.add_argument("--groups", nargs="+", help="多组，每组用逗号分隔 ID，如 'id1,id2' 'id3,id4'")
    parser.add_argument("--start-y", type=int, default=0, help="起始 y 坐标 (默认 0)")
    parser.add_argument("--gap", type=int, default=24, help="组内间距 (px, 默认 24)")
    parser.add_argument("--group-gap", type=int, default=60, help="组间距 (px, 默认 60)")
    args = parser.parse_args()

    if not args.nodes and not args.groups:
        print("错误：必须指定 --nodes 或 --groups", file=sys.stderr)
        sys.exit(1)

    with open(args.file) as f:
        data = json.load(f)

    root = data.get("children", [])

    # 构建分组列表
    groups: list[list[str]] = []
    if args.nodes:
        groups.append(args.nodes)
    if args.groups:
        for g in args.groups:
            groups.append([nid.strip() for nid in g.split(",") if nid.strip()])

    # 计算布局
    y = args.start_y
    operations = []

    for gi, group_ids in enumerate(groups):
        for nid in group_ids:
            node = find_node(root, nid)
            if not node:
                print(f"警告：未找到节点 {nid}", file=sys.stderr)
                continue
            h = estimate_height(node)
            operations.append(f'U("{nid}", {{"y": {round(y)}}})')
            y += h + args.gap

        # 最后一组不加组间距
        if gi < len(groups) - 1:
            y = y - args.gap + args.group_gap

    if not operations:
        print("没有有效的节点需要排列", file=sys.stderr)
        sys.exit(1)

    # 分批输出
    batch_size = 10
    for i in range(0, len(operations), batch_size):
        batch = operations[i : i + batch_size]
        ops_str = "\\n".join(batch)
        print(f"# 批次 {i // batch_size + 1} ({len(batch)} 个操作)")
        print(f'mcporter call pencil.batch_design --args \'{{"filePath": "{args.file}", "operations": "{ops_str}"}}\' --timeout 120000')
        print()

    print(f"# 共 {len(operations)} 个节点，y={args.start_y} → {round(y - args.gap)}", file=sys.stderr)


if __name__ == "__main__":
    main()
