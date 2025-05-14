from locust import HttpUser, task, between
import json
import random

class DocumentManagementUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    token = None

    def on_start(self):
        """Login and get token before starting tasks"""
        # Register a new user
        register_data = {
            "email": f"test_user_{random.randint(1, 1000)}@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
        self.client.post("/api/auth/register", json=register_data)

        # Login to get token
        login_data = {
            "username": register_data["email"],
            "password": register_data["password"]
        }
        response = self.client.post("/api/auth/login", json=login_data)
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.client.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def list_documents(self):
        """List all documents"""
        self.client.get("/api/documents/")

    @task(2)
    def get_document(self):
        """Get a specific document"""
        # Assuming document IDs are sequential, try a random one
        doc_id = random.randint(1, 100)
        self.client.get(f"/api/documents/{doc_id}")

    @task(1)
    def upload_document(self):
        """Upload a new document"""
        # Create a simple text file
        files = {
            "file": ("test.txt", "This is a test document", "text/plain")
        }
        data = {
            "title": f"Test Document {random.randint(1, 1000)}",
            "description": "This is a test document",
            "file_type": "txt"
        }
        self.client.post("/api/documents/", files=files, data=data)

    @task(1)
    def update_document(self):
        """Update a document"""
        doc_id = random.randint(1, 100)
        update_data = {
            "title": f"Updated Document {random.randint(1, 1000)}",
            "description": "This is an updated document",
            "file_type": "txt"
        }
        self.client.put(f"/api/documents/{doc_id}", json=update_data)

class AdminUser(DocumentManagementUser):
    """Admin user with additional privileges"""
    
    @task(1)
    def list_users(self):
        """List all users (admin only)"""
        self.client.get("/api/users/")

    @task(1)
    def delete_document(self):
        """Delete a document (admin only)"""
        doc_id = random.randint(1, 100)
        self.client.delete(f"/api/documents/{doc_id}")

    @task(1)
    def trigger_ingestion(self):
        """Trigger document ingestion (admin only)"""
        self.client.post("/api/ingestion/trigger") 