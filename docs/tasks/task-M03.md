# task-M03: MBTI 推断 (MBTI Inference)

> 对应文档：`docs/design.md` §6.2 MBTI 推断接口 · `docs/proposal.md` §9 MBTI 概率化映射方案
> 路径：`backend/app/core/mbti.py`

---

## 依赖

- **前置**：DATA-05（MBTI 映射权重）、M02（依赖 ScoringResult 作为输入）
- **后置**：M04（报告生成依赖本模块结果）
- **调用方**：M04 或 M07

---

## 子任务

### M03-01 权重配置加载 [P1]

- 读取 `mbti_mapping.json`
- 解析 4 对维度的权重配置（E/I, S/N, T/F, J/P）
- 验证配置完整性：每对维度必须有 formula, weights, bias

### M03-02 Sigmoid 校准函数 [P1]

- 实现 `_sigmoid(x: float) -> float`
- 标准 sigmoid 函数：`1 / (1 + exp(-x))`
- 测试：x=0 → 0.5, x→∞ → 1, x→-∞ → 0

### M03-03 E/I 维度概率计算 [P1]

- 从 ScoringResult 中取出相关 domain/facet 分数
- 按权重加权求和，通过 sigmoid 映射到 [0,1]
- 返回 (p_E, p_I)，且 p_E + p_I = 1

### M03-04 S/N 维度概率计算 [P1]

- 同上，使用 S/N 对应权重

### M03-05 T/F 维度概率计算 [P1]

- 同上，使用 T/F 对应权重

### M03-06 J/P 维度概率计算 [P1]

- 同上，使用 J/P 对应权重

### M03-07 置信度计算 + MBTIResult 组装 [P1]

- 置信度公式：`1 - |p_a - 0.5| * 2`（越接近 0.5 越不确定）
- 硬分类 type_code：选概率高的那个字母（仅用于展示，不对外承诺）
- 组装 MBTIResult（4 对维度 + confidence + type_code）

### M03-08 测试：概率合理性 [P1]

- E 域高分 → E/I 中 E 概率 > 0.5
- 全部中立 → 4 对概率都在 0.4~0.6 区间
- 边界情况：极端分数 → 概率接近 1 或 0

---

## 接口签名

```python
class MBTIInference:
    def __init__(self, mapping_config: dict): ...
    def infer(self, big_five_scores: ScoringResult) -> MBTIResult: ...
    def _sigmoid(self, x: float) -> float: ...
    def _compute_dimension(self, scores, weights) -> tuple[float, float]: ...
    def _confidence(self, prob_a: float, prob_b: float) -> float: ...
```

---

## 测试点

| 测试项 | 覆盖 |
|--------|------|
| 已知大五分数 → MBTI 概率合理 | M03-08 |
| E 高分 → E 概率 > 0.5 | M03-08 |
| 中立分数 → 概率接近 0.5 | M03-08 |
| 极端分数 → 概率接近 1.0 | M03-08 |
| 4 对维度概率 p_a + p_b = 1 | M03-03~06 |
| 置信度在 0~1 范围 | M03-07 |
| sigmoid(0) = 0.5 | M03-02 |
