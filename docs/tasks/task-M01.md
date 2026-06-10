# task-M01: 问卷管理 (Questionnaire)

> 对应文档：`docs/design.md` §4 接口契约 · §9 数据文件格式
> 路径：`backend/app/api/questionnaire.py` · `backend/app/schemas/models.py`

---

## 依赖

- **前置**：DATA-01~04（IPIP 题目 JSON 文件）
- **后置**：M07（API 层依赖本模块提供题目数据）
- **调用方**：M07 API 层

---

## 子任务

### M01-01 问卷加载器 [P1]

- 实现 `QuestionnaireLoader` 类
- 方法 `load_items(mode: str, lang: str) -> list[dict]`
- 根据 `mode`（standard/advanced）和 `lang`（zh/en）读取对应 JSON 文件
- 文件路径通过配置模块获取
- 边界：mode 或 lang 不存在时抛出明确异常

### M01-02 题目缓存 [P2]

- 在加载器内实现 LRU 缓存（`functools.lru_cache` 或手动 dict）
- 避免每次请求都读磁盘
- 缓存 key = `(mode, lang)`

### M01-03 答案数量校验 [P1]

- 实现 `validate_answer_count(answers: list, mode: str)` 函数
- standard → 必须 120 条
- advanced → 必须 300 条
- 数量不匹配 → 抛出 `ValueError` 含详细信息

### M01-04 答案值范围校验 [P1]

- 实现 `validate_answer_values(answers: list[AnswerItem])` 函数
- 每条答案的 value 必须在 1~5 范围内（含两端）
- 越界 → 抛出 `ValueError`，标明是哪条题目

### M01-05 题目列表序列化 [P1]

- 定义 Pydantic schema：`QuestionnaireItem`, `QuestionnaireResponse`
- 将加载的 dict 数据转换为 Pydantic 模型
- 确保 item_id, dimension, facet, text, reversed 字段完整

### M01-06 测试：加载与校验 [P1]

- 测试 `load_items('standard', 'zh')` 返回 120 条
- 测试 `load_items('advanced', 'en')` 返回 300 条
- 测试 `validate_answer_count` 正常/异常情况
- 测试 `validate_answer_values` 正常/边界情况
- 测试无效 mode/lang → 明确错误

---

## 接口签名

```python
class QuestionnaireLoader:
    def load_items(self, mode: str, lang: str) -> list[dict]: ...

def validate_answer_count(answers: list, mode: str) -> None: ...
def validate_answer_values(answers: list[AnswerItem]) -> None: ...
```

---

## 测试点

| 测试项 | 覆盖 |
|--------|------|
| 标准模式返回 120 题 | M01-06 |
| 高级模式返回 300 题 | M01-06 |
| 中/英文各自返回对应语言文本 | M01-06 |
| 答案数量不匹配报错 | M01-06 |
| 答案值越界报错（1-5 范围） | M01-06 |
| 无效 mode/lang 报错 | M01-06 |
| 缓存命中避免重复读文件 | M01-02 验收 |
