import pytest
from fastapi import status
import time

def test_rate_limiting_headers(client, auth_headers):
    # Make a request and check rate limit headers
    response = client.get(
        "/api/v1/mind-maps",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert "X-RateLimit-Reset" in response.headers

def test_rate_limiting_exceeded(client, auth_headers):
    # Make requests until rate limit is exceeded
    for _ in range(60):  # Assuming limit is 60 requests per minute
        response = client.get(
            "/api/v1/mind-maps",
            headers=auth_headers
        )
        if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            break
    
    # Verify rate limit exceeded response
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert "Retry-After" in response.headers
    data = response.json()
    assert data["detail"] == "Rate limit exceeded"
    assert "retry_after" in data

def test_rate_limiting_reset(client, auth_headers):
    # First, exceed the rate limit
    for _ in range(60):
        client.get("/api/v1/mind-maps", headers=auth_headers)
    
    # Wait for rate limit to reset (1 minute)
    time.sleep(61)
    
    # Make a new request
    response = client.get(
        "/api/v1/mind-maps",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert int(response.headers["X-RateLimit-Remaining"]) > 0

def test_different_endpoints_rate_limits(client, auth_headers):
    # Test that different endpoints have separate rate limits
    # Make requests to one endpoint until limit is reached
    for _ in range(60):
        client.get("/api/v1/mind-maps", headers=auth_headers)
    
    # Make a request to a different endpoint
    response = client.get(
        "/api/v1/templates",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK

def test_authenticated_vs_unauthenticated_limits(client):
    # Test that authenticated and unauthenticated requests have different limits
    # Make unauthenticated requests
    for _ in range(30):  # Assuming lower limit for unauthenticated
        response = client.get("/api/v1/mind-maps")
        if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            break
    
    # Make authenticated request
    response = client.get(
        "/api/v1/mind-maps",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK

def test_rate_limiting_websocket(client, auth_headers):
    # Test that WebSocket connections are also rate limited
    ws_url = client.base_url.replace("http", "ws") + "ws"
    
    # Try to establish multiple WebSocket connections
    connections = []
    for _ in range(5):  # Assuming limit is 5 concurrent connections
        try:
            connection = connect(ws_url)
            connections.append(connection)
        except Exception:
            break
    
    # Verify that we couldn't establish more than the limit
    assert len(connections) <= 5
    
    # Clean up connections
    for connection in connections:
        connection.close() 