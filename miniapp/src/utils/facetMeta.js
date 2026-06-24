/**
 * Facet 元数据 — 与 web 版同步
 */
export const dimColors = ['#7B2FF7', '#00B4D8', '#FFD60A', '#06D6A0', '#FF006E']
export const dimensionOrder = ['O', 'C', 'E', 'A', 'N']

export const dimLabel = {
  O: { zh: '开放性', en: 'Openness' },
  C: { zh: '严谨性', en: 'Conscientiousness' },
  E: { zh: '外向性', en: 'Extraversion' },
  A: { zh: '宜人性', en: 'Agreeableness' },
  N: { zh: '神经质', en: 'Neuroticism' },
}

export const facetMeta = {
  O_imagination:    { en: 'Imagination',          zh: '想象力' },
  O_aesthetics:     { en: 'Aesthetics',           zh: '审美敏感度' },
  O_feelings:       { en: 'Feelings',             zh: '情感丰富度' },
  O_adventurousness:{ en: 'Adventurousness',      zh: '冒险接受度' },
  O_intellect:      { en: 'Intellect',            zh: '求知欲' },
  O_liberalism:     { en: 'Liberalism',           zh: '思想开明度' },
  C_self_efficacy:         { en: 'Self-Efficacy',        zh: '自信程度' },
  C_orderliness:           { en: 'Orderliness',          zh: '条理性' },
  C_dutifulness:           { en: 'Dutifulness',          zh: '责任感' },
  C_achievement_striving:  { en: 'Achievement-Striving', zh: '成就欲' },
  C_self_discipline:       { en: 'Self-Discipline',      zh: '自律性' },
  C_cautiousness:          { en: 'Cautiousness',         zh: '审慎度' },
  E_friendliness:     { en: 'Friendliness',       zh: '热情程度' },
  E_gregariousness:   { en: 'Gregariousness',     zh: '群居偏好度' },
  E_assertiveness:    { en: 'Assertiveness',      zh: '支配欲' },
  E_activity_level:   { en: 'Activity Level',     zh: '活跃度' },
  E_excitement_seeking:{ en: 'Excitement-Seeking',zh: '刺激偏好度' },
  E_cheerfulness:     { en: 'Cheerfulness',       zh: '自然积极度' },
  A_trust:        { en: 'Trust',        zh: '信任倾向度' },
  A_morality:     { en: 'Morality',     zh: '社交直率度' },
  A_altruism:     { en: 'Altruism',     zh: '利他性' },
  A_cooperation:  { en: 'Cooperation',  zh: '顺从度' },
  A_modesty:      { en: 'Modesty',      zh: '低调指数' },
  A_sympathy:     { en: 'Sympathy',     zh: '同理心' },
  N_anxiety:             { en: 'Anxiety',             zh: '易焦虑程度' },
  N_anger:               { en: 'Anger',               zh: '易怒指数' },
  N_depression:          { en: 'Depression',          zh: '抑郁倾向' },
  N_self_consciousness:  { en: 'Self-Consciousness',  zh: '他人看法敏感度' },
  N_immoderation:        { en: 'Immoderation',        zh: '易冲动程度' },
  N_vulnerability:       { en: 'Vulnerability',       zh: '压力易感性' },
}

export const facetGroups = {
  O: ['O_imagination', 'O_aesthetics', 'O_feelings', 'O_adventurousness', 'O_intellect', 'O_liberalism'],
  C: ['C_self_efficacy', 'C_orderliness', 'C_dutifulness', 'C_achievement_striving', 'C_self_discipline', 'C_cautiousness'],
  E: ['E_friendliness', 'E_gregariousness', 'E_assertiveness', 'E_activity_level', 'E_excitement_seeking', 'E_cheerfulness'],
  A: ['A_trust', 'A_morality', 'A_altruism', 'A_cooperation', 'A_modesty', 'A_sympathy'],
  N: ['N_anxiety', 'N_anger', 'N_depression', 'N_self_consciousness', 'N_immoderation', 'N_vulnerability'],
}
