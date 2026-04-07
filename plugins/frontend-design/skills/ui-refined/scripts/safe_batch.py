#!/usr/bin/env python3
"""执行 batch_design 的便捷脚本。

用法:
  python3 scripts/safe_batch.py file.pen 'I("parentId", {"type": "frame", ...})'
  python3 scripts/safe_batch.py file.pen 'U("id", {"content": "new"})'
  python3 scripts/safe_batch.py file.pen 'D("oldId")'

退出码:
  0 - 操作成功
  1 - 操作失败
"""
import subprocess, sys, json, os


def main():
    if len(sys.argv) != 3:
        print("用法: safe_batch.py <file.pen> '<operations>'", file=sys.stderr)
        sys.exit(1)

    file_path = os.path.abspath(sys.argv[1])
    operations = sys.argv[2]

    cmd = ["mcporter", "call", "pencil.batch_design",
           "--args", json.dumps({"filePath": file_path, "operations": operations}, ensure_ascii=False),
           "--timeout", "120000"]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=130)
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
