# agent-coding-skeleton — 跨项目决策母库

> 本文件聚合自多个项目的关键设计决策。所有 ADR 均标注来源。
> 母库自身决策标注 `[母库]`。

---

## ADR-028：清理冗余索引脚本，补齐骨架 manifest

| 字段 | 内容 |
|------|------|
| **状态** | Active |
| **日期** | 2026-05-30 |
| **问题** | 骨架完整性审查发现 5 个可改进点：1) 两个索引脚本共存（`build-troubleshooting-index.py` 内容被 `build-experience-index.py` 完全覆盖）；2) `skeleton-manifest.json` 遗漏 `.gitattributes` 和 `config/github-sync.json`；3) `config/github-sync.json` 的 `branch` 硬编码 `main` 但脚本已自适应；4) `templates/` 缺少 `TRIGGERS.md`（仅 `starter/` 有）；5) `opencode.json` Playwright 配置指向已搁置的天猫项目 |
| **候选方案** | A. 全部修复：删除冗余、补齐 manifest、修复死配置、对齐模板、禁用死配置<br>B. 只修一部分 |
| **决策** | **A. 全部修复** |
| **理由** | 骨架作为母库，文件结构的一致性直接影响下游项目质量。冗余索引脚本会误导后续维护者；manifest 遗漏导致新项目初始化时缺文件；死配置分散注意力。一次性修干净，避免债务积累。 |
| **后果** | 正面：母库骨架完整性提升，manifest 与实际基础设施一致。负面：无（均为清理性修改）。 |
| **可逆性** | **高**。被删除的冗余脚本已在 Git 历史中；Playwright 配置仅 `enabled: false` 未删除。 |