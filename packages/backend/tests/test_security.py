import pytest
from fastapi import status
from jose import jwt
from datetime import datetime, timedelta
import os

def test_password_hashing():
    from app.core.security import get_password_hash, verify_password
    
    password = "testpassword123"
    hashed_password = get_password_hash(password)
    
    assert verify_password(password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)

def test_jwt_token_creation():
    from app.core.security import create_access_token
    
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta)
    
    # Verify token can be decoded
    decoded = jwt.decode(
        token,
        os.getenv("JWT_SECRET_KEY"),
        algorithms=[os.getenv("JWT_ALGORITHM")]
    )
    assert decoded["sub"] == "test@example.com"

def test_jwt_token_expiration():
    from app.core.security import create_access_token
    
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(seconds=1)  # Very short expiration
    token = create_access_token(data, expires_delta)
    
    # Wait for token to expire
    import time
    time.sleep(2)
    
    # Verify token is expired
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=[os.getenv("JWT_ALGORITHM")]
        )

def test_csrf_protection(client, auth_headers):
    # Test that requests without CSRF token are rejected
    response = client.post(
        "/api/v1/mind-maps",
        json={"title": "Test Map"},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "CSRF token missing"

def test_rate_limiting_security(client, auth_headers):
    # Test that rate limiting prevents brute force attacks
    for _ in range(10):  # Assuming limit is 5 attempts per minute
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            }
        )
        if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            break
    
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

def test_sql_injection_protection(client, auth_headers):
    # Test that SQL injection attempts are blocked
    response = client.get(
        "/api/v1/mind-maps?title=' OR '1'='1",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_xss_protection(client, auth_headers):
    # Test that XSS attempts are sanitized
    xss_payload = "<script>alert('xss')</script>"
    response = client.post(
        "/api/v1/mind-maps",
        json={
            "title": xss_payload,
            "description": "Test description"
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert xss_payload not in data["title"]  # Should be sanitized

def test_content_security_policy(client):
    # Test that CSP headers are present
    response = client.get("/")
    assert "Content-Security-Policy" in response.headers

def test_secure_headers(client):
    # Test that security headers are present
    response = client.get("/")
    headers = response.headers
    
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["X-XSS-Protection"] == "1; mode=block"
    assert "Strict-Transport-Security" in headers

def test_password_policy(client):
    # Test that password policy is enforced
    weak_passwords = [
        "password",
        "123456",
        "abc123",
        "qwerty"
    ]
    
    for password in weak_passwords:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": password,
                "full_name": "Test User"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "password" in response.json()["detail"][0]["loc"]

def test_session_management(client, auth_headers):
    # Test that sessions are properly managed
    # Login to create a session
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    
    # Use the token
    response = client.get(
        "/api/v1/mind-maps",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Logout to invalidate the session
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Try to use the invalidated token
    response = client.get(
        "/api/v1/mind-maps",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 