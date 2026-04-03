#!/usr/bin/env python3
"""从 JSON 文件恢复 excalidraw 画布。

用法:
  python restore_canvas.py <name>              # 从 <项目根目录>/ui-sketch/<name>.json 恢复
  python restore_canvas.py <name> --path <dir> # 从指定目录恢复
  python restore_canvas.py <name> --no-clear   # 追加恢复，不清空画布

示例:
  python restore_canvas.py blog                # → 读取 ./ui-sketch/blog.json
  python restore_canvas.py blog --no-clear     # 追加，不删除现有元素
"""

import json
import os
import subprocess
import sys

DEFAULT_DIR = "ui-sketch"

READONLY_FIELDS = {
    "id", "seed", "version", "versionNonce", "isDeleted", "boundElements",
    "updated", "link", "locked", "syncedAt", "source", "syncTimestamp",
    "index", "frameId", "lastCommittedPoint", "startBinding", "endBinding",
    "startArrowhead", "endArrowhead",
}

BATCH_SIZE = 25


def clean_element(e):
    """清理单个元素，去除只读字段并修正类型。"""
    clean = {k: v for k, v in e.items() if k not in READONLY_FIELDS}
    if "fontFamily" in clean and not isinstance(clean["fontFamily"], str):
        clean["fontFamily"] = str(clean["fontFamily"])
    if "points" in clean:
        clean["points"] = [{"x": p[0], "y": p[1]} for p in clean["points"]]
    return clean


def parse_mcporter_output(stdout):
    """解析 mcporter 输出，跳过前缀文本和尾部内容，提取 JSON。"""
    brace_idx = stdout.find("{")
    if brace_idx < 0:
        return None
    # 找到匹配的最后一个 }
    depth = 0
    end_idx = brace_idx
    for i in range(brace_idx, len(stdout)):
        if stdout[i] == "{":
            depth += 1
        elif stdout[i] == "}":
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break
    return json.loads(stdout[brace_idx:end_idx])


def clear_canvas():
    """清空画布上所有元素。"""
    result = subprocess.run(
        ["mcporter", "call", "excalidraw.clear_canvas", "--args", "{}"],
        capture_output=True, text=True
    )
    resp = parse_mcporter_output(result.stdout)
    count = resp["deletedCount"] if resp else 0
    print(f"画布已清空（删除 {count} 个元素）")


def restore_elements(elements):
    """分批恢复元素到画布。"""
    cleaned = [clean_element(e) for e in elements]
    batches = [cleaned[i:i + BATCH_SIZE] for i in range(0, len(cleaned), BATCH_SIZE)]
    print(f"分为 {len(batches)} 批恢复（每批最多 {BATCH_SIZE} 个）")
    for i, batch in enumerate(batches):
        result = subprocess.run(
            ["mcporter", "call", "excalidraw.batch_create_elements",
             "--args", json.dumps({"elements": batch})],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"批次 {i} 失败: {result.stdout[:300]}", file=sys.stderr)
            sys.exit(1)
        resp = parse_mcporter_output(result.stdout)
        if resp is None:
            print(f"批次 {i}: 已发送（无法解析返回值）")
        else:
            print(f"  批次 {i}: {resp['count']} 个元素已恢复")


def main():
    if len(sys.argv) < 2:
        print("用法: python restore_canvas.py <name> [--path <dir>] [--no-clear]", file=sys.stderr)
        sys.exit(1)

    name = sys.argv[1]
    load_dir = DEFAULT_DIR
    no_clear = "--no-clear" in sys.argv
    if "--path" in sys.argv:
        idx = sys.argv.index("--path")
        load_dir = sys.argv[idx + 1]

    if not name.endswith(".json"):
        name += ".json"

    input_path = os.path.join(load_dir, name)
    with open(input_path, "r", encoding="utf-8") as f:
        elements = json.load(f)
    print(f"读取到 {len(elements)} 个元素（来自 {input_path}）")

    if not no_clear:
        clear_canvas()
    restore_elements(elements)
    print("恢复完成")


if __name__ == "__main__":
    main()
