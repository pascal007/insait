def test_create_generated_text(client, auth_headers):
    response = client.post("/generated-text", json={"prompt": "Test prompt"}, headers=auth_headers)
    assert response.status_code == 201
    assert response.json["success"] is True
    assert "data" in response.json


def test_get_generated_text(client, auth_headers):
    create_response = client.post("/generated-text", json={"prompt": "Test prompt"}, headers=auth_headers)
    prompt_id = create_response.json["data"]["id"]
    response = client.get(f"/generated-text/{prompt_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["prompt"] == "Test prompt"


def test_delete_generated_text(client, auth_headers):
    create_response = client.post("/generated-text", json={"prompt": "Test prompt"}, headers=auth_headers)
    prompt_id = create_response.json["data"]["id"]
    delete_response = client.delete(f"/generated-text/{prompt_id}", headers=auth_headers)
    assert delete_response.status_code == 200
    assert delete_response.json["success"] is True
    get_response = client.get(f"/generated-text/{prompt_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_update_generated_text(client, auth_headers):
    create_response = client.post("/generated-text", json={"prompt": "Initial prompt"}, headers=auth_headers)
    prompt_id = create_response.json["data"]["id"]
    update_response = client.put(
        f"/generated-text/{prompt_id}",
        json={"prompt": "Updated prompt"},
        headers=auth_headers
    )
    assert update_response.status_code == 200
    assert update_response.json["success"] is True
    assert update_response.json["data"]["prompt"] == "Updated prompt"
    get_response = client.get(f"/generated-text/{prompt_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json["data"]["prompt"] == "Updated prompt"
