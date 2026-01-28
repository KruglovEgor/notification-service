from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_notification() -> None:
    response = client.post(
        "/api/notifications",
        json={"user_id": 1, "message": "Hello", "type": "email"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["status"] == "pending"


def test_create_notification_validation_error() -> None:
    response = client.post(
        "/api/notifications",
        json={"user_id": 1, "message": "Hello", "type": "sms"},
    )
    assert response.status_code == 422


def test_list_notifications_filter_by_status() -> None:
    client.post(
        "/api/notifications",
        json={"user_id": 2, "message": "Hi", "type": "telegram"},
    )
    response = client.get("/api/notifications/2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

    status = data[0]["status"]
    filtered = client.get("/api/notifications/2", params={"status": status})
    assert filtered.status_code == 200
    filtered_data = filtered.json()
    assert len(filtered_data) >= 1
    assert all(item["status"] == status for item in filtered_data)
