import pytest
from fastapi.testclient import TestClient
from tests.test_candidates import client


def test_valid_and_invalid_stage_transitions():
    # 1. Create candidate
    c_res = client.post("/api/candidates", json={
        "full_name": "Stage Test User",
        "email": "stage.test@example.com",
        "position": "Backend Lead"
    })
    c_id = c_res.json()["id"]

    # 2. Valid: Applied -> Screening
    res = client.patch(f"/api/candidates/{c_id}/stage", json={
        "stage": "Screening",
        "changed_by": "Tester",
        "reason": "Passed resume check"
    })
    assert res.status_code == 200
    assert res.json()["current_stage"] == "Screening"

    # 3. Invalid Skip: Screening -> Offer (Should fail)
    res_skip = client.patch(f"/api/candidates/{c_id}/stage", json={"stage": "Offer"})
    assert res_skip.status_code == 400
    assert "Invalid stage transition" in str(res_skip.json())

    # 4. Invalid Backward: Screening -> Applied (Should fail)
    res_back = client.patch(f"/api/candidates/{c_id}/stage", json={"stage": "Applied"})
    assert res_back.status_code == 400

    # 5. Complete progression: Screening -> Interview -> Offer -> Hired
    assert client.patch(f"/api/candidates/{c_id}/stage", json={"stage": "Interview"}).status_code == 200
    assert client.patch(f"/api/candidates/{c_id}/stage", json={"stage": "Offer"}).status_code == 200
    assert client.patch(f"/api/candidates/{c_id}/stage", json={"stage": "Hired"}).status_code == 200

    # 6. Terminal State check: Hired -> any stage must fail
    res_terminal = client.patch(f"/api/candidates/{c_id}/stage", json={"stage": "Interview"})
    assert res_terminal.status_code == 400


def test_immutable_history_audit_trail():
    c_res = client.post("/api/candidates", json={
        "full_name": "Audit Trail User",
        "email": "audit.test@example.com",
        "position": "QA Lead"
    })
    c_id = c_res.json()["id"]

    client.patch(f"/api/candidates/{c_id}/stage", json={"stage": "Screening"})
    
    hist_res = client.get(f"/api/candidates/{c_id}/history")
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert len(history) == 2
    assert history[0]["to_stage"] == "Applied"
    assert history[1]["to_stage"] == "Screening"