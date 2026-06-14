#!/bin/bash
# checkpoint.sh — 快速拍快照，改东西前跑一下
# 用法: bash scripts/checkpoint.sh "改字体颜色"
# 效果: git add -A && git commit -m "checkpoint: 改字体颜色" && git push

set -e

if [ -z "$1" ]; then
  echo "用法: bash scripts/checkpoint.sh \"改动说明\""
  echo "  例: bash scripts/checkpoint.sh \"调深色模式颜色\""
  exit 1
fi

MSG="checkpoint: $1"
echo "📸 checkpoint: $MSG"
git add -A
git commit -m "$MSG"
git push
echo ""
echo "✅ 完成 — 回滚方式:"
echo "   git revert HEAD       撤销这一步"
echo "   git checkout HEAD~1 -- 文件名  只恢复某个文件"
