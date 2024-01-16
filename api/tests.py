import pytest
from fastapi.testclient import TestClient

from api.main import app

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
    response_put = client.put("/v1/test_bucket/",
                              json={"title": "Test", "message": "Test message", "bucket": "test_bucket"})
    assert response_put.status_code == 200, f"Expected 200, but received {response_put.status_code}. Response: {response_put.text}"

    event_response = response_put.json()
    event_id = event_response.get('id')

    assert event_id is not None, "Event ID is not present in the response. Test failed."

    response_get = client.get(f"/v1/test_bucket/{event_id}")

    assert response_get.status_code == 200, f"Expected 200, but received {response_get.status_code}. Response: {response_get.text}"

    assert response_get.json() == event_response, "Retrieved event details do not match the stored event"

    print("Details of the retrieved event:", response_get.json())


def test_get_event_details_invalid_id():
    response = client.get("/v1/test_bucket/99999")
    assert response.status_code == 404
    assert "Event not found" in response.text


def test_get_event_ids():
    client.put("/v1/test_bucket/", json={"title": "Test", "message": "Test message"})

    response = client.get("/v1/test_bucket/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_store_event_valid_bucket():
    response = client.put("/v1/valid_bucket/", json={"title": "NewTest", "message": "New test message"})
    assert response.status_code == 422


def test_store_event_valid_bucket_invalid_data():
    response = client.put("/v1/valid_bucket/", json={"title": "", "message": "Invalid data"})
    assert response.status_code == 422


def test_store_event_invalid_bucket():
    response = client.put("/v1/invalid_bucket/", json={"title": "NewTest", "message": "New test message"})
    assert response.status_code == 422


def test_get_event_details_nonexistent():
    response = client.get("/v1/test_bucket/nonexistent_id")
    assert response.status_code == 404


def test_get_event_details_existing():
    response_put = client.put("/v1/test_bucket/", json={"title": "ExistingTest", "message": "Existing test message"})
    assert response_put.status_code == 422
    event_response = response_put.json()
    event_id = event_response.get('id')

    response_get = client.get(f"/v1/test_bucket/{event_id}")
    assert response_get.status_code == 404


