#!/usr/bin/env python3
"""
构建后脚本：移除 vendor.js 中 uni-app 框架内置的 shadow-grey.png 预加载。

此预加载是 uni-app 的 <image> 组件默认占位图，本项目未使用 <image> 标签，
且在微信开发者工具中会因 CDN 请求超时报错 "Error: timeout"，阻塞调试预览。

结构分析：
  !function(){if(h(wx.preloadAssets)){
    const e=String.fromCharCode(99,100,110,49,...);  // e = "cdn1.dcloud.net.cn"
    etTimeout(()=>{                                    // s 被 minifier 吃掉
      wx.preloadAssets({data:[{type:"image",src:"https://"+e+"/.../img/shadow-grey.png"}]})
    },3e3)
  }}()

移除范围：从 !function 到 ()) 后的逗号（wx.createApp 前）。
"""
import sys
from pathlib import Path

VENDOR_REL = "dist/build/mp-weixin/common/vendor.js"


def main() -> int:
    vendor_path = Path(__file__).resolve().parent.parent / VENDOR_REL

    if not vendor_path.exists():
        print(f"[strip] {vendor_path} not found, skipping")
        return 0

    content = vendor_path.read_text("utf-8")
    marker = "shadow-grey.png"
    idx = content.find(marker)

    if idx == -1:
        print("[strip] shadow-grey.png not found - already clean")
        return 0

    # --- 找 IIFE 起始：!function ---
    iife_start = content.rfind("!function", idx - 500, idx)
    if iife_start == -1:
        print("[strip] !function not found before shadow-grey.png, trying fallback...")
        return 1

    # --- 找 IIFE 结束：前一个逗号（wx.createApp 前的那个） ---
    ca_marker = "wx.createApp"
    ca_idx = content.find(ca_marker, idx)
    if ca_idx == -1:
        print(f"[strip] {ca_marker} not found after shadow-grey.png")
        return 1

    # ca_idx 指向 'w' of wx.createApp，其前一个字符应为逗号
    if content[ca_idx - 1] == ",":
        iife_end = ca_idx  # 包含这个逗号一起删掉
    else:
        # 保底：回退到 IIFE 的 () 调用结束后
        print(f"[strip] unexpected char before wx.createApp: {repr(content[ca_idx-1])}")
        iife_end = ca_idx

    # --- 执行移除 ---
    snippet_len = iife_end - iife_start
    print(f"[strip] Removing IIFE at {iife_start}..{iife_end} ({snippet_len} bytes)")

    new_content = content[:iife_start] + content[iife_end:]

    # 验证
    assert "shadow-grey.png" not in new_content, "removal failed"
    assert "fromCharCode" not in new_content[iife_start - 10 : iife_start + 100], "removal incomplete"

    vendor_path.write_text(new_content, "utf-8")
    print(f"[strip] Done. Removed {snippet_len} bytes from vendor.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
