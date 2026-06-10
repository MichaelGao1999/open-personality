# task-M07: API 层 (API Layer)

> 对应文档：`docs/design.md` §4 接口契约 · §12 错误处理策略
> 路径：`backend/app/api/{questionnaire.py, report.py}` · `backend/app/schemas/models.py`

---

## 依赖

- **前置**：M01（问卷加载）、M02（计分引擎）、M03（MBTI 推断）、M04（报告生成）、M05（彩蛋引擎）、M06（持久化层）
- **后置**：M08（前端视图依赖本层 API）
- **调用方**：前端浏览器（HTTP）

---

## 子任务

### M07-01 FastAPI 应用初始化 + CORS [P1]

- 复用 INFRA-04 的 main.py
- 添加 CORS middleware（允许 `http://localhost:5173`）
- 配置全局异常处理器
- 添加请求日志 + 响应时间（可选 middleware）

### M07-02 GET /api/questionnaires/items [P1]

- 参数：`mode`（默认 standard）、`lang`（默认 zh）
- 调用 M01-01 加载题目列表
- 返回 `{ items: QuestionnaireItem[] }`
- 错误：无效 mode → 422

### M07-03 POST /api/questionnaires/submit [P1]

- 接收 `SubmitRequest`（mode, lang, answers）
- 校验顺序：数量 → 值范围（M01-03, M01-04）
- 调用 M02 → M03 → M05 → M04 串联执行
- 调用 M06-04 事务保存
- 返回完整 Report

### M07-04 GET /api/report/{share_token} [P1]

- 调用 M06-05 查询
- 命中 → 返回 Report
- 未命中 → 404 `{ error: "report_not_found" }`

### M07-05 GET /api/i18n/{lang} [P1]

- 读取前端 UI 语言包 JSON
- 返回 `{ [key]: string }` 字典
- 语言包文件由 M08-05 准备，API 层直接读取文件目录

### M07-06 请求入参校验 [P1]

- 使用 Pydantic model 做请求校验
- `SubmitRequest`: mode 只能是 standard/advanced, lang 只能是 zh/en
- `AnswerItem`: item_id 非空, value 1-5

### M07-07 错误处理中间件 [P1]

- 统一异常处理器：
  - `ValueError` → 422
  - `ReportNotFoundError` → 404
  - `ScoringError` → 500
  - 其他未预期异常 → 500 + 日志记录
- 响应格式：`{ "error": "error_code", "detail": "..." }`

### M07-08 集成测试：完整流程 [P1]

- 提交 IPIP-120 固定答案 → 验证返回 Report 结构完整
- 取 share_token → GET /api/report/{token} 验证一致性

### M07-09 集成测试：错误场景 [P1]

- 提交 119 条答案 → 422
- 提交 value=6 的答案 → 422
- 查询不存在的 token → 404
- 无效 lang → 422

### M07-10 OpenAPI 文档 [P2]

- 确保 FastAPI 自动生成 `/docs` 和 `/redoc` 页面
- 为各端点添加 summary, description, response model 装饰
- 添加 tags 分组

---

## 请求/响应汇总

| 方法 | 路径 | 请求 | 响应 (200) | 错误 |
|------|------|------|-----------|------|
| GET | /api/questionnaires/items | Query: mode, lang | `{ items: QuestionnaireItem[] }` | 422 |
| POST | /api/questionnaires/submit | Body: SubmitRequest | Report | 422 |
| GET | /api/report/{share_token} | Path: share_token | Report | 404 |
| GET | /api/i18n/{lang} | Path: lang | `{ [key]: string }` | 404 |

---

## 测试点

| 测试项 | 覆盖 |
|--------|------|
| 提交 → 返回完整 Report | M07-08 |
| share_token 一致 | M07-08 |
| 答案数量不符 422 | M07-09 |
| 答案越界 422 | M07-09 |
| 无效 token 404 | M07-09 |
| 题目列表返回正确数量 | M07-02 |
| i18n 返回有效 JSON | M07-05 |
| OpenAPI 文档可访问 | M07-10 |
