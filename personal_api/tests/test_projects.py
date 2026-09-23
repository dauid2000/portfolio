"""Tests for the projects endpoints (public reads, admin writes)."""

NEW_PROJECT = {
    "name": "Test Project",
    "description": "A project created by the automated test suite.",
    "technologies": ["Python", "SQLite"],
}


def test_list_projects_is_public(client):
    res = client.get("/api/projects")
    assert res.status_code == 200
    assert len(res.json()) >= 3


def test_seeded_projects_present(client):
    names = {p["name"] for p in client.get("/api/projects").json()}
    assert "Bana Kulu Finances" in names
    assert "Bus Station Transport Management & Automated Dispatch System" in names
    assert "KITE" in names


def test_get_single_project(client):
    res = client.get("/api/projects/1")
    assert res.status_code == 200
    assert res.json()["id"] == 1


def test_get_missing_project_returns_404(client):
    assert client.get("/api/projects/99999").status_code == 404


def test_create_project_requires_auth(client):
    assert client.post("/api/projects", json=NEW_PROJECT).status_code == 401


def test_admin_project_crud_cycle(client, admin_headers):
    res = client.post("/api/projects", json=NEW_PROJECT, headers=admin_headers)
    assert res.status_code == 201, res.text
    project = res.json()
    assert project["technologies"] == ["Python", "SQLite"]

    res = client.put(
        f"/api/projects/{project['id']}",
        json={"tagline": "Updated tagline"},
        headers=admin_headers,
    )
    assert res.status_code == 200
    assert res.json()["tagline"] == "Updated tagline"

    res = client.delete(f"/api/projects/{project['id']}", headers=admin_headers)
    assert res.status_code == 204
    assert client.get(f"/api/projects/{project['id']}").status_code == 404
