import pytest
from mongoengine import connect, disconnect
import mongomock
from fastapi.testclient import TestClient
from app.main import app
from app.celery_tasks.send_email import send_welcome_email_task
from unittest.mock import patch

@pytest.fixture(scope="module")
def client():
    disconnect()
    connect(
        "mongoenginetest",
        host="mongodb://localhost:1234",
        mongo_client_class=mongomock.MongoClient,
        uuidRepresentation="standard"
    )
    yield TestClient(app)
    disconnect()

def test_create_user(client):
    r = client.post(
        "/users",
        json={
            "email": "testuser@gmail.com",
        },
    )
    assert r.status_code == 200
