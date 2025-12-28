import pytest
from fastapi.testclient import TestClient
from main import app, USERS_DB

client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint"""

    def test_read_root(self):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to FastAPI Login API"}


class TestLoginEndpoint:
    """Tests for the login endpoint"""

    def test_login_successful_with_valid_credentials(self):
        """Test successful login with valid username and password"""
        response = client.post(
            "/login",
            json={"username": "testuser", "password": "password123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Login successful"
        assert data["username"] == "testuser"
        assert data["token"] == "token_testuser_authenticated"

    def test_login_successful_with_admin_credentials(self):
        """Test successful login with admin credentials"""
        response = client.post(
            "/login",
            json={"username": "admin", "password": "admin123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Login successful"
        assert data["username"] == "admin"
        assert data["token"] == "token_admin_authenticated"

    def test_login_fails_with_invalid_username(self):
        """Test login fails with non-existent username"""
        response = client.post(
            "/login",
            json={"username": "nonexistent", "password": "password123"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid username or password"

    def test_login_fails_with_invalid_password(self):
        """Test login fails with wrong password"""
        response = client.post(
            "/login",
            json={"username": "testuser", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid username or password"

    def test_login_fails_with_empty_username(self):
        """Test login fails with empty username"""
        response = client.post(
            "/login",
            json={"username": "", "password": "password123"}
        )
        assert response.status_code == 401

    def test_login_fails_with_empty_password(self):
        """Test login fails with empty password"""
        response = client.post(
            "/login",
            json={"username": "testuser", "password": ""}
        )
        assert response.status_code == 401

    def test_login_fails_with_missing_username(self):
        """Test login fails when username field is missing"""
        response = client.post(
            "/login",
            json={"password": "password123"}
        )
        assert response.status_code == 422  # Unprocessable Entity

    def test_login_fails_with_missing_password(self):
        """Test login fails when password field is missing"""
        response = client.post(
            "/login",
            json={"username": "testuser"}
        )
        assert response.status_code == 422  # Unprocessable Entity

    def test_login_response_structure(self):
        """Test login response has correct structure"""
        response = client.post(
            "/login",
            json={"username": "testuser", "password": "password123"}
        )
        data = response.json()
        assert "message" in data
        assert "username" in data
        assert "token" in data
        assert isinstance(data["message"], str)
        assert isinstance(data["username"], str)
        assert isinstance(data["token"], str)
