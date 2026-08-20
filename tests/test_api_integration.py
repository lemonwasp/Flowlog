import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient

from backend.database import engine
from backend.main import app
from backend.models import Base

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_identifies_flowlog_api():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Flowlog API"}


def test_user_creation_and_listing_round_trip():
    create_response = client.post(
        "/users/",
        json={"name": "Test User", "email": "test@example.com"},
    )

    assert create_response.status_code == 200
    created_user = create_response.json()
    assert created_user["name"] == "Test User"
    assert created_user["email"] == "test@example.com"

    list_response = client.get("/users/")

    assert list_response.status_code == 200
    users = list_response.json()
    assert len(users) == 1
    assert users[0]["id"] == created_user["id"]


def test_core_tracking_flow_persists_related_records():
    user_response = client.post(
        "/users/",
        json={"name": "Flow Tester", "email": "flow@example.com"},
    )
    user_id = user_response.json()["id"]

    activity_type_response = client.post(
        "/activity-types/",
        json={"name": "deep-work"},
    )
    activity_type_id = activity_type_response.json()["id"]

    emotion_response = client.post(
        "/emotions/",
        json={"user_id": user_id, "free_text": "오늘은 행복 신나다"},
    )
    assert emotion_response.status_code == 200
    emotion = emotion_response.json()
    assert emotion["emotion"] == "positive"
    assert emotion["emotion_score"] > 0

    activity_response = client.post(
        "/activities/",
        json={
            "user_id": user_id,
            "activity_type_id": activity_type_id,
            "description": "Focused coding session",
        },
    )
    assert activity_response.status_code == 200
    assert activity_response.json()["description"] == "Focused coding session"

    flow_response = client.post(
        "/flow-curve/",
        json={
            "user_id": user_id,
            "time_spent": 1.5,
            "satisfaction": 4.5,
        },
    )
    assert flow_response.status_code == 200
    flow = flow_response.json()
    assert flow["time_spent"] == 1.5
    assert flow["satisfaction"] == 4.5
