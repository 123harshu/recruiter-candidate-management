import pytest
from tests.test_candidates import client


@pytest.fixture
def seed_test_search_data():
    client.post("/api/candidates", json={
        "full_name": "Harshita Verma",
        "email": "harshita@example.com",
        "position": "Dev"
    })
    client.post("/api/candidates", json={
        "full_name": "Rahul Kapoor",
        "email": "rahul@example.com",
        "position": "PM"
    })


def test_fuzzy_search(seed_test_search_data):
    # Search "Harsh" should fuzzy match "Harshita Verma"
    res = client.get("/api/candidates?search=Harsh")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "Harshita Verma"


def test_combined_search(seed_test_search_data):
    res = client.get("/api/candidates?search=Rah&stage=Applied")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "Rahul Kapoor"