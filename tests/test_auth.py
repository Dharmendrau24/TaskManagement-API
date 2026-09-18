from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_login():
    response = client.post(
        "/user/login",
        json={
            "username": "dharmendra",
            "password": "dharm"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "token" in data
    assert data["token"]


def test_authenticated_user():
    login_response = client.post(
        "/user/login",
        json={
            "username": "dharmendra",
            "password": "dharm"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["token"]

    response = client.get(
        "/user/is_auth",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "dharmendra"


def test_login_invalid_password():
    response = client.post(
        "/user/login",
        json={
            "username": "dharmendra",
            "password": "wrong-password"
        }
    )

    assert response.status_code == 401

def test_get_tasks_without_authentication():
    response = client.get("/tasks")

    assert response.status_code == 401

def test_get_tasks_with_invalid_token():
    response = client.get(
        "/tasks",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    assert response.status_code == 401

def test_is_auth_without_token():
    response = client.get("/user/is_auth")

    assert response.status_code == 401

def test_login_invalid_username():
    response = client.post(
        "/user/login",
        json={
            "username": "user_that_does_not_exist",
            "password": "any-password"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "You entered an invalid username."