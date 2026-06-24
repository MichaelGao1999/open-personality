/**
 * 国际化模块 — 内嵌中英文字符串
 * 复用 web 版 i18n JSON 的核心 key
 */
const strings = {
  zh: {
    'app.title': 'Open Personality',
    'app.subtitle': '大五人格（Big Five）测试',

    'home.speed': '极速模式',
    'home.speed_desc': 'IPIP-30 · 约 3 分钟',
    'home.standard': '标准模式',
    'home.standard_desc': 'IPIP-120 · 约 10 分钟',
    'home.advanced': '完整模式',
    'home.advanced_desc': 'IPIP-300 · 约 25 分钟',
    'home.start': '开始测试',
    'home.share_code_placeholder': '输入分享码查看报告',
    'home.share_code_button': '查询',
    'home.what_is_this': '什么是大五人格？',
    'home.why_big_title_1': '大五人格是什么？',
    'home.why_big_body_1': '大五人格（Big Five）是目前心理学领域最主流的人格模型之一，通过五个核心维度描述一个人的行为倾向、思维模式与情绪特点。',
    'home.why_big_title_2': '为什么值得你尝试？',
    'home.why_big_body_2': '相比传统的性格分类工具，大五人格最大的优势在于它建立在大量心理学研究和统计分析之上，更科学，也更贴近真实的人性。',
    'home.recent_title': '最近测评',
    'home.no_recent': '暂无最近记录',
    'home.resume_banner': '你有未完成的测评',
    'home.resume_btn': '继续答题',
    'home.resume_dismiss': '放弃',
    'home.continue_button': '继续答题',
    'home.continue_to_300': '想要更精准？继续答题',
    'home.standard_help': '标准120题评估模式，可随时中断和恢复，完成后也可选择继续答题细化评估',
    'home.speed_help': '基础30题评估模式，可随时中断和恢复，完成后也可选择继续答题细化评估',
    'home.advanced_help': '完整300题评估模式，可随时中断和恢复',

    'questionnaire.loading': '加载中...',
    'questionnaire.progress': '进度',
    'questionnaire.of': '/',
    'questionnaire.hint': '无需纠结，凭直觉选择',
    'questionnaire.prev': '上一题',
    'questionnaire.summary_title': '答题总览',
    'questionnaire.summary_desc': '请检查你的作答，点击可返回修改',
    'questionnaire.summary_unanswered': '未作答',
    'questionnaire.summary_submit': '提交答案',
    'questionnaire.confirm_title': '确认提交',
    'questionnaire.confirm_body': '你确定要提交答案吗？提交后将无法修改。',
    'questionnaire.cancel': '取消',
    'questionnaire.confirm': '确认提交',
    'questionnaire.partial_view': '查看当前结果',
    'questionnaire.partial_save': '保存到云端',
    'questionnaire.partial_saved': '进度已保存！分享码：',

    'report.title': '你的性格画像',
    'report.big_five': '大五人格',
    'report.mbti': 'MBTI 类型',
    'report.mbti_label': 'MBTI 解读为',
    'report.interpretation': '维度解读',
    'report.share': '分享报告',
    'report.share_copied': '已复制！',
    'report.share_code_label': '分享码',
    'report.back_home': '返回首页',
    'report.loading': '正在计算你的性格画像...',
    'report.partial_badge': '初步结果',
    'report.partial_note': '继续答题以获得更精确的性格画像',
    'report.continue_test': '继续答题',
  },
  en: {
    'app.title': 'Open Personality',
    'app.subtitle': 'Big Five Personality Test',

    'home.speed': 'Speed',
    'home.speed_desc': 'IPIP-30 · ~3 min',
    'home.standard': 'Standard',
    'home.standard_desc': 'IPIP-120 · ~10 min',
    'home.advanced': 'Advanced',
    'home.advanced_desc': 'IPIP-300 · ~25 min',
    'home.start': 'Start Test',
    'home.share_code_placeholder': 'Enter share code',
    'home.share_code_button': 'View',
    'home.what_is_this': 'What is Big Five?',
    'home.why_big_title_1': 'What is Big Five?',
    'home.why_big_body_1': 'The Big Five is one of the most widely accepted personality models in psychology, describing five core dimensions of human behavior and thinking.',
    'home.why_big_title_2': 'Why try it?',
    'home.why_big_body_2': 'Unlike simple binary personality types, the Big Five places everyone on a continuous spectrum across five dimensions, providing a more nuanced and scientifically grounded understanding of personality.',
    'home.recent_title': 'Recent Tests',
    'home.no_recent': 'No recent tests',
    'home.resume_banner': 'You have an unfinished test',
    'home.resume_btn': 'Continue',
    'home.resume_dismiss': 'Dismiss',
    'home.continue_button': 'Continue',
    'home.continue_to_300': 'Want more accuracy? Continue',
    'home.standard_help': 'Standard 120-question assessment. Pause and resume anytime.',
    'home.speed_help': 'Quick 30-question assessment. Pause and resume anytime.',
    'home.advanced_help': 'Complete 300-question assessment. Pause and resume anytime.',

    'questionnaire.loading': 'Loading...',
    'questionnaire.progress': 'Progress',
    'questionnaire.of': 'of',
    'questionnaire.hint': 'Go with your gut feeling',
    'questionnaire.prev': 'Previous',
    'questionnaire.summary_title': 'Answer Summary',
    'questionnaire.summary_desc': 'Review your answers, tap to go back',
    'questionnaire.summary_unanswered': 'Unanswered',
    'questionnaire.summary_submit': 'Submit Answers',
    'questionnaire.confirm_title': 'Confirm Submit',
    'questionnaire.confirm_body': 'Are you sure? Answers cannot be changed after submission.',
    'questionnaire.cancel': 'Cancel',
    'questionnaire.confirm': 'Confirm',
    'questionnaire.partial_view': 'View Partial Results',
    'questionnaire.partial_save': 'Save Progress',
    'questionnaire.partial_saved': 'Progress saved! Code:',

    'report.title': 'Your Personality Profile',
    'report.big_five': 'Big Five',
    'report.mbti': 'MBTI Type',
    'report.mbti_label': 'MBTI:',
    'report.interpretation': 'Interpretation',
    'report.share': 'Share Report',
    'report.share_copied': 'Copied!',
    'report.share_code_label': 'Share Code',
    'report.back_home': 'Back Home',
    'report.loading': 'Calculating your personality profile...',
    'report.partial_badge': 'Partial Results',
    'report.partial_note': 'Continue for more accurate results',
    'report.continue_test': 'Continue Test',
  },
}

let currentLang = 'zh'

export function useI18n() {
  function t(key) {
    return strings[currentLang]?.[key] || key
  }

  function setLang(lang) {
    if (strings[lang]) currentLang = lang
  }

  function getLang() {
    return currentLang
  }

  return { t, setLang, getLang }
}
