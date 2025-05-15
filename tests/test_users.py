import pytest
from fastapi import status
from app.models.user import UserRole

def test_list_users(authorized_client, test_user):
    response = authorized_client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["email"] == test_user.email

def test_update_user(authorized_client, test_user):
    response = authorized_client.put(
        f"/api/users/{test_user.id}",
        json={
            "full_name": "Updated Name",
            "role": "editor"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["role"] == "editor"

def test_delete_user(authorized_client, test_user):
    response = authorized_client.delete(f"/api/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

def test_unauthorized_access(client):
    response = client.get("/api/users")
    assert response.status_code == 401

def test_get_user_by_id(authorized_client, test_user):
    # Should succeed for existing user
    response = authorized_client.get(f"/api/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email
    # Should 404 for non-existent user
    response = authorized_client.get("/api/users/999999")
    assert response.status_code == 404 