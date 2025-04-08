from fastapi import status
from uuid import uuid4

def test_create_node(client, auth_headers, test_mind_map):
    response = client.post(
        f"/api/v1/mind-maps/{test_mind_map.id}/nodes",
        json={
            "content": "New Node",
            "position": {"x": 100, "y": 100}
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["content"] == "New Node"
    assert data["position"] == {"x": 100, "y": 100}
    assert data["mind_map_id"] == str(test_mind_map.id)

def test_create_node_invalid_mind_map(client, auth_headers):
    response = client.post(
        f"/api/v1/mind-maps/{uuid4()}/nodes",
        json={
            "content": "New Node",
            "position": {"x": 100, "y": 100}
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_node(client, auth_headers, test_node):
    response = client.put(
        f"/api/v1/nodes/{test_node.id}",
        json={
            "content": "Updated Node",
            "position": {"x": 200, "y": 200}
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["content"] == "Updated Node"
    assert data["position"] == {"x": 200, "y": 200}

def test_update_nonexistent_node(client, auth_headers):
    response = client.put(
        f"/api/v1/nodes/{uuid4()}",
        json={
            "content": "Updated Node",
            "position": {"x": 200, "y": 200}
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_node(client, auth_headers, test_node):
    response = client.delete(
        f"/api/v1/nodes/{test_node.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_nonexistent_node(client, auth_headers):
    response = client.delete(
        f"/api/v1/nodes/{uuid4()}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_edge(client, auth_headers, test_node):
    # Create a target node
    target_node = client.post(
        f"/api/v1/mind-maps/{test_node.mind_map_id}/nodes",
        json={
            "content": "Target Node",
            "position": {"x": 200, "y": 200}
        },
        headers=auth_headers
    ).json()

    response = client.post(
        "/api/v1/edges",
        json={
            "source_id": str(test_node.id),
            "target_id": str(target_node["id"])
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["source_id"] == str(test_node.id)
    assert data["target_id"] == str(target_node["id"])

def test_create_edge_invalid_nodes(client, auth_headers):
    response = client.post(
        "/api/v1/edges",
        json={
            "source_id": str(uuid4()),
            "target_id": str(uuid4())
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_edge(client, auth_headers, test_edge):
    response = client.delete(
        f"/api/v1/edges/{test_edge.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_nonexistent_edge(client, auth_headers):
    response = client.delete(
        f"/api/v1/edges/{uuid4()}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_mind_map_with_nodes(client, auth_headers, test_mind_map, test_node):
    response = client.get(
        f"/api/v1/mind-maps/{test_mind_map.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(test_mind_map.id)
    assert len(data["nodes"]) > 0
    assert any(node["id"] == str(test_node.id) for node in data["nodes"]) 