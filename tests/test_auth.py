def test_register_user(client):
    response = client.post("/register", json={"username": "newuser", "password": "password123"})
    assert response.status_code == 201
    assert response.json["success"] is True


def test_login_user(client):
    client.post("/register", json={"username": "newuser", "password": "password123"})
    response = client.post("/login", json={"username": "newuser", "password": "password123"})
    assert response.status_code == 200
    assert "data" in response.json
