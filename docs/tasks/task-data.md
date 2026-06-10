# task-data: 数据文件准备

> 对应文档：`docs/design.md` §9 数据文件格式

---

## 依赖

- **前置**：无
- **后置**：M01（问卷加载）、M02（维度映射）、M03（MBTI 权重）、M04（解读模板）、M05（彩蛋）

---

## 子任务

### DATA-01 IPIP-120 中文题目 JSON [P1]

- 文件：`backend/data/items/ipip120_zh.json`
- 120 条大五人格题目（中文翻译版，参考学术界已有翻译）
- 每题含：`item_id`, `dimension`, `facet`, `text`, `reversed`
- metadata: mode=standard, total_items=120, lang=zh
- 确认每条题目都有对应的 dimension 和 facet

### DATA-02 IPIP-120 英文题目 JSON [P1]

- 文件：`backend/data/items/ipip120_en.json`
- 与 DATA-01 同结构，text 字段为英文原版
- 英文原版来自 IPIP Public Domain

### DATA-03 IPIP-300 中文题目 JSON [P2]

- 文件：`backend/data/items/ipip300_zh.json`
- 300 条（高级模式），结构同上
- metadata: mode=advanced, total_items=300

### DATA-04 IPIP-300 英文题目 JSON [P2]

- 文件：`backend/data/items/ipip300_en.json`
- 结构同上，英文

### DATA-05 MBTI 映射权重 JSON [P1]

- 文件：`backend/data/mbti_mapping.json`
- 基于 McCrae & Costa (1989) 的回归权重
- 结构：每对 MBTI 维度（E_I, S_N, T_F, J_P）的 formula + weights + bias
- weights 的 key 为大五 domain/facet 名称，value 为权重系数

### DATA-06 常模数据 JSON [P1]

- 文件：`backend/data/norms.json`
- T-score 标准化所需的均值和标准差
- 5 个域 + 30 个子维度各自的 Mean 和 SD
- 注意：IPIP-120 和 IPIP-300 可能使用不同常模

### DATA-07 中文解读模板 JSON [P1]

- 文件：`backend/data/interpretations_zh.json`
- 每个域（O/C/E/A/N）的高分解读 + 低分解读
- 每个 facet（30 个）的高分解读 + 低分解读
- 格式：`{ "O": { "high": { "title": "...", "body": "..." }, "low": { ... } }, ... }`

### DATA-08 英文解读模板 JSON [P1]

- 文件：`backend/data/interpretations_en.json`
- 与 DATA-07 结构一致，英文

### DATA-09 彩蛋文案 JSON [P1]

- 文件：`backend/data/easter_eggs.json`
- 10~15 条短文案 + 3~5 条中等彩蛋
- 每条含：`id`, `zh`, `en`
- trigger_rate: 0.1

---

## 数据完整性校验

| 检查项 | 覆盖 |
|--------|------|
| IPIP-120：正好 120 条，无重复 item_id | DATA-01, DATA-02 |
| IPIP-300：正好 300 条，无重复 item_id | DATA-03, DATA-04 |
| 所有 item_id 格式一致（ipip_001 ~ ipip_120） | DATA-01~04 |
| 所有 dimension 值在 {O,C,E,A,N} 内 | DATA-01~04 |
| 所有 facet 值符合命名规范（{domain}_{facet_name}） | DATA-01~04 |
| MBTI 权重映射覆盖全部 4 对维度 | DATA-05 |
| 常模数据覆盖所有 domain + facet | DATA-06 |
| 解读模板覆盖所有 domain + facet 的高/低分 | DATA-07, DATA-08 |
| JSON 文件格式正确（`python -m json.tool` 验证） | 全部 |
| 彩蛋 zh/en 字段均非空 | DATA-09 |

---

## 注意事项

- IPIP 题目为 Public Domain，无需版权授权
- 中文版可参考学术文献（如戴晓阳等的中文版 IPIP-NEO）加入趣味性微调
- MBTI 映射权重的值只是学界估计，后续可校准，默认用 McCrae & Costa (1989) 论文披露的近似值
- 常模数据初期可用预设值（M=50, SD=10），或从公开文献获取
- 解读模板初始版本不必完美，后续可迭代完善
