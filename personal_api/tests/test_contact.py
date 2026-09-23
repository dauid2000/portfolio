"""Tests for contact: public submission, admin-only reading."""

VALID = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+260999000111",
    "subject": "Project opportunity",
    "message": "Hello David, I would like to discuss a project opportunity.",
}


def test_submit_contact_is_public(client):
    res = client.post("/api/contact", json=VALID)
    assert res.status_code == 201, res.text
    data = res.json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"
    assert data["subject"] == "Project opportunity"
    assert data["message"].startswith("Hello David")


def test_contact_validation_rejects_bad_data(client):
    # Invalid email
    bad = {**VALID, "email": "not-an-email"}
    assert client.post("/api/contact", json=bad).status_code == 422

    # Message too short
    short = {**VALID, "message": "hi"}
    assert client.post("/api/contact", json=short).status_code == 422

    # Missing required fields
    assert client.post("/api/contact", json={"name": "x"}).status_code == 422


def test_contact_subject_is_optional(client):
    minimal = {
        "name": "No Subject",
        "email": "nosubject@example.com",
        "message": "This message intentionally has no subject line.",
    }
    res = client.post("/api/contact", json=minimal)
    assert res.status_code == 201
    assert res.json()["subject"] is None


def test_messages_are_private_without_auth(client):
    res = client.post("/api/contact", json=VALID)
    assert res.status_code == 201
    # No token -> submissions must not be readable
    assert client.get("/api/contact/messages").status_code == 401


def test_admin_can_read_messages(client, admin_headers):
    client.post("/api/contact", json=VALID)
    res = client.get("/api/contact/messages", headers=admin_headers)
    assert res.status_code == 200
    messages = res.json()
    assert len(messages) >= 1
    assert all({"id", "name", "email", "message", "created_at"} <= set(m) for m in messages)
