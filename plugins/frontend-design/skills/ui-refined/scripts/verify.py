#!/usr/bin/env python3
"""批量验证节点状态，一次调用完成操作后检查。

用法:
  # 验证节点存在
  python3 scripts/verify.py file.pen --exists id1 id2 id3

  # 验证节点不存在（已删除）
  python3 scripts/verify.py file.pen --missing id1 id2

  # 验证子节点顺序
  python3 scripts/verify.py file.pen --order parentId id1 id2 id3

  # 验证属性值
  python3 scripts/verify.py file.pen --prop id1 fill '$$--accent' --prop id2 layout 'vertical'

  # 混合使用
  python3 scripts/verify.py file.pen --exists newId --missing oldId --order parentId a b c

退出码:
  0 - 全部通过
  1 - 存在失败项
"""
import json, sys, argparse


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


def check_exists(root, ids, expected=True):
    results = []
    for tid in ids:
        node = find(root, tid)
        found = node is not None
        ok = found == expected
        label = "EXISTS" if expected else "MISSING"
        status = "✓" if ok else "✗"
        results.append(ok)
        if not ok:
            name = node.get("name", "") if node else ""
            print(f"  {status} {tid} {label} — actual: {'found' + (f' ({name})' if name else '') if found else 'not found'}")
    return all(results)


def check_order(root, parent_id, expected_ids):
    parent = find(root, parent_id)
    if not parent:
        print(f"  ✗ Parent '{parent_id}' not found")
        return False
    actual = [c["id"] for c in parent.get("children", []) if isinstance(c, dict)]
    # 只检查 expected_ids 在 actual 中的相对顺序
    positions = {}
    for i, eid in enumerate(expected_ids):
        if eid in actual:
            positions[eid] = actual.index(eid)
        else:
            print(f"  ✗ {eid} not in children of {parent_id}")
            return False
    ordered = all(positions[expected_ids[i]] < positions[expected_ids[i + 1]] for i in range(len(expected_ids) - 1))
    if ordered:
        print(f"  ✓ {parent_id} order: {' > '.join(expected_ids)}")
    else:
        print(f"  ✗ {parent_id} order mismatch — expected: {' > '.join(expected_ids)}, actual: {' > '.join(actual)}")
    return ordered


def check_prop(root, node_id, prop, value):
    node = find(root, node_id)
    if not node:
        print(f"  ✗ {node_id} not found")
        return False
    actual = node.get(prop)
    ok = str(actual) == value
    status = "✓" if ok else "✗"
    if not ok:
        print(f"  {status} {node_id}.{prop} — expected: {value}, actual: {actual}")
    return ok


def main():
    parser = argparse.ArgumentParser(description="批量验证节点状态")
    parser.add_argument("file", help=".pen 文件路径")
    parser.add_argument("--exists", nargs="+", help="验证节点存在")
    parser.add_argument("--missing", nargs="+", help="验证节点不存在")
    parser.add_argument("--order", nargs="+", help="验证子节点顺序: PARENT_ID ID1 ID2 ...")
    parser.add_argument("--prop", nargs=3, action="append", metavar=("ID", "PROP", "VALUE"), help="验证属性值 (可多次使用)")
    args = parser.parse_args()

    if not args.exists and not args.missing and not args.order and not args.prop:
        print("错误：至少指定一个检查项 (--exists / --missing / --order / --prop)", file=sys.stderr)
        sys.exit(1)

    with open(args.file) as f:
        raw = json.load(f)
    # 兼容两种格式：.pen 文件 {"children": [...]} 和 batch_get 输出 [...]
    if isinstance(raw, list):
        root = raw
    else:
        root = raw.get("children", [])

    all_ok = True
    if args.exists:
        print(f"Checking exists: {args.exists}")
        if not check_exists(root, args.exists, expected=True):
            all_ok = False
    if args.missing:
        print(f"Checking missing: {args.missing}")
        if not check_exists(root, args.missing, expected=False):
            all_ok = False
    if args.order:
        parent_id = args.order[0]
        expected = args.order[1:]
        print(f"Checking order: {parent_id} → {' > '.join(expected)}")
        if not check_order(root, parent_id, expected):
            all_ok = False
    if args.prop:
        print(f"Checking props: {len(args.prop)} items")
        for node_id, prop, value in args.prop:
            if not check_prop(root, node_id, prop, value):
                all_ok = False

    if all_ok:
        print("All checks passed ✓")
    else:
        print("Some checks failed ✗")
        sys.exit(1)


if __name__ == "__main__":
    main()
