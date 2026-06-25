#!/usr/bin/env python3
"""
启动 uni-app dev 模式，首次构建完成后自动剥离 shadow-grey.png。
"""
import subprocess
import sys
import time
from pathlib import Path

VENDOR_REL = "dist/build/mp-weixin/common/vendor.js"
STRIP_SCRIPT = "scripts/strip-shadow-preload.py"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    vendor_path = root / VENDOR_REL

    print("[dev] 启动 uni-app dev 模式...")
    proc = subprocess.Popen(
        ["npx", "uni", "-p", "mp-weixin"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    stripped = False
    try:
        while True:
            line = proc.stdout.readline()
            if line:
                print(line, end="", flush=True)
                # 构建完成时 uni 会输出 "DONE" 或类似标志
                if not stripped and ("DONE" in line or "Build" in line) and vendor_path.exists():
                    content = vendor_path.read_text("utf-8", errors="replace")
                    if "shadow-grey.png" in content:
                        subprocess.run([sys.executable, str(root / STRIP_SCRIPT)], cwd=root)
                        stripped = True
                        print("[dev] shadow-grey.png 已剥离 ✓")

            if proc.poll() is not None:
                break

    except KeyboardInterrupt:
        print("\n[dev] 用户终止")
        proc.terminate()
        return 0

    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
