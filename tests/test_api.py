import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_user_register():
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@gmail.com",
            "password": "test123",
            "role": "user"
        }
    )

    assert response.status_code in [200, 400]
def test_user_login():
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@gmail.com",
            "password": "test123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
def get_auth_token():
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@gmail.com",
            "password": "test123"
        }
    )
    return response.json()["access_token"]
def test_place_order():
    token = get_auth_token()

    response = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "restaurant_id": 1,
            "items": [
                {"menu_id": 1, "quantity": 1}
            ]
        }
    )

    assert response.status_code in [200, 201]
def test_assign_delivery():
    token = get_auth_token()

    response = client.post(
        "/delivery/assign?order_id=1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [200, 400]
def test_add_rating():
    token = get_auth_token()

    response = client.post(
        "/ratings",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "order_id": 1,
            "rating": 5,
            "feedback": "Good service"
        }
    )

    assert response.status_code in [200, 400]
