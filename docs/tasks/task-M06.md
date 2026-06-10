# task-M06: 持久化层 (Persistence)

> 对应文档：`docs/design.md` §5 数据库设计 · §6.5 持久化层接口 · §5.3 分享机制
> 路径：`backend/app/db/{database.py, models.py, repository.py}`

---

## 依赖

- **前置**：INFRA-07（数据库初始化）
- **后置**：M07（API 层依赖本模块保存/查询数据）
- **调用方**：M07 API 层

---

## 子任务

### M06-01 SQLAlchemy ORM 模型 [P1]

- 定义三个模型：`SessionORM`, `AnswerORM`, `ReportORM`
- 对应 `sessions`, `answers`, `reports` 三张表
- 字段与 design.md §5.2 的 DDL 一致
- session_id 为 UUID 字符串
- 外键关系：sessions → answers（一对多）, sessions → reports（一对一）

### M06-02 数据库引擎初始化 [P1]

- `database.py`：创建 SQLAlchemy async engine 或 sync engine
- 实现 `get_db()` 依赖注入（FastAPI `Depends`）
- 启动时调用 `Base.metadata.create_all()` 自动建表

### M06-03 share_token 生成 [P1]

- 实现 `generate_share_token() -> str`
- 8 位 base62 字符集：`0-9a-zA-Z`
- 使用 `secrets.token_urlsafe` + 字符映射

### M06-04 save_complete_session 事务方法 [P1]

- 实现 `ReportRepository.save_complete_session(session, answers, report)`
- 单一事务：insert session → bulk insert answers → insert report → commit
- 任一失败 → rollback，不留孤儿数据
- 返回 session_id

### M06-05 get_report_by_token 查询 [P1]

- 实现 `ReportRepository.get_report_by_token(share_token) -> Report | None`
- JOIN 查询：sessions + answers + reports
- 命中 → 组装为 Report 对象
- 未命中 → 返回 None

### M06-06 事务回滚测试 [P1]

- 模拟中间步骤写入失败
- 验证数据库中未残留部分数据
- 使用 SQLite 内存数据库测试

### M06-07 查询命中/未命中测试 [P1]

- 插入一条记录 → 通过 share_token 查询命中文档
- 查询不存在的 token → 返回 None

### M06-08 高并发无碰撞测试 [P2]

- 批量插入 10000 条 session
- 验证无 share_token 重复

---

## 关键设计约束

> **事务规则**（来自 design.md §6.5）：
> 数据库写入只有一个入口——`save_complete_session`。计算成功前绝不碰数据库，计算成功后一次事务写入全部数据。
> 无单独的 `save_session`/`save_answers`/`save_report` 方法，杜绝部分写入导致的孤儿数据。

---

## 接口签名

```python
class ReportRepository:
    def save_complete_session(self, session, answers, report) -> str: ...
    def get_report_by_token(self, share_token: str) -> Report | None: ...
```

---

## 测试点

| 测试项 | 覆盖 |
|--------|------|
| 完整写入后三表数据一致 | M06-04 |
| 中间步骤失败 → 全回滚 | M06-06 |
| share_token 查询命中 | M06-07 |
| share_token 查询未命中返回 None | M06-07 |
| token 不重复 | M06-08 |
| 数据库引擎启动正常 | M06-02 |
