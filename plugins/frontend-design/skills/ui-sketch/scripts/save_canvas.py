#!/usr/bin/env python3
"""保存 excalidraw 画布到 JSON 文件。

用法:
  python save_canvas.py <name>              # 保存到 <项目根目录>/ui-sketch/<name>.json
  python save_canvas.py <name> --path <dir> # 保存到指定目录

示例:
  python save_canvas.py blog                # → ./ui-sketch/blog.json
  python save_canvas.py blog --path ./sketches  # → ./sketches/blog.json
"""

import json
import os
import subprocess
import sys

DEFAULT_DIR = "ui-sketch"


def get_elements():
    """从画布获取全量元素数据。"""
    result = subprocess.run(
        ["mcporter", "call", "excalidraw.get_resource",
         "--args", json.dumps({"resource": "elements"})],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"获取画布失败: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(result.stdout)
    elements = data["elements"]
    print(f"获取到 {len(elements)} 个元素")
    from collections import Counter
    for t, c in Counter(e["type"] for e in elements).items():
        print(f"  {t}: {c}")
    return elements


def main():
    if len(sys.argv) < 2:
        print("用法: python save_canvas.py <name> [--path <dir>]", file=sys.stderr)
        sys.exit(1)

    name = sys.argv[1]
    save_dir = DEFAULT_DIR
    if "--path" in sys.argv:
        idx = sys.argv.index("--path")
        save_dir = sys.argv[idx + 1]

    if not name.endswith(".json"):
        name += ".json"

    output_path = os.path.join(save_dir, name)
    os.makedirs(save_dir, exist_ok=True)

    elements = get_elements()
    if not elements:
        print("画布为空，未保存。", file=sys.stderr)
        sys.exit(1)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(elements, f, ensure_ascii=False, indent=2)
    print(f"已保存到 {output_path}")


if __name__ == "__main__":
    main()
