"""Tests for the skills endpoints (public reads, admin writes)."""

NEW_SKILL = {"name": "Rust Basics", "category": "Programming"}


def test_list_skills_is_public_and_seeded(client):
    res = client.get("/api/skills")
    assert res.status_code == 200
    skills = res.json()
    assert len(skills) >= 14
    names = {s["name"] for s in skills}
    assert "Python Programming" in names
    assert "Database Security" in names
    assert all({"id", "name", "category"} <= set(s) for s in skills)


def test_create_skill_without_token_fails(client):
    res = client.post("/api/skills", json=NEW_SKILL)
    assert res.status_code == 401


def test_create_and_delete_skill_with_admin(client, admin_headers):
    res = client.post("/api/skills", json=NEW_SKILL, headers=admin_headers)
    assert res.status_code == 201, res.text
    skill = res.json()
    assert skill["name"] == "Rust Basics"

    # Duplicate names are rejected
    dup = client.post("/api/skills", json=NEW_SKILL, headers=admin_headers)
    assert dup.status_code == 409

    # Cleanup
    res = client.delete(f"/api/skills/{skill['id']}", headers=admin_headers)
    assert res.status_code == 204
    assert client.get(f"/api/skills/{skill['id']}").status_code == 404
