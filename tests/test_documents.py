import pytest
from fastapi import status
import os

def test_upload_document(authorized_client):
    # Create a test file
    with open("test.pdf", "wb") as f:
        f.write(b"test content")
    
    try:
        with open("test.pdf", "rb") as f:
            response = authorized_client.post(
                "/api/documents/",
                files={
                    "file": ("test.pdf", f, "application/pdf")
                },
                data={
                    "title": "Test Document",
                    "description": "This is a test document",
                    "file_type": "pdf"
                }
            )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Document"
        assert data["description"] == "This is a test document"
        assert data["file_type"] == "pdf"
    finally:
        # Clean up test file
        if os.path.exists("test.pdf"):
            os.remove("test.pdf")

def test_list_documents(authorized_client):
    response = authorized_client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_document(authorized_client):
    # First create a document
    with open("test.pdf", "wb") as f:
        f.write(b"test content")
    
    try:
        with open("test.pdf", "rb") as f:
            response = authorized_client.post(
                "/api/documents/",
                files={
                    "file": ("test.pdf", f, "application/pdf")
                },
                data={
                    "title": "Test Document",
                    "description": "This is a test document",
                    "file_type": "pdf"
                }
            )
        assert response.status_code == 200
        document_id = response.json()["id"]
        
        # Then get the document
        response = authorized_client.get(f"/api/documents/{document_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Document"
        assert data["description"] == "This is a test document"
        assert data["file_type"] == "pdf"
    finally:
        if os.path.exists("test.pdf"):
            os.remove("test.pdf")

def test_update_document(authorized_client):
    # First create a document
    with open("test.pdf", "wb") as f:
        f.write(b"test content")

    try:
        with open("test.pdf", "rb") as f:
            response = authorized_client.post(
                "/api/documents/",
                files={
                    "file": ("test.pdf", f, "application/pdf")
                },
                data={
                    "title": "Test Document",
                    "description": "This is a test document",
                    "file_type": "pdf"
                }
            )
        assert response.status_code == 200
        document_id = response.json()["id"]

        # Update the document
        update_data = {
            "title": "Updated Document",
            "description": "This is an updated document",
            "file_type": "pdf"
        }
        response = authorized_client.put(
            f"/api/documents/{document_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Document"
        assert data["description"] == "This is an updated document"
    finally:
        # Clean up
        if os.path.exists("test.pdf"):
            os.remove("test.pdf") 