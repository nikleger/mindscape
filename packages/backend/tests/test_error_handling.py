import pytest
from fastapi import status
from uuid import uuid4

def test_not_found_error(client, auth_headers):
    response = client.get(
        f"/api/v1/mind-maps/{uuid4()}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Resource not found"
    assert "error_code" in data
    assert data["error_code"] == "NOT_FOUND"

def test_validation_error(client, auth_headers):
    response = client.post(
        "/api/v1/mind-maps",
        json={
            "title": "",  # Empty title should trigger validation error
            "description": "Test description"
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert len(data["detail"]) > 0
    assert "loc" in data["detail"][0]
    assert "msg" in data["detail"][0]

def test_unauthorized_error(client):
    response = client.get(
        "/api/v1/mind-maps"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Not authenticated"
    assert data["error_code"] == "UNAUTHORIZED"

def test_forbidden_error(client, auth_headers, test_mind_map):
    # Try to access a mind map that doesn't belong to the user
    response = client.get(
        f"/api/v1/mind-maps/{test_mind_map.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    data = response.json()
    assert data["detail"] == "Access forbidden"
    assert data["error_code"] == "FORBIDDEN"

def test_internal_server_error(client, auth_headers, monkeypatch):
    # Mock a function to raise an exception
    def mock_raise_error():
        raise Exception("Test error")
    
    monkeypatch.setattr("app.api.mind_maps.get_mind_maps", mock_raise_error)
    
    response = client.get(
        "/api/v1/mind-maps",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["detail"] == "Internal server error"
    assert data["error_code"] == "INTERNAL_SERVER_ERROR"

def test_bad_request_error(client, auth_headers):
    response = client.post(
        "/api/v1/mind-maps",
        json={
            "invalid_field": "value"
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Invalid request"
    assert data["error_code"] == "BAD_REQUEST"

def test_conflict_error(client, auth_headers):
    # Try to create a resource that already exists
    response = client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "password": "password123"
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    data = response.json()
    assert data["detail"] == "Resource already exists"
    assert data["error_code"] == "CONFLICT"

def test_error_response_format(client):
    # Test that all error responses follow the same format
    error_endpoints = [
        ("/api/v1/invalid-route", status.HTTP_404_NOT_FOUND),
        ("/api/v1/mind-maps", status.HTTP_401_UNAUTHORIZED),
    ]
    
    for endpoint, expected_status in error_endpoints:
        response = client.get(endpoint)
        assert response.status_code == expected_status
        data = response.json()
        assert "detail" in data
        assert "error_code" in data
        assert isinstance(data["detail"], str)
        assert isinstance(data["error_code"], str) 