from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Session(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    mode = Column(String, nullable=False)
    lang = Column(String, nullable=False, default="zh")
    status = Column(String, nullable=False, default="complete")  # active | partial | complete
    total_items = Column(Integer, nullable=True)
    share_token = Column(String, unique=True, nullable=False)
    created_at = Column(String, nullable=False)


class Answer(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, nullable=False)
    item_id = Column(String, nullable=False)
    value = Column(Integer, nullable=False)


class Report(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, unique=True, nullable=False)
    big_five_scores = Column(Text, nullable=False)
    mbti_result = Column(Text, nullable=False)
    interpretations = Column(Text, nullable=False)
    easter_egg = Column(String, nullable=True)
    created_at = Column(String, nullable=False)


class Feedback(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(String, nullable=False)
