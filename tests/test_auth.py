def test_login(auth_client):
    response = auth_client.post(
        "/user/login",
        json={
            "username": "testuser",
            "password": "testuser@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "token" in data
    assert data["token"]


def test_authenticated_user(auth_client):
    response = auth_client.get("/user/is_auth")

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"


def test_login_invalid_password(auth_client):
    response = auth_client.post(
        "/user/login",
        json={
            "username": "testuser",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_get_tasks_without_authentication(client):
    response = client.get("/tasks")

    assert response.status_code == 401


def test_get_tasks_with_invalid_token(client):
    response = client.get(
        "/tasks",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401


def test_is_auth_without_token(client):
    response = client.get("/user/is_auth")

    assert response.status_code == 401


def test_login_invalid_username(client):
    response = client.post(
        "/user/login",
        json={
            "username": "user_that_does_not_exist",
            "password": "any-password",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "You entered an invalid username."