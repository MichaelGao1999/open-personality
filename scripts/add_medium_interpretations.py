"""
为 interpretations_zh.json 和 interpretations_en.json 补充 medium 条目。
每个维度/面新增 medium.title + medium.body。
"""
import json

# ===== 中文 medium =====
ZH_MEDIUM = {
    # 维度
    "O": {"title": "开放性适中", "body": "你在开放性上处于中等水平，既保持着对新事物的好奇心，也不会轻易被新奇的想法带偏。你能够吸收新观念，但也保留了务实的判断力，在创新与传统之间找到平衡点。"},
    "C": {"title": "尽责性适中", "body": "你的尽责性处于中等水平，在自律和灵活性之间取得了不错的平衡。需要专注时你能投入，但也不会被计划束缚住，懂得根据实际情况调整节奏。"},
    "E": {"title": "外向性适中", "body": "你的外向性处于中等水平，在独处和社交之间切换自如。你既能享受与人相处的乐趣，也能从安静的独处中获得能量，属于灵活适应型。"},
    "A": {"title": "宜人性适中", "body": "你的宜人性处于中等水平，懂得在合作与坚持自我之间找到平衡。你关心他人感受，但也知道什么时候该表达自己的立场，不盲从也不对立。"},
    "N": {"title": "情绪稳定性适中", "body": "你的神经质处于中等水平，情绪反应在正常范围内。你能感知到压力与负面情绪的波动，但通常能自行调节恢复，不轻易被情绪左右。"},
    # 面
    "O_imagination": {"title": "想象力适中", "body": "你的想象力处于中等水平，有一定的创造性思维，但也不脱离现实基础。"},
    "O_aesthetics": {"title": "审美感受适中", "body": "你对美的感受处于中等水平，能欣赏艺术与自然之美，但不会过度沉迷其中。"},
    "O_feelings": {"title": "情感丰富度适中", "body": "你的情感丰富度处于中等水平，能察觉内心的情绪变化，但不会被情绪完全主导。"},
    "O_adventurousness": {"title": "冒险精神适中", "body": "你的冒险精神处于中等水平，愿意尝试新事物，同时也会权衡风险。"},
    "O_intellect": {"title": "求知欲适中", "body": "你的求知欲处于中等水平，对知识保持开放态度，但有自己关注的领域。"},
    "O_liberalism": {"title": "价值观开放度适中", "body": "你的价值观开放度处于中等水平，尊重多元观点，但也保留自己的核心信念。"},
    "C_self_efficacy": {"title": "自我效能感适中", "body": "你对自身能力的信心处于中等水平，相信自己的判断，但并不总是确信能成功。"},
    "C_orderliness": {"title": "条理性适中", "body": "你的条理性处于中等水平，做事有一定的规划，但也不排斥灵活调整。"},
    "C_dutifulness": {"title": "责任感适中", "body": "你的责任感处于中等水平，重视承诺，但偶尔也会根据优先级灵活处理。"},
    "C_achievement_striving": {"title": "成就追求适中", "body": "你的成就动机处于中等水平，有进取心，但不会为了成功牺牲一切。"},
    "C_self_discipline": {"title": "自律性适中", "body": "你的自律性处于中等水平，能够坚持完成任务，但也需要适当的休息和放松。"},
    "C_cautiousness": {"title": "谨慎性适中", "body": "你的谨慎性处于中等水平，做事会考虑后果，但也不至于过分犹豫。"},
    "E_friendliness": {"title": "友善度适中", "body": "你的友善度处于中等水平，待人真诚友善，但不会刻意迎合每一个人。"},
    "E_gregariousness": {"title": "合群性适中", "body": "你的合群性处于中等水平，喜欢与人相处，但也享受独处的时光。"},
    "E_assertiveness": {"title": "果断性适中", "body": "你的果断性处于中等水平，需要时能表达自己的观点，但也会听取他人意见。"},
    "E_activity_level": {"title": "活力水平适中", "body": "你的活力水平处于中等水平，有充沛精力应对日常事务，但也不会过度活跃。"},
    "E_excitement_seeking": {"title": "刺激寻求适中", "body": "你追求刺激的倾向处于中等水平，享受适度冒险，但不会刻意寻求高风险活动。"},
    "E_cheerfulness": {"title": "乐观程度适中", "body": "你的乐观程度处于中等水平，总体积极向上，但也承认生活中的不如意。"},
    "A_trust": {"title": "信任倾向适中", "body": "你的信任倾向处于中等水平，相信他人，但也会保持合理的警惕。"},
    "A_morality": {"title": "正直感适中", "body": "你的正直感处于中等水平，诚实守信，但在复杂情境中也会灵活变通。"},
    "A_altruism": {"title": "利他性适中", "body": "你的利他性处于中等水平，愿意帮助他人，但也会照顾自己的需要。"},
    "A_cooperation": {"title": "合作性适中", "body": "你的合作性处于中等水平，善于团队协作，同时也能独立思考。"},
    "A_modesty": {"title": "谦逊度适中", "body": "你的谦逊度处于中等水平，不刻意炫耀，但也不低估自己的价值。"},
    "A_sympathy": {"title": "同情心适中", "body": "你的同情心处于中等水平，能感受他人的情绪，但不会过度共情。"},
    "N_anxiety": {"title": "焦虑倾向适中", "body": "你的焦虑倾向处于中等水平，会为重要事情担忧，但通常不会持续过久。"},
    "N_anger": {"title": "愤怒倾向适中", "body": "你的愤怒倾向处于中等水平，遇到不公时会表达不满，但能较快平复。"},
    "N_depression": {"title": "抑郁倾向适中", "body": "你的抑郁倾向处于中等水平，偶尔会感到低落，但通常能自行恢复。"},
    "N_self_consciousness": {"title": "自我意识适中", "body": "你的自我意识处于中等水平，在意他人看法，但不会过度敏感。"},
    "N_immoderation": {"title": "冲动控制适中", "body": "你的冲动控制处于中等水平，偶尔会放纵自己，但总体上能约束行为。"},
    "N_vulnerability": {"title": "压力脆弱性适中", "body": "你对压力的承受能力处于中等水平，遇到压力时能应对，但也会感到吃力。"},
}

# ===== 英文 medium =====
EN_MEDIUM = {
    "O": {"title": "Moderate Openness", "body": "You have a balanced level of Openness to Experience. You're curious enough to explore new ideas but practical enough to stay grounded. You appreciate novelty without being easily distracted by every new trend, finding a comfortable middle ground between tradition and innovation."},
    "C": {"title": "Moderate Conscientiousness", "body": "You have a balanced level of Conscientiousness. You can be organized and disciplined when needed, but you also know when to be flexible and go with the flow. This adaptability lets you work hard without burning out."},
    "E": {"title": "Moderate Extraversion", "body": "You have a balanced level of Extraversion. You're comfortable in social settings but also value your alone time. You can be outgoing when the situation calls for it, yet you don't depend on constant social stimulation."},
    "A": {"title": "Moderate Agreeableness", "body": "You have a balanced level of Agreeableness. You care about others' feelings but also know how to stand your ground when necessary. You navigate cooperation and self-assertion with reasonable ease."},
    "N": {"title": "Moderate Emotional Stability", "body": "You have a moderate level of Neuroticism. You experience normal ups and downs in your emotions, but you generally recover well from stress and setbacks. Your emotional responses are proportionate to situations."},
    "O_imagination": {"title": "Moderate Imagination", "body": "You have a moderate imagination — creative enough to think outside the box, but practical enough to stay grounded in reality."},
    "O_aesthetics": {"title": "Moderate Aesthetic Sensitivity", "body": "You have a moderate appreciation for beauty and art — you can enjoy aesthetic experiences without being consumed by them."},
    "O_feelings": {"title": "Moderate Emotional Depth", "body": "You have moderate emotional depth — you're aware of your feelings but not entirely driven by them."},
    "O_adventurousness": {"title": "Moderate Adventurousness", "body": "You have a moderate sense of adventure — willing to try new things, but with reasonable caution."},
    "O_intellect": {"title": "Moderate Intellectual Curiosity", "body": "You have moderate intellectual curiosity — open to learning, with focused interests rather than scattered exploration."},
    "O_liberalism": {"title": "Moderate Openness to Values", "body": "You have a moderate openness to new values — respectful of different perspectives while holding your own core beliefs."},
    "C_self_efficacy": {"title": "Moderate Self-Efficacy", "body": "You have moderate self-efficacy — you trust your abilities but acknowledge that success isn't always certain."},
    "C_orderliness": {"title": "Moderate Orderliness", "body": "You have moderate orderliness — you like some structure but can adapt when plans change."},
    "C_dutifulness": {"title": "Moderate Dutifulness", "body": "You have a moderate sense of duty — you keep your promises but know when to reprioritize."},
    "C_achievement_striving": {"title": "Moderate Achievement Striving", "body": "You have moderate achievement drive — ambitious enough to aim high, but balanced enough not to sacrifice everything for success."},
    "C_self_discipline": {"title": "Moderate Self-Discipline", "body": "You have moderate self-discipline — you can stay on task but also allow yourself breaks when needed."},
    "C_cautiousness": {"title": "Moderate Cautiousness", "body": "You have moderate cautiousness — you think before acting without being overly hesitant."},
    "E_friendliness": {"title": "Moderate Friendliness", "body": "You have moderate friendliness — warm and approachable, but not overly eager to please."},
    "E_gregariousness": {"title": "Moderate Gregariousness", "body": "You have a moderate social drive — you enjoy company but also value solitude."},
    "E_assertiveness": {"title": "Moderate Assertiveness", "body": "You have moderate assertiveness — you speak up when needed while respecting others' input."},
    "E_activity_level": {"title": "Moderate Activity Level", "body": "You have a moderate activity level — energetic enough for daily demands without being constantly on the go."},
    "E_excitement_seeking": {"title": "Moderate Excitement Seeking", "body": "You have a moderate need for excitement — you enjoy some thrill but don't chase extreme experiences."},
    "E_cheerfulness": {"title": "Moderate Cheerfulness", "body": "You have moderate cheerfulness — generally positive in outlook while acknowledging life's difficulties."},
    "A_trust": {"title": "Moderate Trust", "body": "You have a moderate level of trust — you give people the benefit of the doubt while keeping reasonable caution."},
    "A_morality": {"title": "Moderate Morality", "body": "You have a moderate moral compass — honest and principled, yet able to navigate gray areas."},
    "A_altruism": {"title": "Moderate Altruism", "body": "You have moderate altruism — you help others without neglecting your own needs."},
    "A_cooperation": {"title": "Moderate Cooperation", "body": "You have a moderate tendency to cooperate — you work well in teams while maintaining independent thinking."},
    "A_modesty": {"title": "Moderate Modesty", "body": "You have moderate modesty — you don't show off, but you also recognize your own worth."},
    "A_sympathy": {"title": "Moderate Sympathy", "body": "You have moderate sympathy — you can feel for others without being overwhelmed by their emotions."},
    "N_anxiety": {"title": "Moderate Anxiety", "body": "You have a moderate tendency toward anxiety — you worry about important matters but usually move past it."},
    "N_anger": {"title": "Moderate Anger", "body": "You have a moderate tendency toward anger — you can express frustration when needed but generally recover quickly."},
    "N_depression": {"title": "Moderate Depression", "body": "You have a moderate tendency toward low mood — you experience occasional sadness but typically bounce back."},
    "N_self_consciousness": {"title": "Moderate Self-Consciousness", "body": "You have moderate self-consciousness — you care about others' perceptions without being overly sensitive."},
    "N_immoderation": {"title": "Moderate Immoderation", "body": "You have moderate self-control — you occasionally indulge but maintain overall discipline."},
    "N_vulnerability": {"title": "Moderate Vulnerability to Stress", "body": "You have moderate resilience to stress — you can cope with pressure but it does take its toll at times."},
}


def add_medium(filepath, medium_map):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    added = 0
    for key, medium in medium_map.items():
        if key in data:
            if "medium" not in data[key]:
                data[key]["medium"] = medium
                added += 1
    
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    
    return added


if __name__ == "__main__":
    zh_file = "backend/data/interpretations_zh.json"
    en_file = "backend/data/interpretations_en.json"
    
    n_zh = add_medium(zh_file, ZH_MEDIUM)
    n_en = add_medium(en_file, EN_MEDIUM)
    
    print(f"zh: 新增 {n_zh}/35 条 medium 条目")
    print(f"en: 新增 {n_en}/35 条 medium 条目")
    print("✅ 完成")
