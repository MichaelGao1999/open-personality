# task-M02: 计分引擎 (Scoring Engine)

> 对应文档：`docs/design.md` §6.1 计分引擎接口 · §11.2 关键测试场景
> 路径：`backend/app/core/scoring.py`

---

## 依赖

- **前置**：DATA-01~04（维度映射依赖题目 JSON）、DATA-06（常模数据）
- **后置**：M03（MBTI 推断依赖本模块的输出）、M04（报告生成依赖本模块结果）
- **调用方**：M07 API 层直接调用

---

## 子任务

### M02-01 维度映射配置 [P1]

- 从题目 JSON 元数据构建维度 → 题目列表映射
- 构建 5 个域（O/C/E/A/N）各自的题目 ID 集合
- 构建 30 个子维度各自的题目 ID 集合
- 存储为 dict 结构供计分时直接使用

### M02-02 反向计分逻辑 [P1]

- 实现 `_reverse_score(value: int) -> int`
- 公式：`6 - value`（1↔5, 2↔4, 3 不变）
- 从题目配置中读取 `reversed` 标记
- 只对标记为 reversed 的题目做反转

### M02-03 原始分计算：5 域 [P1]

- 实现 `_compute_raw_scores(answers, dimension_map) -> dict[str, float]`
- 按域（O/C/E/A/N）汇总各题得分（含反向计分）
- 返回 5 个域的原始分

### M02-04 原始分计算：30 子维度 [P1]

- 同上，但按 facet 维度汇总
- 返回 30 个子维度的原始分
- 高级模式（IPIP-300）才有完整 30 子维度数据

### M02-05 T-score 标准化 [P1]

- 实现 `_normalize(raw_scores, norms) -> dict[str, float]`
- 公式：`T = 10 * (raw - mean) / sd + 50`
- 读取 `norms.json` 中的 Mean/SD 配置
- 同时处理 5 域 + 30 子维度的标准化

### M02-06 ScoringResult 组装 [P1]

- 组装 `ScoringResult`（`raw_scores`, `t_scores`, `facet_scores`）
- 返回给调用方

### M02-07 固定种子答案测试 [P1]

- 准备已知答案的固定数据集
- 验证输出分数与预期值一致（精确到小数点后 1 位）
- 包括 5 域和 30 子维度

### M02-08 边界测试 [P1]

- 全部选 1 → 所有域得分在最低区间
- 全部选 5 → 所有域得分在最高区间
- 全部选 3（中立）→ 所有域得分在中间区间
- 交替 1-5 → 分数在合理区间

### M02-09 无效数据容错 [P2]

- 包含未知 item_id 的答案 → 跳过不报错
- 空答案列表 → 抛出明确异常

### M02-10 性能基准 [P2]

- 标准模式（120 题）计分耗时 < 50ms
- 高级模式（300 题）计分耗时 < 100ms

---

## 接口签名

```python
class ScoringEngine:
    def __init__(self, items_config: dict): ...
    def calculate(self, answers: list[AnswerItem], mode: str) -> ScoringResult: ...
    def _compute_raw_scores(self, answers, dimension_map) -> dict[str, float]: ...
    def _normalize(self, raw_scores, norms) -> dict[str, float]: ...
```

---

## 测试点

| 测试项 | 覆盖 |
|--------|------|
| 已知答案 → 预期分数一致 | M02-07 |
| 反向计分正确反转 | M02-07 |
| 全 1/全 5/全 3 结果合理 | M02-08 |
| T-score M=50, SD=10 分布 | M02-07 |
| 空答案抛出异常 | M02-09 |
| 120 题 < 50ms | M02-10 |
