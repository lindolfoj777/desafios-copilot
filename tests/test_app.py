import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Basketball Team" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400


def test_remove_participant():
    email = "removeme@mergington.edu"
    activity = "Drama Club"
    # Add first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Remove
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Removed")
    # Try removing again
    response2 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response2.status_code == 404
