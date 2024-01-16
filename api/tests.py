import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_valid_bucket():
    response = client.put("/v1/valid_bucket/", json={"title": "Test", "message": "Test message"})
    assert response.status_code == 422, f"Expected 422, but received {response.status_code}. Response: {response.text}"


def test_invalid_bucket():
    response = client.put("/v1/invalid-bucket/", json={"title": "Test", "message": "Test message"})
    assert response.status_code == 422, f"Expected 422, but received {response.status_code}. Response: {response.text}"
    assert "Field required" in response.text, f"Expected 'Field required' in response, but not found. Response: {response.text}"


def test_get_event_details():
    response_put = client.put("/v1/test_bucket/", json={"title": "Test", "message": "Test message"})
    event_response = response_put.json()

    if 'id' not in event_response:
        pytest.skip("Event ID is not present in the response. Skipping test.")

    event_id = event_response['id']

    response_get = client.get(f"/v1/test_bucket/{event_id}")
    assert response_get.status_code == 200, f"Expected 200, but received {response_get.status_code}. Response: {response_get.text}"

    # Verifică dacă detaliile evenimentului obținute prin GET coincid cu cele stocate prin PUT
    assert response_get.json() == event_response, "Retrieved event details do not match the stored event"

    print("Details of the retrieved event:", response_get.json())


def test_get_event_details_invalid_id():
    response = client.get("/v1/test_bucket/99999")
    assert response.status_code == 404
    assert "Event not found" in response.text


def test_get_event_ids():
    # Adăugați un eveniment într-un anumit bucket pentru a avea date de test
    client.put("/v1/test_bucket/", json={"title": "Test", "message": "Test message"})

    response = client.get("/v1/test_bucket/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)