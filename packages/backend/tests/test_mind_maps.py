from fastapi import status
from uuid import uuid4

def test_create_mind_map(client, auth_headers):
    response = client.post(
        "/api/v1/mind-maps",
        json={
            "title": "New Mind Map",
            "template_id": None
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "New Mind Map"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_mind_map(client, auth_headers, test_mind_map):
    response = client.get(
        f"/api/v1/mind-maps/{test_mind_map.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(test_mind_map.id)
    assert data["title"] == test_mind_map.title

def test_get_nonexistent_mind_map(client, auth_headers):
    response = client.get(
        f"/api/v1/mind-maps/{uuid4()}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_mind_map(client, auth_headers, test_mind_map):
    response = client.put(
        f"/api/v1/mind-maps/{test_mind_map.id}",
        json={
            "title": "Updated Title"
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Title"

def test_delete_mind_map(client, auth_headers, test_mind_map):
    response = client.delete(
        f"/api/v1/mind-maps/{test_mind_map.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_list_mind_maps(client, auth_headers, test_mind_map):
    response = client.get(
        "/api/v1/mind-maps",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(mind_map["id"] == str(test_mind_map.id) for mind_map in data)

def test_create_mind_map_with_template(client, auth_headers, test_template):
    response = client.post(
        "/api/v1/mind-maps",
        json={
            "title": "Template-based Mind Map",
            "template_id": str(test_template.id)
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Template-based Mind Map"
    assert data["template_id"] == str(test_template.id)

def test_unauthorized_access(client, test_mind_map):
    response = client.get(
        f"/api/v1/mind-maps/{test_mind_map.id}"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 