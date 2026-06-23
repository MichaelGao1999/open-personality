# task-M05: 彩蛋引擎 (Easter Egg)

> 对应文档：`docs/design.md` §6.3 彩蛋引擎接口 · `docs/design.md` §9.3 彩蛋 JSON 格式 · `docs/proposal.md` §11 彩蛋设计
> 路径：`backend/app/core/easter_egg.py`

---

## 依赖

- **前置**：DATA-09（彩蛋文案 JSON，含 condition 字段）
- **后置**：M04（报告生成依赖本模块结果）
- **调用方**：M07 API 层（传 scoring/MBTI/mode 给 trigger）

---

## 子任务

### M05-01 彩蛋文案加载 [P1]

- 读取 `easter_eggs.json`
- 解析短文案数组 + 中等彩蛋数组
- 每条蛋含 `id`, `zh`, `en`, `condition` 字段
- 按语言（zh/en）索引，便于按 lang 随机选取

### M05-02 分层概率判定 [P1]

- 实现 `_TRIGGER_RATES = {"standard": 0.5, "speed": 0.1}`
- `_roll(mode: str = "standard") -> bool`
- standard 模式 50% 触发率，speed 模式 10% 触发率
- advanced 模式由调用方传入 `force=True` 绕过概率判定
- 使用 `random.random()` 判定
- 可选 seed 参数实现可重现测试

### M05-03 条件选取彩蛋 [P1]

- 实现 `_pick_conditional(lang, scoring, mbti, mode) -> str`
- 遍历蛋池，对每条蛋调用 `_match_condition` 筛选
- 无 scoring/MBTI 数据时回退到全部蛋均可选（向后兼容）
- 候选池为空时返回空字符串（防御性兜底）
- 短文案与中等彩蛋同等权重选取

### M05-04 触发/未触发流程 [P1]

- `trigger(lang="zh", seed=None, force=False, scoring=None, mbti=None, mode="standard") -> str | None`
- force=True → 跳过概率判定，直接进入条件选取
- 概率未命中 → 返回 None
- 命中 → 条件筛选 → 候选池非空则返回文案，为空则 None

### M05-05 测试：触发率 [P1]

- 1000 次 speed 模式调用，触发率在 5%~15% 之间
- 使用固定 seed 验证可重现
- force=True 测试 100 次全部触发

### M05-06 测试：输出正确性 [P1]

- 触发时返回 str 且非空
- 未触发时返回 None
- 验证 zh 和 en 语言输出正确
- 无 scoring/MBTI 输入时仍可正常触发（向后兼容）

### M05-07 条件匹配引擎 [P1]

- 实现 `_match_condition(condition: dict, scoring, mbti, mode: str) -> bool`
- 递归求值，支持条件类型（共 20+）：
  - domain/facet 阈值（ge/le）
  - highest_domain / lowest_domain / highest_facet / lowest_facet
  - mbti（精确匹配）、mbti_in（多选）、mbti_dim（轴偏好+置信度）
  - mbti_confidence_ge / mbti_confidence_le
  - mode / mode_in
  - flat（全域 45-55）
  - and / or / not 复合条件
- 空 condition 返回 True（无条件=始终可选）

### M05-08 全覆盖画像测试 [P1]

- 13 种画像类型全部验证：5 域各高（ge:55）+ 5 域各低（le:45）+ 平坦 + advanced + speed
- 边界测试：ge:55 临界值、le:45 临界值、flat 上下界（45/55 包含）

---

## 接口签名

```python
class EasterEggEngine:
    _TRIGGER_RATES = {"standard": 0.5, "speed": 0.1}

    def __init__(self, data_dir: str | None = None): ...
    def trigger(
        self,
        lang: str = "zh",
        seed: str | None = None,
        force: bool = False,
        scoring: ScoringResult | None = None,
        mbti: MBTIResult | None = None,
        mode: str = "standard",
    ) -> str | None: ...
    def _roll(self, mode: str = "standard") -> bool: ...
    def _match_condition(self, condition: dict, scoring, mbti, mode: str) -> bool: ...
    def _pick_conditional(self, lang: str, scoring, mbti, mode: str) -> str: ...
```

---

## 测试点

| 测试项 | 覆盖 |
|--------|------|
| speed 模式 1000 次触发率 5-15% | M05-05 |
| force=True 100% 触发 | M05-05 |
| 触发返回非空字符串 | M05-06 |
| 未触发返回 None | M05-06 |
| 选中文案语言正确 | M05-06 |
| 无 scoring/MBTI 时向后兼容 | M05-06 |
| 无 condition 时始终可选 | M05-07 |
| domain 阈值（ge/le 边界） | M05-07 |
| highest/lowest domain/facet | M05-07 |
| MBTI 精确匹配/多选/维度置信度 | M05-07 |
| mode/mode_in/flat | M05-07 |
| and/or/not 复合条件 | M05-07 |
| 13 种画像全部命中 | M05-08 |
| ge:55/le:45/flat 边界值 | M05-08 |
