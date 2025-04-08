from fastapi import status
from datetime import datetime, timedelta
import jwt
from app.core.config import settings

def test_login_success(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 3600

def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "new@example.com",
            "password": "password123",
            "name": "New User"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["email"] == "new@example.com"
    assert data["name"] == "New User"

def test_register_duplicate_email(client, test_user):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Duplicate User"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_refresh_token_success(client, test_token):
    response = client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_refresh_token_invalid(client):
    response = client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_protected_endpoint_unauthorized(client):
    response = client.get("/api/v1/mind-maps")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_protected_endpoint_authorized(client, auth_headers):
    response = client.get("/api/v1/mind-maps", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK

def test_token_expiration(client, test_user):
    # Create an expired token
    expired_token = jwt.encode(
        {
            "sub": str(test_user.id),
            "exp": datetime.utcnow() - timedelta(minutes=1)
        },
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    response = client.get(
        "/api/v1/mind-maps",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 