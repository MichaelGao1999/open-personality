/**
 * 构建后脚本：从 vendor.js 中移除 uni-app 框架内置的 shadow-grey.png 预加载
 *
 * 此预加载是 uni-app 的 <image> 组件默认占位图，本项目未使用 <image> 标签，
 * 且 CDN 地址在微信开发者工具中会超时报错（Error: timeout），阻塞调试预览。
 *
 * 用法（在 miniapp/ 目录下）：
 *   node scripts/strip-shadow-preload.js
 */

const fs = require('fs')
const path = require('path')

const vendorPath = path.resolve(__dirname, '..', 'dist/build/mp-weixin/common/vendor.js')

if (!fs.existsSync(vendorPath)) {
  console.log('[strip] vendor.js not found, skipping')
  process.exit(0)
}

let content = fs.readFileSync(vendorPath, 'utf-8')

// 定位 "shadow-grey.png" 关键词，向后找到最近的尾部代码边界
const marker = 'shadow-grey.png'
const idx = content.indexOf(marker)
if (idx === -1) {
  console.log('[strip] shadow-grey.png not found in vendor.js - already clean')
  process.exit(0)
}

// 向前找到最近的逗号或分号作为起始边界
let start = idx
for (let i = idx; i >= 0; i--) {
  const ch = content[i]
  if (ch === ',' || ch === ';') {
    // 但如果前面跟著 . 或者 [ 的逗号会误切，检查一下
    // vendor.js 中是 ,setTimeout(...) 这种模式
    start = i
    break
  }
}

// 向后找到代码块的闭合边界 — 统计大括号/圆括号
let braceCount = 0
let parenCount = 0
let inCapture = false
let end = idx
for (let i = idx - 50; i < content.length; i++) {
  // 找到 setTimeout 开始捕获
  if (content.slice(i, i + 10) === 'setTimeout') {
    start = i - 1  // 包括前面的逗号
    break
  }
}

// 从 start 开始，找到匹配的闭合括号
for (let i = start; i < content.length; i++) {
  const ch = content[i]
  if (ch === '(') parenCount++
  if (ch === ')') parenCount--
  if (content[i] === '{') braceCount++
  if (content[i] === '}') braceCount--
  if (content[i] === ')' && parenCount <= 0 && braceCount <= 0) {
    end = i + 1
    break
  }
}

const snippet = content.slice(start, end)
console.log('[strip] Removing preload snippet:', snippet.slice(0, 120) + '...')

// 从 start 到 end 的位置替换为逗号（保持前端数组元素间的逗号）
content = content.slice(0, start) + content.slice(end)
fs.writeFileSync(vendorPath, content, 'utf-8')
console.log('[strip] Done: removed shadow-grey.png preload from vendor.js')
