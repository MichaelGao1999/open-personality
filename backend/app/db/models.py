from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    mode = Column(String, nullable=False)
    lang = Column(String, nullable=False, default="zh")
    share_token = Column(String, unique=True, nullable=False)
    created_at = Column(String, nullable=False)


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, nullable=False)
    item_id = Column(String, nullable=False)
    value = Column(Integer, nullable=False)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, unique=True, nullable=False)
    big_five_scores = Column(Text, nullable=False)
    mbti_result = Column(Text, nullable=False)
    interpretations = Column(Text, nullable=False)
    easter_egg = Column(String, nullable=True)
    created_at = Column(String, nullable=False)
