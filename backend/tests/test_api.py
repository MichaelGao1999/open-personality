from fastapi.testclient import TestClient

from backend.app.db.database import get_db
from backend.app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.models import Base

_test_engine = create_engine("sqlite://", echo=False, poolclass=StaticPool, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=_test_engine)
_TestSession = sessionmaker(bind=_test_engine)


def override_get_db():
    db = _TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_items_standard_zh():
    response = client.get("/api/questionnaires/items?mode=standard&lang=zh")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 120


def test_get_items_standard_en():
    response = client.get("/api/questionnaires/items?mode=standard&lang=en")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 120


def test_get_items_invalid_mode():
    response = client.get("/api/questionnaires/items?mode=invalid&lang=zh")
    assert response.status_code == 422


def test_get_items_invalid_lang():
    response = client.get("/api/questionnaires/items?mode=standard&lang=fr")
    assert response.status_code == 422


def test_submit_valid():
    answers = [{"item_id": f"ipip_{i:03d}", "value": 3} for i in range(1, 121)]
    response = client.post("/api/questionnaires/submit", json={
        "mode": "standard", "lang": "zh", "answers": answers,
    })
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "share_token" in data
    assert "scoring" in data
    assert "mbti" in data
    assert "interpretations" in data
    assert data["mode"] == "standard"
    assert data["lang"] == "zh"


def test_submit_wrong_count():
    answers = [{"item_id": f"ipip_{i:03d}", "value": 3} for i in range(1, 10)]
    response = client.post("/api/questionnaires/submit", json={
        "mode": "standard", "lang": "zh", "answers": answers,
    })
    assert response.status_code == 422


def test_submit_invalid_value():
    answers = [{"item_id": f"ipip_{i:03d}", "value": 3} for i in range(1, 121)]
    answers[0]["value"] = 0
    response = client.post("/api/questionnaires/submit", json={
        "mode": "standard", "lang": "zh", "answers": answers,
    })
    assert response.status_code == 422


def test_submit_invalid_mode():
    answers = [{"item_id": f"ipip_{i:03d}", "value": 3} for i in range(1, 121)]
    response = client.post("/api/questionnaires/submit", json={
        "mode": "invalid", "lang": "zh", "answers": answers,
    })
    assert response.status_code == 422


def test_get_report_by_token():
    answers = [{"item_id": f"ipip_{i:03d}", "value": 3} for i in range(1, 121)]
    submit_resp = client.post("/api/questionnaires/submit", json={
        "mode": "standard", "lang": "zh", "answers": answers,
    })
    assert submit_resp.status_code == 200
    token = submit_resp.json()["share_token"]
    response = client.get(f"/api/report/{token}")
    assert response.status_code == 200
    data = response.json()
    assert data["share_token"] == token


def test_get_report_not_found():
    response = client.get("/api/report/nonexist")
    assert response.status_code == 404


def test_get_i18n_zh():
    response = client.get("/api/i18n/zh")
    assert response.status_code == 200


def test_get_i18n_en():
    response = client.get("/api/i18n/en")
    assert response.status_code == 200


def test_get_i18n_not_found():
    response = client.get("/api/i18n/fr")
    assert response.status_code == 404


def test_submit_advanced_wrong_count():
    answers = [{"item_id": f"ipip_{i:03d}", "value": 4} for i in range(1, 121)]
    response = client.post("/api/questionnaires/submit", json={
        "mode": "advanced", "lang": "en", "answers": answers,
    })
    assert response.status_code == 422
