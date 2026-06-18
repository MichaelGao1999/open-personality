import { dimLabelCn, dimLabelEn, facetMeta, facetGroups, dimensionOrder } from './facetMeta.js'

function getScore(scoring, dim) {
  return scoring?.t_scores?.[dim] ?? scoring?.[dim] ?? 50
}

function getFacetScore(scoring, facetKey) {
  return scoring?.facet_scores?.[facetKey] ?? 50
}

export function compare(myReport, friendReport, lang = 'zh') {
  const myScoring = myReport.scoring
  const friendScoring = friendReport.scoring
  const labels = lang === 'zh' ? dimLabelCn : dimLabelEn

  const dimDiffs = dimensionOrder.map(dim => ({
    dim,
    label: labels[dim],
    myScore: getScore(myScoring, dim),
    friendScore: getScore(friendScoring, dim),
    diff: getScore(myScoring, dim) - getScore(friendScoring, dim),
  }))

  const allFacets = dimensionOrder.flatMap(dim =>
    facetGroups[dim].map(key => ({
      key,
      dim,
      label: facetMeta[key]?.userTranslation ?? key,
      myScore: getFacetScore(myScoring, key),
      friendScore: getFacetScore(friendScoring, key),
      diff: getFacetScore(myScoring, key) - getFacetScore(friendScoring, key),
    }))
  )

  const facetDiffs = allFacets
    .filter(f => Math.abs(f.diff) > 1)
    .sort((a, b) => Math.abs(b.diff) - Math.abs(a.diff))
    .slice(0, 10)

  const similarity = Math.max(0, Math.min(100,
    Math.round(100 - dimDiffs.reduce((sum, d) => sum + Math.abs(d.diff), 0) / 5)
  ))

  const bestDim = dimDiffs.reduce((a, b) => Math.abs(b.diff) > Math.abs(a.diff) ? b : a, dimDiffs[0])

  return { dimDiffs, facetDiffs, similarity, topDiffDim: bestDim }
}
