"""Tests for authentication: login, token use, and rejection paths."""


def test_login_with_valid_credentials(client):
    res = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "TestAdmin-2026"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["token_type"] == "bearer"
    assert len(body["access_token"]) > 20


def test_login_with_wrong_password_fails(client):
    res = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "wrong-password"},
    )
    assert res.status_code == 401


def test_login_with_unknown_user_fails(client):
    res = client.post(
        "/api/auth/login",
        data={"username": "ghost", "password": "whatever"},
    )
    assert res.status_code == 401


def test_protected_endpoint_rejects_garbage_token(client):
    res = client.get(
        "/api/contact/messages",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert res.status_code == 401


def test_protected_endpoint_accepts_admin_token(client, admin_headers):
    res = client.get("/api/contact/messages", headers=admin_headers)
    assert res.status_code == 200
