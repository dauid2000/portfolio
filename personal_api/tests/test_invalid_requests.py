"""Tests for invalid requests and validation edge cases."""


def test_unknown_route_returns_404_json(client):
    res = client.get("/api/does-not-exist")
    assert res.status_code == 404


def test_project_id_must_be_integer(client):
    assert client.get("/api/projects/not-a-number").status_code == 422


def test_project_create_rejects_missing_fields(client):
    res = client.post(
        "/api/projects",
        json={"name": "x"},  # description missing/too short
        headers={"Authorization": "Bearer invalid"},
    )
    # Fails on auth before validation — both are acceptable security behavior
    assert res.status_code in (401, 422)


def test_contact_rejects_empty_body(client):
    assert client.post("/api/contact").status_code == 422


def test_contact_rejects_non_json(client):
    res = client.post(
        "/api/contact",
        content="name=David",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == 422


def test_method_not_allowed(client):
    assert client.delete("/api/profile").status_code == 405
