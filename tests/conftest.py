import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.utils.db import Base, get_db


TEST_DATABASE_URL = (
    "postgresql://postgres:admin@localhost:5432/myDb_test"
)

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


def create_test_client():
    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


@pytest.fixture
def client():
    test_client = create_test_client()

    try:
        yield test_client
    finally:
        test_client.close()
        app.dependency_overrides.clear()


@pytest.fixture
def auth_client(client):
    username = "testuser"
    password = "testuser@123"

    register_response = client.post(
        "/user/register",
        json={
            "name": "Test User",
            "username": username,
            "email": "testuser@example.com",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/user/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client


@pytest.fixture
def authenticated_user(auth_client):
    response = auth_client.get("/user/is_auth")

    assert response.status_code == 200

    return response.json()


@pytest.fixture
def second_auth_client():
    client = create_test_client()

    username = "testuser2"
    password = "testuser@123"

    try:
        # Register User 2
        register_response = client.post(
            "/user/register",
            json={
                "name": "Test User 2",
                "username": username,
                "email": "testuser2@example.com",
                "password": password,
            },
        )

        assert register_response.status_code == 201

        # Login User 2
        login_response = client.post(
            "/user/login",
            json={
                "username": username,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()["token"]

        client.headers.update({
            "Authorization": f"Bearer {token}"
        })

        yield client

    finally:
        client.close()
        app.dependency_overrides.clear()