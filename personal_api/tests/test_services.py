"""Tests for the public services endpoint."""


def test_list_services_is_public(client):
    res = client.get("/api/services")
    assert res.status_code == 200
    services = res.json()
    assert len(services) >= 5
    assert all({"id", "title", "description"} <= set(s) for s in services)
    titles = {s["title"] for s in services}
    assert "Python Programming" in titles
    assert "AI & Automation" in titles
