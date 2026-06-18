import json
import os
from typing import Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "data")

facets = {
    "O": ["imagination", "aesthetics", "feelings", "adventurousness", "intellect", "liberalism"],
    "C": ["self_efficacy", "orderliness", "dutifulness", "achievement_striving", "self_discipline", "cautiousness"],
    "E": ["friendliness", "gregariousness", "assertiveness", "activity_level", "excitement_seeking", "cheerfulness"],
    "A": ["trust", "morality", "altruism", "cooperation", "modesty", "sympathy"],
    "N": ["anxiety", "anger", "depression", "self_consciousness", "immoderation", "vulnerability"],
}

en_texts = {
    "O_imagination": [
        "I have a rich imagination.",
        "I enjoy daydreaming about possibilities.",
        "I seldom daydream.",  # rev
        "I find it hard to imagine things that don't exist.",  # rev
    ],
    "O_aesthetics": [
        "I love exploring art and beauty.",
        "I am deeply moved by natural beauty.",
        "Abstract art does not appeal to me.",  # rev
        "I seldom notice aesthetic details.",  # rev
    ],
    "O_feelings": [
        "I experience strong emotions.",
        "I am very sensitive to my feelings.",
        "I rarely pay attention to my emotions.",  # rev
        "I don't let emotions affect my decisions.",  # rev
    ],
    "O_adventurousness": [
        "I prefer variety to routine.",
        "I love trying new things.",
        "I prefer familiar routines.",  # rev
        "I am uncomfortable with change.",  # rev
    ],
    "O_intellect": [
        "I enjoy exploring abstract ideas.",
        "I love philosophical discussions.",
        "I find intellectual debates boring.",  # rev
        "I prefer practical topics over abstract ones.",  # rev
    ],
    "O_liberalism": [
        "I am open to unconventional ideas.",
        "I tend to support progressive values.",
        "I believe traditional values are important.",  # rev
        "I prefer tried-and-true methods.",  # rev
    ],
    "C_self_efficacy": [
        "I complete tasks successfully.",
        "I excel in what I do.",
        "I often doubt my abilities.",  # rev
        "I feel underqualified for many tasks.",  # rev
    ],
    "C_orderliness": [
        "I like to keep things organized.",
        "I find order and routine appealing.",
        "I often leave things lying around.",  # rev
        "My workspace is usually messy.",  # rev
    ],
    "C_dutifulness": [
        "I keep my promises.",
        "I follow through on commitments.",
        "I sometimes break my promises.",  # rev
        "I tend to bend rules when convenient.",  # rev
    ],
    "C_achievement_striving": [
        "I strive for excellence in everything.",
        "I set high standards for myself.",
        "I am satisfied with just getting by.",  # rev
        "I don't push myself to achieve more.",  # rev
    ],
    "C_self_discipline": [
        "I get chores done right away.",
        "I am disciplined in my habits.",
        "I often procrastinate on important tasks.",  # rev
        "I need external pressure to start working.",  # rev
    ],
    "C_cautiousness": [
        "I think carefully before acting.",
        "I avoid mistakes by being thorough.",
        "I tend to act impulsively.",  # rev
        "I often rush through decisions.",  # rev
    ],
    "E_friendliness": [
        "I enjoy spending time with people.",
        "I make friends easily.",
        "I prefer to be alone.",  # rev
        "I find social situations draining.",  # rev
    ],
    "E_gregariousness": [
        "I love large social events.",
        "I enjoy being part of a crowd.",
        "I prefer quiet evenings alone.",  # rev
        "I dislike crowded places.",  # rev
    ],
    "E_assertiveness": [
        "I take charge in groups.",
        "I express my opinions confidently.",
        "I let others take the lead.",  # rev
        "I prefer to stay in the background.",  # rev
    ],
    "E_activity_level": [
        "I am always busy doing something.",
        "I have a lot of energy.",
        "I prefer a relaxed pace of life.",  # rev
        "I often feel sluggish.",  # rev
    ],
    "E_excitement_seeking": [
        "I seek adventure and excitement.",
        "I enjoy thrilling activities.",
        "I prefer a calm and quiet life.",  # rev
        "I avoid risky situations.",  # rev
    ],
    "E_cheerfulness": [
        "I laugh easily and often.",
        "I am a cheerful optimist.",
        "I often feel gloomy.",  # rev
        "I tend to see the negative side.",  # rev
    ],
    "A_trust": [
        "I trust people easily.",
        "I believe people have good intentions.",
        "I tend to be suspicious of others.",  # rev
        "I think most people would take advantage.",  # rev
    ],
    "A_morality": [
        "I would never cheat or lie.",
        "I value honesty above all.",
        "I sometimes bend the truth.",  # rev
        "I believe the end can justify the means.",  # rev
    ],
    "A_altruism": [
        "I enjoy helping others.",
        "I put others' needs before mine.",
        "I am not interested in volunteer work.",  # rev
        "I think people should look after themselves.",  # rev
    ],
    "A_cooperation": [
        "I am easy to work with.",
        "I value cooperation over competition.",
        "I prefer to work alone.",  # rev
        "I enjoy competing against others.",  # rev
    ],
    "A_modesty": [
        "I am humble about my achievements.",
        "I don't like to brag.",
        "I often talk about my accomplishments.",  # rev
        "I think I am better than most people.",  # rev
    ],
    "A_sympathy": [
        "I feel others' emotions deeply.",
        "I am moved by others' suffering.",
        "I find it hard to sympathize with people.",  # rev
        "Others' problems don't affect me much.",  # rev
    ],
    "N_anxiety": [
        "I worry about many things.",
        "I get stressed easily.",
        "I seldom feel anxious.",  # rev
        "I remain calm in most situations.",  # rev
    ],
    "N_anger": [
        "I get irritated easily.",
        "I have a quick temper.",
        "I rarely get angry.",  # rev
        "I am even-tempered and hard to upset.",  # rev
    ],
    "N_depression": [
        "I often feel sad or blue.",
        "I tend to feel down more than others.",
        "I rarely feel depressed.",  # rev
        "I am generally in good spirits.",  # rev
    ],
    "N_self_consciousness": [
        "I am easily embarrassed.",
        "I feel awkward in social situations.",
        "I am comfortable with who I am.",  # rev
        "I rarely worry about what others think.",  # rev
    ],
    "N_immoderation": [
        "I often give in to temptations.",
        "I have difficulty controlling impulses.",
        "I can resist temptations easily.",  # rev
        "I practice self-control regularly.",  # rev
    ],
    "N_vulnerability": [
        "I panic easily under pressure.",
        "I fall apart under stress.",
        "I stay calm under pressure.",  # rev
        "I handle crises well.",  # rev
    ],
}

zh_texts = {
    "O_imagination": [
        "我有丰富的想象力。",
        "我喜欢对可能性做白日梦。",
        "我很少做白日梦。",
        "我觉得想象不存在的东西很难。",
    ],
    "O_aesthetics": [
        "我喜欢探索艺术和自然之美。",
        "自然之美深深打动我。",
        "我对抽象艺术不感兴趣。",
        "我很少留意审美细节。",
    ],
    "O_feelings": [
        "我体验强烈的情绪。",
        "我对自己的情绪非常敏感。",
        "我很少留意自己的情绪状态。",
        "我不会让情绪影响我的决定。",
    ],
    "O_adventurousness": [
        "我更喜欢变化而非按部就班。",
        "我喜欢尝试新事物。",
        "我更喜欢熟悉的常规。",
        "我对变化感到不安。",
    ],
    "O_intellect": [
        "我喜欢探索抽象概念。",
        "我热爱哲学讨论。",
        "我觉得烧脑的辩论很无聊。",
        "比起抽象话题我更喜欢实用的。",
    ],
    "O_liberalism": [
        "我乐于接受非常规的想法。",
        "我倾向于支持进步的主张。",
        "我相信传统价值观很重要。",
        "我更喜欢经过验证的方法。",
    ],
    "C_self_efficacy": [
        "我能成功完成任务。",
        "我擅长我所做的事。",
        "我经常怀疑自己的能力。",
        "面对很多任务我都觉得不够格。",
    ],
    "C_orderliness": [
        "我喜欢保持事物井井有条。",
        "我觉得条理和常规很有吸引力。",
        "我经常随手乱放东西。",
        "我的工作空间通常很乱。",
    ],
    "C_dutifulness": [
        "我信守承诺。",
        "我会坚持履行我的义务。",
        "我有时会违背承诺。",
        "我倾向于在方便时变通规则。",
    ],
    "C_achievement_striving": [
        "我做每件事都追求卓越。",
        "我为自己设定高标准。",
        "我对敷衍了事感到满足。",
        "我不会逼自己去争取更多。",
    ],
    "C_self_discipline": [
        "我会立刻完成该做的事。",
        "我的习惯很有自律性。",
        "我经常拖延重要任务。",
        "我需要外部压力才能开始工作。",
    ],
    "C_cautiousness": [
        "我行动前会仔细思考。",
        "我通过细致来避免错误。",
        "我倾向于冲动行事。",
        "我经常仓促做出决定。",
    ],
    "E_friendliness": [
        "我喜欢和别人待在一起。",
        "我很容易交朋友。",
        "我更喜欢独处。",
        "我觉得社交场合很消耗精力。",
    ],
    "E_gregariousness": [
        "我喜爱大型社交活动。",
        "我喜欢身处人群之中。",
        "我更喜欢安静的独处时光。",
        "我不喜欢拥挤的地方。",
    ],
    "E_assertiveness": [
        "我在群体中主动担责。",
        "我自信地表达自己的观点。",
        "我让他人来做主导。",
        "我更喜欢待在幕后。",
    ],
    "E_activity_level": [
        "我总是忙着做各种事。",
        "我精力充沛。",
        "我更喜欢慢节奏的生活。",
        "我经常感到没精神。",
    ],
    "E_excitement_seeking": [
        "我追求冒险和刺激。",
        "我喜欢刺激的活动。",
        "我更喜欢平静安宁的生活。",
        "我避免有风险的情况。",
    ],
    "E_cheerfulness": [
        "我经常开怀大笑。",
        "我是个开朗的乐天派。",
        "我经常感到忧郁。",
        "我倾向于看事情消极的一面。",
    ],
    "A_trust": [
        "我容易信任他人。",
        "我相信人们怀有善意。",
        "我倾向于怀疑别人。",
        "我觉得大多数人都会占便宜。",
    ],
    "A_morality": [
        "我绝不作弊或说谎。",
        "我把诚实看得高于一切。",
        "我有时会歪曲事实。",
        "我相信结果可以证明手段正当。",
    ],
    "A_altruism": [
        "我喜欢帮助别人。",
        "我把别人的需要放在自己之前。",
        "我对志愿工作不感兴趣。",
        "我认为每个人都应该管好自己。",
    ],
    "A_cooperation": [
        "我很好合作共事。",
        "我重视合作胜过竞争。",
        "我更喜欢独自工作。",
        "我喜欢与他人竞争。",
    ],
    "A_modesty": [
        "我对自己的成就保持谦虚。",
        "我不喜欢吹嘘。",
        "我经常谈论自己的成就。",
        "我认为自己比大多数人优秀。",
    ],
    "A_sympathy": [
        "我能深刻感受到他人的情绪。",
        "别人的苦难会触动我。",
        "我很难同情别人。",
        "别人的问题不太影响我。",
    ],
    "N_anxiety": [
        "我担心很多事情。",
        "我很容易紧张。",
        "我很少感到焦虑。",
        "我在大多数情况下保持冷静。",
    ],
    "N_anger": [
        "我很容易烦躁。",
        "我脾气来得快。",
        "我很少生气。",
        "我性情平和，很难被惹恼。",
    ],
    "N_depression": [
        "我经常感到悲伤或忧郁。",
        "我比别人更容易情绪低落。",
        "我很少感到沮丧。",
        "我通常心情不错。",
    ],
    "N_self_consciousness": [
        "我很容易难为情。",
        "我在社交场合感到不自在。",
        "我对自己感到自在。",
        "我很少担心别人的看法。",
    ],
    "N_immoderation": [
        "我经常屈服于诱惑。",
        "我很难控制冲动。",
        "我能轻松抵制诱惑。",
        "我经常进行自我克制。",
    ],
    "N_vulnerability": [
        "压力下我容易慌乱。",
        "压力下我会崩溃。",
        "我在压力下保持冷静。",
        "我能很好地应对危机。",
    ],
}

idx = 0
items_zh = []
items_en = []
for dim in ["O", "C", "E", "A", "N"]:
    for facet_name in facets[dim]:
        key = f"{dim}_{facet_name}"
        for q_idx in range(4):
            idx += 1
            item_id = f"ipip_{idx:03d}"
            rev = q_idx >= 2
            items_zh.append({
                "item_id": item_id, "dimension": dim,
                "facet": key, "text": zh_texts[key][q_idx], "reversed": rev,
            })
            items_en.append({
                "item_id": item_id, "dimension": dim,
                "facet": key, "text": en_texts[key][q_idx], "reversed": rev,
            })

os.makedirs(os.path.join(DATA_DIR, "items"), exist_ok=True)
for lang, items in [("zh", items_zh), ("en", items_en)]:
    path = os.path.join(DATA_DIR, "items", f"ipip120_{lang}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"metadata": {"mode": "standard", "total_items": 120, "lang": lang}, "items": items}, f, ensure_ascii=False, indent=2)
    print(f"Saved {path} ({len(items)} items)")

mbti = {
    "E_I": {"weights": {"E": 0.35, "A": -0.15, "N": -0.10}, "bias": 0.0},
    "S_N": {"weights": {"O": 0.40, "E": 0.10, "C": -0.15}, "bias": 0.0},
    "T_F": {"weights": {"A": 0.35, "C": 0.10, "O": 0.05}, "bias": 0.0},
    "J_P": {"weights": {"C": 0.40, "O": -0.20, "N": 0.10}, "bias": 0.0},
}
with open(os.path.join(DATA_DIR, "mbti_mapping.json"), "w", encoding="utf-8") as f:
    json.dump(mbti, f, ensure_ascii=False, indent=2)
print("Saved mbti_mapping.json")

all_facet_keys = [f"{dim}_{facet}" for dim in ["O","C","E","A","N"] for facet in facets[dim]]
norms: dict[str, Any] = {}
for dim in ["O","C","E","A","N"]:
    norms[dim] = {"mean": 50.0, "sd": 10.0}
for key in all_facet_keys:
    norms[key] = {"mean": 50.0, "sd": 10.0}
norms["metadata"] = {"standard": "T-score (M=50, SD=10)", "source": "initial preset"}
with open(os.path.join(DATA_DIR, "norms.json"), "w", encoding="utf-8") as f:
    json.dump(norms, f, ensure_ascii=False, indent=2)
print("Saved norms.json")

dim_titles_zh = {
    "O": "开放性", "C": "严谨性", "E": "外向性", "A": "宜人性", "N": "神经质"
}
dim_titles_en = {
    "O": "Openness", "C": "Conscientiousness", "E": "Extraversion", "A": "Agreeableness", "N": "Neuroticism"
}

zh_interpretations = {}
en_interpretations = {}
for dim in ["O","C","E","A","N"]:
    short_zh = dim_titles_zh[dim]
    short_en = dim_titles_en[dim]
    zh_interpretations[dim] = {
        "high": {"title": f"{short_zh}偏高", "body": f"你在{short_zh}维度上得分较高。请补充详细解读。"},
        "low": {"title": f"{short_zh}偏低", "body": f"你在{short_zh}维度上得分较低。请补充详细解读。"},
    }
    en_interpretations[dim] = {
        "high": {"title": f"High in {short_en}", "body": f"You scored high in {short_en}. Detailed interpretation pending."},
        "low": {"title": f"Low in {short_en}", "body": f"You scored low in {short_en}. Detailed interpretation pending."},
    }
    for facet_name in facets[dim]:
        key = f"{dim}_{facet_name}"
        zh_interpretations[key] = {
            "high": {"title": f"{key} 偏高", "body": f"你在{key}上得分较高。"},
            "low": {"title": f"{key} 偏低", "body": f"你在{key}上得分较低。"},
        }
        en_interpretations[key] = {
            "high": {"title": f"High {key}", "body": f"You scored high on {key}."},
            "low": {"title": f"Low {key}", "body": f"You scored low on {key}."},
        }

with open(os.path.join(DATA_DIR, "interpretations_zh.json"), "w", encoding="utf-8") as f:
    json.dump(zh_interpretations, f, ensure_ascii=False, indent=2)
print("Saved interpretations_zh.json")

with open(os.path.join(DATA_DIR, "interpretations_en.json"), "w", encoding="utf-8") as f:
    json.dump(en_interpretations, f, ensure_ascii=False, indent=2)
print("Saved interpretations_en.json")

eggs = {
    "eggs": [
        {"id": "egg_001", "zh": "你的创造力指数堪比文艺复兴大师——建议今天请半天假去美术馆。", "en": "Your creativity rivals the Renaissance masters. Take a half day for the museum."},
        {"id": "egg_002", "zh": "心理学家说你的大脑结构像迷宫——连你自己都会迷路。", "en": "Psychologists say your brain is like a maze. Even you get lost in it."},
        {"id": "egg_003", "zh": "你的共情能力强到能感受到宠物的情绪。你的猫今天心情不好。", "en": "Your empathy lets you sense your pet's mood. Your cat is having a rough day."},
        {"id": "egg_004", "zh": "据测算，你昨晚的决定中有73%其实是潜意识做的。它想告诉你：该睡了。", "en": "73% of your decisions last night were subconscious. It says: go to bed."},
        {"id": "egg_005", "zh": "严谨性测试显示：你认真读了每道题。连这一条也是。", "en": "Conscientiousness check: you read every question carefully. Even this one."},
        {"id": "egg_006", "zh": "开放性满分。说明你连测什么都无所谓。", "en": "Perfect Openness score. You don't even care what this test measures."},
        {"id": "egg_007", "zh": "宜人性过高警告：你可能刚刚对弹出的广告说了不好意思。", "en": "Agreeableness alert: you may have just apologized to a pop-up ad."},
        {"id": "egg_008", "zh": "神经质维度显示：你的大脑默认在灾难预演模式。今天预演得不错，挺精彩。", "en": "Your brain runs in disaster-prehearsal mode. Today's rehearsal was quite dramatic."},
        {"id": "egg_009", "zh": "研究表明选中立最多的人，在生活中也最难点外卖。", "en": "Research: people who pick Neutral most often also struggle to order takeout."},
        {"id": "egg_010", "zh": "你的外向性得分意味着你是派对里帮主人洗碗的那种人。", "en": "Your Extraversion means you're the type who helps wash dishes at parties."},
        {"id": "egg_011", "zh": "本测试由一群INTP开发。他们现在在争论这个彩蛋分类对不对。", "en": "Built by a team of INTPs. They're now debating whether this egg is correctly categorized."},
        {"id": "egg_012", "zh": "你做这道题时，世界上有47个人同时在测。其中一人选了和你一样的答案。平行宇宙确认+1。", "en": "47 people take this test simultaneously. One picked the same answer. Parallel universe confirmed."},
    ],
    "medium": [
        {"id": "medium_001", "zh": "关于我是谁这个问题，大五人格给了你五个数字。不算回答，但至少比GPS坐标浪漫一点。", "en": "To 'Who am I?' the Big Five gives five numbers. Not an answer, but more romantic than GPS coordinates."},
        {"id": "medium_002", "zh": "McCrae & Costa 1989年发表MBTI映射论文时用的是手算。你的MBTI概率背后有35年前的纸笔余温。", "en": "McCrae & Costa hand-calculated the 1989 MBTI paper. Your probabilities carry 35-year-old pencil-on-paper echoes."},
        {"id": "medium_003", "zh": "IPIP量表最初为了让心理学研究免费而生。你刚参加了一场持续30年的学术开源运动。", "en": "IPIP was created to make psych research free. You just joined a 30-year academic open-source movement."},
        {"id": "medium_004", "zh": "本测试不告诉你你是谁。它只告诉你，在120道题上你的回答和某些人有多相似。真正的答案在你自己那儿。", "en": "This test won't tell you who you are. Just how your answers resemble a population. The real answer's inside you."},
    ],
    "trigger_rate": 0.1,
}

with open(os.path.join(DATA_DIR, "easter_eggs.json"), "w", encoding="utf-8") as f:
    json.dump(eggs, f, ensure_ascii=False, indent=2)
print("Saved easter_eggs.json")

print("All data files created!")
