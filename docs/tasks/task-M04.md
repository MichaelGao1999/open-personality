# task-M04: 报告生成 (Report Generator)

> 对应文档：`docs/design.md` §6.4 报告生成接口 · §4.2 数据结构
> 路径：`backend/app/core/report_gen.py`

---

## 依赖

- **前置**：DATA-07~08（解读模板）、M02/M03/M05（依赖计分/MBTI/彩蛋的输出）
- **后置**：M06（持久化层保存 Report 对象）
- **调用方**：M07 API 层

---

## 子任务

### M04-01 解读模板加载 [P1]

- 读取 `interpretations_{lang}.json`
- 构建 domain 解读映射 + facet 解读映射
- 缓存两份语言模板

### M04-02 5 域文字解读 [P1]

- 实现 `_build_domain_interpretations(scores, lang) -> list[Interpretation]`
- 根据 T-score 判断高低（阈值：>= 55 高分 / <= 45 低分 / 其余中等）
- 选对应模板，填入具体分数

### M04-03 30 子维度文字解读 [P1]

- 实现 `_build_facet_interpretations(scores, lang) -> list[Interpretation]`
- 同上逻辑，为 30 个子维度生成解读

### M04-04 MBTI 解读文字 [P1]

- 实现 `_build_mbti_interpretation(mbti_result, lang) -> Interpretation`
- 生成一段描述文字说明 MBTI 概率映射结果

### M04-05 Report 对象组装 [P1]

- 组装完整 Report（含 session_id, share_token, scoring, mbti, interpretations, easter_egg, lang, mode, created_at）
- session_id 用 uuid4 生成
- share_token 由调用方传入（M06-03 生成）或由本模块委托

### M04-06 多语言合并 [P1]

- Interpretation 对象同时包含 zh/en 标题和正文
- 确保两种语言都有内容

### M04-07 缺失模板降级 [P2]

- 如果某个 domain/facet 的模板缺失，使用通用占位文案
- 不因模板缺陷导致报告生成失败

### M04-08 测试：完整报告输出 [P1]

- 模拟已知的 ScoringResult + MBTIResult → 验证 Report 结构完整
- 所有字段非空

### M04-09 测试：语言开关 [P1]

- 同一份得分，zh/en 两种语言生成 → 解读文字语言正确
- 评分数据不变

### M04-10 测试：interpretation 非空 [P1]

- 验证所有 domain + facet 都有 interpretation
- 数量：5（域）+ 30（子维度）或 5（标准模式只输出域）

---

## 接口签名

```python
class ReportGenerator:
    def __init__(self, interpretations_config: dict): ...
    def generate(self, scoring, mbti, easter_egg, lang, session_id, mode) -> Report: ...
    def _build_interpretations(self, scoring, lang) -> list[Interpretation]: ...
```

---

## 测试点

| 测试项 | 覆盖 |
|--------|------|
| Report 结构完整（含所有字段） | M04-08 |
| 全部 domain + facet 有解读 | M04-10 |
| 语言切换解读文字正确 | M04-09 |
| 高/中/低分对应不同模板 | M04-08 |
| 彩蛋 null 时 Report 正常 | M04-08 |
| 模板缺失降级不报错 | M04-07 |
