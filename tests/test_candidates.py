import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_TEST_URL = "sqlite:///./data/test_candidates.db"

engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_create_candidate_success():
    payload = {
        "full_name": "Test Candidate",
        "email": "test.candidate@example.com",
        "phone": "+1-555-9999",
        "position": "Python Engineer",
        "source": "LinkedIn"
    }
    res = client.post("/api/candidates", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["full_name"] == "Test Candidate"
    assert data["current_stage"] == "Applied"
    assert len(data["history"]) == 1
    assert data["history"][0]["to_stage"] == "Applied"


def test_candidate_not_found():
    res = client.get("/api/candidates/999999")
    assert res.status_code == 404