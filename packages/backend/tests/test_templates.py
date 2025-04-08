from fastapi import status
from uuid import uuid4

def test_create_template(client, auth_headers):
    response = client.post(
        "/api/v1/templates",
        json={
            "name": "Project Template",
            "description": "A template for project planning",
            "nodes": [
                {
                    "content": "Project",
                    "position": {"x": 0, "y": 0}
                },
                {
                    "content": "Tasks",
                    "position": {"x": 100, "y": 100}
                }
            ],
            "edges": [
                {
                    "source": 0,
                    "target": 1
                }
            ]
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Project Template"
    assert data["description"] == "A template for project planning"
    assert len(data["nodes"]) == 2
    assert len(data["edges"]) == 1

def test_list_templates(client, auth_headers, test_template):
    response = client.get(
        "/api/v1/templates",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(template["id"] == str(test_template.id) for template in data)

def test_get_template(client, auth_headers, test_template):
    response = client.get(
        f"/api/v1/templates/{test_template.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(test_template.id)
    assert data["name"] == test_template.name
    assert len(data["nodes"]) > 0

def test_get_nonexistent_template(client, auth_headers):
    response = client.get(
        f"/api/v1/templates/{uuid4()}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_template(client, auth_headers, test_template):
    response = client.put(
        f"/api/v1/templates/{test_template.id}",
        json={
            "name": "Updated Template",
            "description": "Updated description",
            "nodes": test_template.nodes,
            "edges": test_template.edges
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Template"
    assert data["description"] == "Updated description"

def test_delete_template(client, auth_headers, test_template):
    response = client.delete(
        f"/api/v1/templates/{test_template.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_create_mind_map_from_template(client, auth_headers, test_template):
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

def test_create_mind_map_invalid_template(client, auth_headers):
    response = client.post(
        "/api/v1/mind-maps",
        json={
            "title": "Invalid Template Mind Map",
            "template_id": str(uuid4())
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND 