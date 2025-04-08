import pytest
from fastapi import status
import json
import yaml
from pathlib import Path

def test_openapi_schema(client):
    # Test OpenAPI schema generation
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK
    
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema
    assert "components" in schema

def test_api_documentation_endpoints(client):
    # Test API documentation endpoints
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]
    
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]

def test_api_versioning(client):
    # Test API versioning in documentation
    response = client.get("/openapi.json")
    schema = response.json()
    
    assert "servers" in schema
    servers = schema["servers"]
    assert any("/api/v1" in server["url"] for server in servers)

def test_endpoint_documentation(client):
    # Test endpoint documentation
    response = client.get("/openapi.json")
    schema = response.json()
    
    # Check mind maps endpoints
    assert "/api/v1/mind-maps" in schema["paths"]
    mind_maps_path = schema["paths"]["/api/v1/mind-maps"]
    
    # Check GET endpoint
    assert "get" in mind_maps_path
    get_operation = mind_maps_path["get"]
    assert "summary" in get_operation
    assert "description" in get_operation
    assert "parameters" in get_operation
    assert "responses" in get_operation
    
    # Check POST endpoint
    assert "post" in mind_maps_path
    post_operation = mind_maps_path["post"]
    assert "requestBody" in post_operation
    assert "content" in post_operation["requestBody"]

def test_security_schemes(client):
    # Test security schemes documentation
    response = client.get("/openapi.json")
    schema = response.json()
    
    assert "securitySchemes" in schema["components"]
    security_schemes = schema["components"]["securitySchemes"]
    
    assert "BearerAuth" in security_schemes
    bearer_auth = security_schemes["BearerAuth"]
    assert bearer_auth["type"] == "http"
    assert bearer_auth["scheme"] == "bearer"

def test_error_responses(client):
    # Test error responses documentation
    response = client.get("/openapi.json")
    schema = response.json()
    
    # Check common error responses
    for path in schema["paths"].values():
        for operation in path.values():
            assert "401" in operation["responses"]
            assert "403" in operation["responses"]
            assert "404" in operation["responses"]
            assert "422" in operation["responses"]

def test_data_models(client):
    # Test data models documentation
    response = client.get("/openapi.json")
    schema = response.json()
    
    assert "schemas" in schema["components"]
    schemas = schema["components"]["schemas"]
    
    # Check common models
    assert "User" in schemas
    assert "MindMap" in schemas
    assert "Node" in schemas
    assert "Edge" in schemas
    assert "Template" in schemas

def test_examples(client):
    # Test examples in documentation
    response = client.get("/openapi.json")
    schema = response.json()
    
    # Check mind map creation example
    mind_maps_path = schema["paths"]["/api/v1/mind-maps"]
    post_operation = mind_maps_path["post"]
    request_body = post_operation["requestBody"]
    
    assert "examples" in request_body["content"]["application/json"]
    examples = request_body["content"]["application/json"]["examples"]
    assert "default" in examples

def test_tags(client):
    # Test API tags
    response = client.get("/openapi.json")
    schema = response.json()
    
    assert "tags" in schema
    tags = [tag["name"] for tag in schema["tags"]]
    
    expected_tags = [
        "Authentication",
        "Mind Maps",
        "Nodes",
        "Edges",
        "Templates",
        "Users"
    ]
    
    assert all(tag in tags for tag in expected_tags)

def test_external_docs(client):
    # Test external documentation links
    response = client.get("/openapi.json")
    schema = response.json()
    
    assert "externalDocs" in schema
    external_docs = schema["externalDocs"]
    assert "url" in external_docs
    assert "description" in external_docs

def test_asyncapi_schema():
    # Test AsyncAPI schema for WebSocket documentation
    asyncapi_path = Path("docs/asyncapi.yaml")
    assert asyncapi_path.exists()
    
    with open(asyncapi_path) as f:
        schema = yaml.safe_load(f)
    
    assert "asyncapi" in schema
    assert "info" in schema
    assert "channels" in schema
    assert "components" in schema 