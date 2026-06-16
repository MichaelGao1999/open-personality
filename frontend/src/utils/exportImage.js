import html2canvas from 'html2canvas'

export async function exportCard(element, filename = 'personality-report.png') {
  const canvas = await html2canvas(element, {
    scale: 2,
    useCORS: true,
    backgroundColor: '#ffffff',
  })

  // Draw logo watermark at the bottom of the exported image
  const ctx = canvas.getContext('2d')
  const logoText = 'open personality'
  const fontSize = Math.max(11, canvas.width * 0.018)
  const paddingBottom = fontSize * 1.8

  ctx.save()
  ctx.font = `500 ${fontSize}px Inter, -apple-system, sans-serif`
  ctx.fillStyle = 'rgba(107, 114, 128, 0.55)'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'bottom'
  ctx.fillText(logoText, canvas.width / 2, canvas.height - paddingBottom)
  ctx.restore()

  const link = document.createElement('a')
  link.download = filename
  link.href = canvas.toDataURL('image/png')
  link.click()
}
