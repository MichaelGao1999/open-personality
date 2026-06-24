# b5-result-text vs open-personality 域级文案对照表

> b5 来源：[Alheimsins/b5-result-text](https://github.com/Alheimsins/b5-result-text)（MIT）
> 我们来源：`backend/data/interpretations_en.json`
>
> b5 结构：`shortDescription` + `results`（high / neutral / low 各 1 句）
> 我们结构：`title` + `body`（high / low / medium 各 2-3 句）

---

## O — Openness

### 定义
| | b5 shortDescription | 我们（无对应，定义不显示给用户） |
|---|---|---|
| | *"Openness describes a dimension of cognitive style that distinguishes imaginative, creative people from down-to-earth, conventional people."* | — |

### high
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Openness is high, indicating you enjoy novelty, variety, and change. You are curious, imaginative, and creative. | You are curious, imaginative, and open to new experiences. You enjoy exploring abstract ideas, art, and unconventional ways of living. You have a rich inner life and are drawn to novelty, whether it's traveling to new places or learning about different cultures. |

### low  
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Openness is low, indicating you like to think in plain and simple terms. Others describe you as down-to-earth, practical, and conservative. | You prefer the familiar and the practical. You are down-to-earth, focusing on what's tangible and useful rather than abstract or speculative ideas. You like routine and tradition, and are more comfortable with tried-and-true approaches than experimental ones. |

### neutral / medium
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Openness is average, indicating you enjoy tradition but are willing to try new things. Your thinking is neither simple nor complex. To others you appear to be a well-educated person but not an intellectual. | You have a well-rounded level of Openness to Experience. You're curious enough to explore new ideas but practical enough to stay grounded. You appreciate novelty without being easily distracted by every new trend, finding a comfortable middle ground between tradition and innovation. |

---

## C — Conscientiousness

### 定义
| | b5 shortDescription | 我们 |
|---|---|---|
| | *"Conscientiousness concerns the way in which we control, regulate, and direct our impulses."* | — |

### high
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 4 句 |
| 正文 | Your score on Conscientiousness is high. This means you set clear goals and pursue them with determination. People regard you as reliable and hard-working. | You are organized, disciplined, and reliable. You set high standards for yourself and work diligently to achieve your goals. Your self-control and ability to plan ahead help you succeed in school, work, and personal projects. Others see you as responsible and dependable. |

### low
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Conscientiousness is low, indicating you like to live for the moment and do what feels good now. Your work tends to be careless and disorganized. | You prefer a spontaneous and flexible lifestyle. You dislike being tied down by strict schedules or rigid plans. While you may be seen as disorganized at times, your flexibility makes you adaptable to change and better at living in the moment. |

### neutral / medium
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Conscientiousness is average. This means you are reasonably reliable, organized, and self-controlled. | You have a healthy mix of discipline and flexibility when it comes to Conscientiousness. You can be organized and focused when needed, but you also know when to be flexible and go with the flow. This adaptability lets you work hard without burning out. |

---

## E — Extraversion

### 定义
| | b5 shortDescription | 我们 |
|---|---|---|
| | *"Extraversion is marked by pronounced engagement with the external world."* | — |

### high
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Extraversion is high, indicating you are sociable, outgoing, energetic, and lively. You prefer to be around people much of the time. | You are energetic, outgoing, and thrive in social settings. You enjoy being around people, making new friends, and being the center of attention. You tend to be positive and enthusiastic, bringing energy to group situations. |

### low
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Extraversion is low, indicating you are introverted, reserved, and quiet. You enjoy solitude and solitary activities. Your socialization tends to be restricted to a few close friends. | You prefer quiet, low-key environments and find too much social stimulation draining rather than energizing. You value deeper one-on-one connections over large social circles. Your rich inner life sustains you, and you're selective about where you invest your social energy. |

### neutral / medium
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Extraversion is average, indicating you are neither a subdued loner nor a jovial chatterbox. You enjoy time with others but also time alone. | Your Extraversion sits comfortably in the middle range. You're at ease in social settings but also value your alone time. You can be outgoing when the situation calls for it, yet you don't depend on constant social stimulation. |

---

## A — Agreeableness

### 定义
| | b5 shortDescription | 我们 |
|---|---|---|
| | *"Agreeableness reflects individual differences in concern with cooperation and social harmony. Agreeable individuals value getting along with others."* | — |

### high
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your high level of Agreeableness indicates a strong interest in others' needs and well-being. You are pleasant, sympathetic, and cooperative. | You are compassionate, trusting, and cooperative. You value harmony in relationships and go out of your way to help others. People find you warm, kind, and easy to get along with. You believe the best in others and avoid unnecessary conflict. |

### low
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Agreeableness is low, indicating less concern with others' needs than with your own. People see you as tough, critical, and uncompromising. | You are more self-oriented and less concerned with pleasing others. You make decisions based on your own needs and aren't afraid of conflict. This assertiveness serves you well in competitive environments, though others may find you challenging to work with. |

### neutral / medium
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your level of Agreeableness is average, indicating some concern with others' Needs, but, generally, unwillingness to sacrifice yourself for others. | Your Agreeableness falls in a well-adjusted middle zone. You care about others' feelings but also know how to stand your ground when necessary. You navigate cooperation and self-assertion with reasonable ease. |

---

## N — Neuroticism

### 定义
| | b5 shortDescription | 我们 |
|---|---|---|
| | *"Neuroticism refers to the tendency to experience negative feelings."* | — |

### high
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Neuroticism is high, indicating that you are easily upset, even by what most people consider the normal demands of living. People consider you to be sensitive and emotional. | You are prone to experiencing negative emotions like anxiety, worry, anger, and sadness. You are sensitive to stress and may find everyday challenges overwhelming at times. However, this sensitivity also gives you deep emotional awareness and can be a wellspring of creativity. |

### low
| | b5 | 我们 |
|---|---|---|
| 句式 | 1 句 | 3 句 |
| 正文 | Your score on Neuroticism is low, indicating that you are exceptionally calm, composed and unflappable. You do not react with intense emotions, even to situations that most people would describe as stressful. | You are emotionally stable and resilient. You stay calm under pressure and don't get easily upset by life's challenges. Your steady mood and positive outlook make you a source of stability for those around you. |

### neutral / medium
| | b5 | 我们 |
|---|---|---|
| 句式 | 2 句 | 3 句 |
| 正文 | Your score on Neuroticism is average, indicating that your level of emotional reactivity is typical of the general population. Stressful and frustrating situations are somewhat upsetting to you, but you are generally able to get over these feelings and cope with these situations. | You have a moderate level of Neuroticism. You experience normal ups and downs in your emotions, but you generally recover well from stress and setbacks. Your emotional responses are proportionate to situations. |

---

## 差异总结

| 维度 | b5 | 我们 |
|------|-----|------|
| **粒度** | 1-2 句/tier | 3-4 句/tier |
| **句式** | "Your score on X is Y, indicating..." 固定模板 | 自由句式 "You are / You prefer / You have..." |
| **low 分态度** | 陈述事实，有时偏负面（careless/disorganized/compromising） | 积极重构（focus/adaptable/serves you well） |
| **neutral/medium** | 偏"平均=平庸"（neither X nor Y） | 偏"平衡=适应优势"（balanced/flexible/well-adjusted） |
| **high/low 对照** | 简单罗列特质 | 描述行为 + 场景优势 |
| **b5 特有** | shortDescription（定义句）+ description（学术段落） | 无 |
| **我们特有** | — | facet 分层解读（30×3=90 条） |

## 可借鉴点

1. **N neutral**：b5 写法 "your level of emotional reactivity is typical of the general population" 比我们的 "moderate level of Neuroticism" 更易理解
2. **E low**：b5 "Your socialization tends to be restricted to a few close friends" 更直观
3. **C low**：b5 "like to live for the moment" 比 "prefer a spontaneous lifestyle" 更口语化
4. **O neutral**：b5 "neither simple nor complex" 这个表达简洁有力
5. **定义句**：b5 shortDescription 可考虑加入报告作为域级说明（不在本文案文件中，另议）
