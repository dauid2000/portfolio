"""Tests for the public profile endpoint."""


def test_profile_returns_personal_info(client):
    res = client.get("/api/profile")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "David Musumali"
    assert data["profession"] == "Third-Year Mining Engineering Student"
    assert data["university"] == "The Copperbelt University"
    assert data["phone"] == "+260773108622"
    assert "musumali01" in data["email"].lower()
