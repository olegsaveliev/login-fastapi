from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_login_success():
    response = client.post(
        "/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["username"] == "admin"
    assert data["token"] == "fake-jwt-token-123"


def test_login_invalid_credentials():
    response = client.post(
        "/login",
        json={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_missing_username():
    response = client.post(
        "/login",
        json={"password": "admin123"}
    )
    assert response.status_code == 422


def test_login_missing_password():
    response = client.post(
        "/login",
        json={"username": "admin"}
    )
    assert response.status_code == 422
