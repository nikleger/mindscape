import pytest
from fastapi import status
import logging
from unittest.mock import patch
import json
import time

def test_request_logging(client, caplog):
    # Test that requests are properly logged
    with caplog.at_level(logging.INFO):
        response = client.get("/api/v1/mind-maps")
        
        # Check that request was logged
        assert any("GET /api/v1/mind-maps" in record.message for record in caplog.records)
        assert any("status_code=401" in record.message for record in caplog.records)

def test_error_logging(client, caplog):
    # Test that errors are properly logged
    with caplog.at_level(logging.ERROR):
        response = client.get("/api/v1/invalid-endpoint")
        
        # Check that error was logged
        assert any("404" in record.message for record in caplog.records)
        assert any("Not Found" in record.message for record in caplog.records)

def test_performance_metrics(client):
    # Test that performance metrics are collected
    start_time = time.time()
    response = client.get("/api/v1/mind-maps")
    end_time = time.time()
    
    # Check response time header
    assert "X-Response-Time" in response.headers
    response_time = float(response.headers["X-Response-Time"])
    assert response_time >= 0
    assert response_time <= (end_time - start_time) * 1000  # Convert to milliseconds

def test_health_check_endpoint(client):
    # Test the health check endpoint
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data

def test_metrics_endpoint(client):
    # Test the metrics endpoint
    response = client.get("/metrics")
    assert response.status_code == status.HTTP_200_OK
    assert "text/plain" in response.headers["content-type"]
    
    # Check for some basic metrics
    metrics = response.text
    assert "http_requests_total" in metrics
    assert "http_request_duration_seconds" in metrics

def test_error_tracking(client, monkeypatch):
    # Test error tracking integration
    mock_capture_exception = pytest.Mock()
    monkeypatch.setattr("sentry_sdk.capture_exception", mock_capture_exception)
    
    # Trigger an error
    response = client.get("/api/v1/invalid-endpoint")
    
    # Verify error was tracked
    mock_capture_exception.assert_called_once()

def test_structured_logging(client, caplog):
    # Test that logs are properly structured
    with caplog.at_level(logging.INFO):
        response = client.get("/api/v1/mind-maps")
        
        # Find the request log
        request_log = next(
            record for record in caplog.records 
            if "GET /api/v1/mind-maps" in record.message
        )
        
        # Check log structure
        log_data = json.loads(request_log.message)
        assert "method" in log_data
        assert "path" in log_data
        assert "status_code" in log_data
        assert "response_time" in log_data

def test_correlation_id(client):
    # Test that correlation IDs are properly handled
    correlation_id = "test-correlation-id"
    response = client.get(
        "/api/v1/mind-maps",
        headers={"X-Correlation-ID": correlation_id}
    )
    
    # Check that correlation ID is returned
    assert response.headers["X-Correlation-ID"] == correlation_id

def test_alerting_thresholds(client, monkeypatch):
    # Test alerting thresholds
    mock_send_alert = pytest.Mock()
    monkeypatch.setattr("app.core.monitoring.send_alert", mock_send_alert)
    
    # Simulate high error rate
    for _ in range(10):
        client.get("/api/v1/invalid-endpoint")
    
    # Verify alert was sent
    mock_send_alert.assert_called_once()

def test_log_rotation():
    # Test log rotation configuration
    from app.core.logging import setup_logging
    import os
    
    # Setup logging
    log_file = "test.log"
    setup_logging(log_file)
    
    # Verify log file exists
    assert os.path.exists(log_file)
    
    # Clean up
    os.remove(log_file) 