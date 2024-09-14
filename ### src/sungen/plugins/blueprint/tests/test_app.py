import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == 200

def test_create_user(client):
    response = client.post('/users', json={"name": "Jane Doe"})
    assert response.status_code == 201
