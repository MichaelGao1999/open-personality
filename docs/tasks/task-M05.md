# task-M05: 彩蛋引擎 (Easter Egg)

> 对应文档：`docs/design.md` §6.3 彩蛋引擎接口 · `docs/proposal.md` §11 彩蛋设计
> 路径：`backend/app/core/easter_egg.py`

---

## 依赖

- **前置**：DATA-09（彩蛋文案 JSON）
- **后置**：M04（报告生成依赖本模块结果）
- **调用方**：M07 API 层

---

## 子任务

### M05-01 彩蛋文案加载 [P1]

- 读取 `easter_eggs.json`
- 解析短文案数组 + 中等彩蛋数组
- 按语言（zh/en）索引，便于按 lang 随机选取

### M05-02 概率判定 [P1]

- 实现 `_roll() -> bool`
- 基于种子决定是否触发（默认 10% 触发率）
- 使用 `random.random()` 判定
- 可选 seed 参数实现可重现测试

### M05-03 随机选取彩蛋 [P1]

- 实现 `_pick(lang: str) -> str`
- 从彩蛋池中随机选取一条
- 优先选取短文案，中等彩蛋概率较低

### M05-04 触发/未触发流程 [P1]

- `trigger(seed=None) -> str | None`
- 未触发 → 返回 None
- 触发 → 返回选中彩蛋文案

### M05-05 测试：触发率 [P1]

- 1000 次调用，统计触发次数
- 触发率在 7%~13% 之间（10% ± 3%）
- 使用固定 seed 验证可重现

### M05-06 测试：输出正确性 [P1]

- 触发时返回 str 且非空
- 未触发时返回 None
- 验证 zh 和 en 语言输出正确

---

## 接口签名

```python
class EasterEggEngine:
    def __init__(self, eggs_config: dict): ...
    def trigger(self, seed: str | None = None) -> str | None: ...
    def _roll(self) -> bool: ...
    def _pick(self, lang: str) -> str: ...
```

---

## 测试点

| 测试项 | 覆盖 |
|--------|------|
| 1000 次调用触发率 ≈ 10% | M05-05 |
| 触发返回非空字符串 | M05-06 |
| 未触发返回 None | M05-06 |
| 选中文案语言正确 | M05-06 |
| 固定 seed 结果可重现 | M05-05 |
