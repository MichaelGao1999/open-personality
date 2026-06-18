export const dimColors = ['#7B2FF7', '#00B4D8', '#FFD60A', '#06D6A0', '#FF006E']
export const dimensionOrder = ['O', 'C', 'E', 'A', 'N']

export const dimLabelCn = {
  O: '开放性',
  C: '严谨性',
  E: '外向性',
  A: '宜人性',
  N: '神经质',
}

export const dimLabelEn = {
  O: 'Openness',
  C: 'Conscientiousness',
  E: 'Extraversion',
  A: 'Agreeableness',
  N: 'Neuroticism',
}

export const facetMeta = {
  O_imagination:    { english: 'Imagination',          userTranslation: '想象力',     academicTranslation: '幻想' },
  O_aesthetics:     { english: 'Aesthetics',           userTranslation: '审美敏感度', academicTranslation: '审美' },
  O_feelings:       { english: 'Feelings',             userTranslation: '情感丰富度', academicTranslation: '感受丰富性' },
  O_adventurousness:{ english: 'Adventurousness',      userTranslation: '冒险接受度', academicTranslation: '求新性' },
  O_intellect:      { english: 'Intellect',            userTranslation: '求知欲',     academicTranslation: '智识' },
  O_liberalism:     { english: 'Liberalism',           userTranslation: '思想开明度', academicTranslation: '价值开放' },
  C_self_efficacy:         { english: 'Self-Efficacy',        userTranslation: '自信程度', academicTranslation: '胜任感' },
  C_orderliness:           { english: 'Orderliness',          userTranslation: '条理性',   academicTranslation: '有序性' },
  C_dutifulness:           { english: 'Dutifulness',          userTranslation: '责任感',   academicTranslation: '尽职' },
  C_achievement_striving:  { english: 'Achievement-Striving', userTranslation: '成就欲',   academicTranslation: '成就努力' },
  C_self_discipline:       { english: 'Self-Discipline',      userTranslation: '自律性',   academicTranslation: '自律性' },
  C_cautiousness:          { english: 'Cautiousness',         userTranslation: '审慎度',   academicTranslation: '审慎性' },
  E_friendliness:     { english: 'Friendliness',       userTranslation: '热情程度',   academicTranslation: '热情' },
  E_gregariousness:   { english: 'Gregariousness',     userTranslation: '群居偏好度', academicTranslation: '合群性' },
  E_assertiveness:    { english: 'Assertiveness',      userTranslation: '支配欲',     academicTranslation: '果敢性' },
  E_activity_level:   { english: 'Activity Level',     userTranslation: '活跃度',     academicTranslation: '活动水平' },
  E_excitement_seeking:{ english: 'Excitement-Seeking',userTranslation: '刺激偏好度', academicTranslation: '刺激寻求' },
  E_cheerfulness:     { english: 'Cheerfulness',       userTranslation: '自然积极度', academicTranslation: '正性情绪' },
  A_trust:        { english: 'Trust',        userTranslation: '信任倾向度', academicTranslation: '信任感' },
  A_morality:     { english: 'Morality',     userTranslation: '社交直率度', academicTranslation: '坦诚' },
  A_altruism:     { english: 'Altruism',     userTranslation: '利他性',     academicTranslation: '利他性' },
  A_cooperation:  { english: 'Cooperation',  userTranslation: '顺从度',     academicTranslation: '顺从' },
  A_modesty:      { english: 'Modesty',      userTranslation: '低调指数',   academicTranslation: '谦逊' },
  A_sympathy:     { english: 'Sympathy',     userTranslation: '同理心',     academicTranslation: '共情' },
  N_anxiety:             { english: 'Anxiety',             userTranslation: '易焦虑程度',     academicTranslation: '焦虑感' },
  N_anger:               { english: 'Anger',               userTranslation: '易怒指数',       academicTranslation: '愤怒性敌意' },
  N_depression:          { english: 'Depression',          userTranslation: '抑郁倾向',       academicTranslation: '抑郁性' },
  N_self_consciousness:  { english: 'Self-Consciousness',  userTranslation: '他人看法敏感度', academicTranslation: '自我意识性' },
  N_immoderation:        { english: 'Immoderation',        userTranslation: '易冲动程度',     academicTranslation: '冲动性' },
  N_vulnerability:       { english: 'Vulnerability',       userTranslation: '压力易感性',     academicTranslation: '脆弱性' },
}

export const facetGroups = {
  O: ['O_imagination', 'O_aesthetics', 'O_feelings', 'O_adventurousness', 'O_intellect', 'O_liberalism'],
  C: ['C_self_efficacy', 'C_orderliness', 'C_dutifulness', 'C_achievement_striving', 'C_self_discipline', 'C_cautiousness'],
  E: ['E_friendliness', 'E_gregariousness', 'E_assertiveness', 'E_activity_level', 'E_excitement_seeking', 'E_cheerfulness'],
  A: ['A_trust', 'A_morality', 'A_altruism', 'A_cooperation', 'A_modesty', 'A_sympathy'],
  N: ['N_anxiety', 'N_anger', 'N_depression', 'N_self_consciousness', 'N_immoderation', 'N_vulnerability'],
}
