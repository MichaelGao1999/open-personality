#!/usr/bin/env python3
"""
从 docs/interpretation-content-draft.md 中提取解读文案，
写入 backend/data/interpretations_zh.json。
"""
import json
import re

with open("docs/interpretation-content-draft.md", "r", encoding="utf-8") as f:
    md = f.read()

# 按 ### 分割成块
sections = md.split("\n### ")

result = {}

for section in sections:
    if not section.strip():
        continue

    # 第一行是 KEY 和标题
    first_line = section.split("\n")[0]
    m = re.match(r"^([\w_]+)\s*[—\-]\s*(.+)", first_line)
    if not m:
        continue
    key = m.group(1).strip()

    # 提取高分
    high_match = re.search(
        r'\*\*高分\*\*\s*[—\-]+\s*`([^`]+)`[：:]\s*\n+((?:>\s*.+\n?)+)',
        section
    )
    high_title = high_match.group(1) if high_match else f"{key}偏高"
    high_body = re.sub(r'^>\s*', '', high_match.group(2), flags=re.MULTILINE).strip() if high_match else ""

    # 提取低分
    low_match = re.search(
        r'\*\*低分\*\*\s*[—\-]+\s*`([^`]+)`[：:]\s*\n+((?:>\s*.+\n?)+)',
        section
    )
    low_title = low_match.group(1) if low_match else f"{key}偏低"
    low_body = re.sub(r'^>\s*', '', low_match.group(2), flags=re.MULTILINE).strip() if low_match else ""

    if high_body or low_body:
        result[key] = {
            "high": {"title": high_title, "body": high_body},
            "low": {"title": low_title, "body": low_body}
        }
        print(f"  {key}: high={len(high_body)}ch low={len(low_body)}ch")

# 写入
with open("backend/data/interpretations_zh.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ Written {len(result)} items")

# 验证完整性
expected = [
    "O", "O_imagination", "O_aesthetics", "O_feelings", "O_adventurousness", "O_intellect", "O_liberalism",
    "C", "C_self_efficacy", "C_orderliness", "C_dutifulness", "C_achievement_striving", "C_self_discipline", "C_cautiousness",
    "E", "E_friendliness", "E_gregariousness", "E_assertiveness", "E_activity_level", "E_excitement_seeking", "E_cheerfulness",
    "A", "A_trust", "A_morality", "A_altruism", "A_cooperation", "A_modesty", "A_sympathy",
    "N", "N_anxiety", "N_anger", "N_depression", "N_self_consciousness", "N_immoderation", "N_vulnerability"
]
missing = [k for k in expected if k not in result]
extra = [k for k in result if k not in expected]
if missing:
    print(f"❌ MISSING: {missing}")
if extra:
    print(f"⚠️  EXTRA: {extra}")
if not missing and not extra:
    print("✅ All 35 items present, no extras")
