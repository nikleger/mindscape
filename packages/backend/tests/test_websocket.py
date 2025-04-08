import pytest
from fastapi import status
from fastapi.testclient import TestClient
from websockets import connect
import json
import asyncio

@pytest.mark.asyncio
async def test_websocket_connection(client: TestClient, auth_headers):
    # Get the WebSocket URL from the client
    ws_url = client.base_url.replace("http", "ws") + "ws"
    
    # Connect to WebSocket
    async with connect(ws_url) as websocket:
        # Send authentication message
        await websocket.send(json.dumps({
            "type": "auth",
            "token": auth_headers["Authorization"].split(" ")[1]
        }))
        
        # Receive authentication response
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "auth_success"
        assert "user_id" in data

@pytest.mark.asyncio
async def test_websocket_invalid_auth(client: TestClient):
    ws_url = client.base_url.replace("http", "ws") + "ws"
    
    async with connect(ws_url) as websocket:
        await websocket.send(json.dumps({
            "type": "auth",
            "token": "invalid_token"
        }))
        
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "error"
        assert data["code"] == "invalid_token"

@pytest.mark.asyncio
async def test_websocket_mind_map_updates(client: TestClient, auth_headers, test_mind_map):
    ws_url = client.base_url.replace("http", "ws") + "ws"
    
    async with connect(ws_url) as websocket:
        # Authenticate
        await websocket.send(json.dumps({
            "type": "auth",
            "token": auth_headers["Authorization"].split(" ")[1]
        }))
        await websocket.recv()  # Wait for auth response
        
        # Subscribe to mind map updates
        await websocket.send(json.dumps({
            "type": "subscribe",
            "mind_map_id": str(test_mind_map.id)
        }))
        
        # Create a new node through HTTP
        response = client.post(
            f"/api/v1/mind-maps/{test_mind_map.id}/nodes",
            json={
                "content": "New Node",
                "position": {"x": 100, "y": 100}
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        # Receive WebSocket update
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "node_created"
        assert data["mind_map_id"] == str(test_mind_map.id)
        assert data["node"]["content"] == "New Node"

@pytest.mark.asyncio
async def test_websocket_collaboration(client: TestClient, auth_headers, test_mind_map):
    ws_url = client.base_url.replace("http", "ws") + "ws"
    
    # Create two WebSocket connections
    async with connect(ws_url) as ws1, connect(ws_url) as ws2:
        # Authenticate both connections
        for ws in [ws1, ws2]:
            await ws.send(json.dumps({
                "type": "auth",
                "token": auth_headers["Authorization"].split(" ")[1]
            }))
            await ws.recv()  # Wait for auth response
        
        # Subscribe both connections to the mind map
        for ws in [ws1, ws2]:
            await ws.send(json.dumps({
                "type": "subscribe",
                "mind_map_id": str(test_mind_map.id)
            }))
        
        # User 1 creates a node
        await ws1.send(json.dumps({
            "type": "create_node",
            "mind_map_id": str(test_mind_map.id),
            "content": "Collaborative Node",
            "position": {"x": 200, "y": 200}
        }))
        
        # Both users should receive the update
        for ws in [ws1, ws2]:
            response = await ws.recv()
            data = json.loads(response)
            assert data["type"] == "node_created"
            assert data["mind_map_id"] == str(test_mind_map.id)
            assert data["node"]["content"] == "Collaborative Node"

@pytest.mark.asyncio
async def test_websocket_heartbeat(client: TestClient, auth_headers):
    ws_url = client.base_url.replace("http", "ws") + "ws"
    
    async with connect(ws_url) as websocket:
        # Authenticate
        await websocket.send(json.dumps({
            "type": "auth",
            "token": auth_headers["Authorization"].split(" ")[1]
        }))
        await websocket.recv()  # Wait for auth response
        
        # Send heartbeat
        await websocket.send(json.dumps({
            "type": "heartbeat"
        }))
        
        # Receive heartbeat response
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "heartbeat_response"
        assert "timestamp" in data 