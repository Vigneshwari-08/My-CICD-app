import pytest
import json
from app.main import app

# Pytest fixture — creates a test client before each test
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_returns_200(client):
    # Verifies the root route is reachable
    response = client.get("/")
    assert response.status_code == 200

def test_home_returns_json(client):
    # Verifies the response is valid JSON with expected keys
    response = client.get("/")
    data = json.loads(response.data)
    assert "message" in data
    assert "status" in data

def test_health_check(client):
    # Critical: verifies the health endpoint works correctly
    response = client.get("/health")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "healthy"

def test_unknown_route_returns_404(client):
    # Tests that unknown routes fail gracefully
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_intentional_failure():
    assert 1 == 2  # This will always fail
