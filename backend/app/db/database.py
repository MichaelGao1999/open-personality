from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.config import DATABASE_URL
from backend.app.db.models import Base

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    db_path = Path(DATABASE_URL.replace("sqlite:///", "")).parent
    db_path.mkdir(parents=True, exist_ok=True)
    create_tables()
    print(f"Database initialized at {DATABASE_URL}")
