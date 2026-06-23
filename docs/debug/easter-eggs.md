# 彩蛋文案工作台

数据源：`backend/data/easter_eggs.json`

## 触发机制

- 基础模式（standard/speed）：每次提交 10% 概率触发
- 完整 300 题（advanced + complete）：**100% 触发**
- 修改文案后需同时维护中英文（`zh` / `en` 字段）
- 引号需 JSON 转义：`"` → `\"`

---

## Short Eggs（12 条）

| ID | zh | en |
|----|----|----|
| egg_001 | 你的创造力指数堪比文艺复兴大师——建议今天请半天假去美术馆。 | Your creativity rivals the Renaissance masters. Take a half day for the museum. |
| egg_002 | 心理学家说你的大脑结构像迷宫——连你自己都会迷路。 | Psychologists say your brain is like a maze. Even you get lost in it. |
| egg_003 | 你的共情能力强到能感受到宠物的情绪。你的猫今天心情不好。 | Your empathy lets you sense your pet's mood. Your cat is having a rough day. |
| egg_004 | 据测算，你昨晚的决定中有73%其实是潜意识做的。它想告诉你：该睡了。 | 73% of your decisions last night were subconscious. It says: go to bed. |
| egg_005 | 严谨性测试显示：你认真读了每道题。连这一条也是。 | Conscientiousness check: you read every question carefully. Even this one. |
| egg_006 | 开放性满分。说明你连测什么都无所谓。 | Perfect Openness score. You don't even care what this test measures. |
| egg_007 | 宜人性过高警告：你可能刚刚对弹出的广告说了不好意思。 | Agreeableness alert: you may have just apologized to a pop-up ad. |
| egg_008 | 神经质维度显示：你的大脑默认在灾难预演模式。今天预演得不错，挺精彩。 | Your brain runs in disaster-prehearsal mode. Today's rehearsal was quite dramatic. |
| egg_009 | 研究表明选中立最多的人，在生活中也最难点外卖。 | Research: people who pick Neutral most often also struggle to order takeout. |
| egg_010 | 你的外向性得分意味着你是派对里帮主人洗碗的那种人。 | Your Extraversion means you're the type who helps wash dishes at parties. |
| egg_011 | 本测试由一群INTP开发。他们现在在争论这个彩蛋分类对不对。 | Built by a team of INTPs. They're now debating whether this egg is correctly categorized. |
| egg_012 | 你做这道题时，世界上有47个人同时在测。其中一人选了和你一样的答案。平行宇宙确认+1。 | 47 people take this test simultaneously. One picked the same answer. Parallel universe confirmed. |

## Medium Eggs（4 条）

| ID | zh | en |
|----|----|----|
| medium_001 | 关于我是谁这个问题，大五人格给了你五个数字。不算回答，但至少比GPS坐标浪漫一点。 | To 'Who am I?' the Big Five gives five numbers. Not an answer, but more romantic than GPS coordinates. |
| medium_002 | McCrae & Costa 1989年发表MBTI映射论文时用的是手算。你的MBTI概率背后有35年前的纸笔余温。 | McCrae & Costa hand-calculated the 1989 MBTI paper. Your probabilities carry 35-year-old pencil-on-paper echoes. |
| medium_003 | IPIP量表最初为了让心理学研究免费而生。你刚参加了一场持续30年的学术开源运动。 | IPIP was created to make psych research free. You just joined a 30-year academic open-source movement. |
| medium_004 | 本测试不告诉你你是谁。它只告诉你，在120道题上你的回答和某些人有多相似。真正的答案在你自己那儿。 | This test won't tell you who you are. Just how your answers resemble a population. The real answer's inside you. |

---

## 修改流程

1. 在此文件 Markdown 表格中调整文案
2. 确认无误后将改动同步回 `backend/data/easter_eggs.json`
3. 运行测试确认：`cd backend && python -m pytest tests/test_easter_egg.py -v`
