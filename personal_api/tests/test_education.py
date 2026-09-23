"""Tests for the education endpoints (public reads, admin writes)."""


def test_list_education_is_public(client):
    res = client.get("/api/education")
    assert res.status_code == 200
    records = res.json()
    assert len(records) >= 1
    cbu = records[0]
    assert cbu["institution"] == "The Copperbelt University"
    assert cbu["programme"] == "Mining Engineering"
    assert cbu["level"] == "Third Year"
    assert cbu["status"] == "Currently Studying"


def test_create_education_requires_auth(client):
    payload = {
        "institution": "Test Institute",
        "programme": "Testing",
        "level": "Year 1",
    }
    assert client.post("/api/education", json=payload).status_code == 401


def test_admin_can_add_and_delete_education(client, admin_headers):
    payload = {
        "institution": "Test Institute",
        "programme": "Testing",
        "level": "Year 1",
    }
    res = client.post("/api/education", json=payload, headers=admin_headers)
    assert res.status_code == 201, res.text
    edu_id = res.json()["id"]

    res = client.delete(f"/api/education/{edu_id}", headers=admin_headers)
    assert res.status_code == 204
