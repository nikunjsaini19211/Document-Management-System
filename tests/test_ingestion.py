import pytest
from fastapi import status

def test_trigger_ingestion(authorized_client):
    response = authorized_client.post("/api/ingestion/trigger")
    assert response.status_code == 200
    assert response.json()["message"] == "Ingestion process started"

def test_get_ingestion_status(authorized_client):
    response = authorized_client.get("/api/ingestion/status")
    assert response.status_code == 200
    data = response.json()
    assert "is_processing" in data
    assert "status" in data 