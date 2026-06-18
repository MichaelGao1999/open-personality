#!/usr/bin/env python3
"""
迁移数据库中的旧报告：重新生成 interpretations，写入新的 body_high/low 字段。

先在测试环境验证，再在生产环境运行。
"""
import json
import sys
import os

# 确保能找到 backend 模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.db.models import Report as DBReport  # type: ignore[import-not-found]
from backend.app.core.report_gen import ReportGenerator  # type: ignore[import-not-found]
from backend.app.schemas.models import ScoringResult, MBTIResult  # type: ignore[import-not-found]

# ---------- 数据库连接 ----------
# 从环境变量读取，或直接填写
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

generator = ReportGenerator()

updated = 0
failed = 0

reports = db.query(DBReport).all()
print(f"Found {len(reports)} reports to process")

for report in reports:
    try:
        # 解析已有的 scoring 和 mbti 数据
        scoring_dict = json.loads(report.big_five_scores)
        mbti_dict = json.loads(report.mbti_result)

        # 重建为 Pydantic 模型（scoring 和 mbti 的结构没变）
        # scoring 需要解析成 ScoringResult
        scoring = ScoringResult(**scoring_dict)
        mbti = MBTIResult(**mbti_dict)

        # 从 session 获取 lang
        from backend.app.db.models import Session as DBSession  # type: ignore[import-not-found]
        session = db.query(DBSession).filter(
            DBSession.id == report.session_id
        ).first()
        lang = session.lang if session else "zh"

        # 重新生成 interpretations（使用当前代码，包含 body_high/low）
        interpretations_data = generator._load_interpretations(lang)
        interpretations_en = generator._load_interpretations("en")

        new_interpretations = []

        # 域级
        for dim in ["O", "C", "E", "A", "N"]:
            dim_data = interpretations_data.get(dim, {})
            t_score = scoring.t_scores.get(dim, 50.0)
            title_zh, body_zh = generator._interpret_domain(
                t_score, dim_data.get("high", {}), dim_data.get("low", {})
            )
            en_data = interpretations_en.get(dim, {})
            title_en, body_en = generator._interpret_domain(
                t_score, en_data.get("high", {}), en_data.get("low", {})
            )
            new_interpretations.append({
                "dimension": dim,
                "title_zh": title_zh,
                "title_en": title_en,
                "body_zh": body_zh,
                "body_en": body_en,
                "body_high_zh": dim_data.get("high", {}).get("body", ""),
                "body_low_zh": dim_data.get("low", {}).get("body", ""),
                "body_high_en": en_data.get("high", {}).get("body", ""),
                "body_low_en": en_data.get("low", {}).get("body", ""),
            })

        # 子维度
        for facet_key in sorted(scoring.facet_scores.keys()):
            dim_data = interpretations_data.get(facet_key, {})
            f_score = scoring.facet_scores.get(facet_key, 50.0)
            title_zh, body_zh = generator._interpret_domain(
                f_score, dim_data.get("high", {}), dim_data.get("low", {})
            )
            en_data = interpretations_en.get(facet_key, {})
            title_en, body_en = generator._interpret_domain(
                f_score, en_data.get("high", {}), en_data.get("low", {})
            )
            new_interpretations.append({
                "dimension": facet_key,
                "title_zh": title_zh,
                "title_en": title_en,
                "body_zh": body_zh,
                "body_en": body_en,
                "body_high_zh": dim_data.get("high", {}).get("body", ""),
                "body_low_zh": dim_data.get("low", {}).get("body", ""),
                "body_high_en": en_data.get("high", {}).get("body", ""),
                "body_low_en": en_data.get("low", {}).get("body", ""),
            })

        report.interpretations = json.dumps(new_interpretations, ensure_ascii=False)
        updated += 1

        if updated % 10 == 0:
            print(f"  Progress: {updated}/{len(reports)}")

    except Exception as e:
        print(f"  FAILED: session_id={report.session_id}: {e}")
        failed += 1

db.commit()
db.close()
print(f"\nDone: {updated} updated, {failed} failed")
