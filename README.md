# Document Management System

A robust Python-based backend service for managing users and documents with role-based access control, document ingestion, and a modern RESTful API. Built with FastAPI, SQLAlchemy, and PostgreSQL.

---

## Features
- User authentication and JWT-based authorization
- Role-based access control (Admin, Editor, Viewer)
- Document CRUD operations with file upload
- Document ingestion and logging
- PostgreSQL database integration
- Dockerized for easy deployment
- Automated testing and load testing (Locust)

---

## Table of Contents
- [API Endpoints](#api-endpoints)
- [Environment Setup](#environment-setup)
- [Running with Docker](#running-with-docker)
- [Manual Local Setup](#manual-local-setup)
- [Testing](#testing)
- [Load Testing](#load-testing)
- [Database Schema](#database-schema)
- [Security](#security)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/token` - Login and get access token (form data)
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout

#### Register
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","full_name":"Test User", "role":"viewer"}'
```
#### Login
```bash
curl -X POST "http://localhost:8000/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```
#### Get Current User
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```
#### Logout
```bash
curl -X POST "http://localhost:8000/api/auth/logout" \
  -H "Authorization: Bearer $TOKEN"
```

---

### User Management (Admin only for some endpoints)
- `GET /api/users/` - List all users (Admin only)
- `GET /api/users/{user_id}` - Get user by ID (Admin only)
- `PUT /api/users/{user_id}` - Update user info (Admin only)
- `DELETE /api/users/{user_id}` - Delete user (Admin only)

#### List Users
```bash
curl -X GET "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN"
```
#### Get User by ID
```bash
curl -X GET "http://localhost:8000/api/users/3" \
  -H "Authorization: Bearer $TOKEN"
```
#### Update User
```bash
curl -X PUT "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Updated Name", "role": "editor"}'
```
#### Delete User
```bash
curl -X DELETE "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Document Management
- `POST /api/documents/` - Upload a new document (Admin/Editor only)
- `GET /api/documents/` - List all documents
- `GET /api/documents/{document_id}` - Get a specific document
- `PUT /api/documents/{document_id}` - Update document metadata (Admin/Editor only)
- `DELETE /api/documents/{document_id}` - Delete a document (Admin only)

#### Upload Document
```bash
curl -X POST "http://localhost:8000/api/documents/" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.pdf" \
  -F "title=Test Document" \
  -F "description=This is a test document" \
  -F "file_type=pdf"
```
#### List Documents
```bash
curl -X GET "http://localhost:8000/api/documents/" \
  -H "Authorization: Bearer $TOKEN"
```
#### Get Document
```bash
curl -X GET "http://localhost:8000/api/documents/1" \
  -H "Authorization: Bearer $TOKEN"
```
#### Update Document (metadata only)
```bash
curl -X PUT "http://localhost:8000/api/documents/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Document", "description": "Updated description", "file_type": "pdf"}'
```
#### Update Document (with file)
```bash
curl -X PUT "http://localhost:8000/api/documents/1" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@updated.pdf" \
  -F "title=Updated Document" \
  -F "description=Updated description" \
  -F "file_type=pdf"
```
#### Delete Document
```bash
curl -X DELETE "http://localhost:8000/api/documents/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Ingestion
- `GET /api/ingestion/` - List all ingestion logs (Admin/Editor only)
- `POST /api/ingestion/trigger` - Trigger document ingestion (Admin/Editor only)
- `GET /api/ingestion/status` - Get ingestion status (Admin/Editor only)

#### List Ingestion Logs
```bash
curl -X GET "http://localhost:8000/api/ingestion/" \
  -H "Authorization: Bearer $TOKEN"
```
#### Trigger Ingestion
```bash
curl -X POST "http://localhost:8000/api/ingestion/trigger" \
  -H "Authorization: Bearer $TOKEN"
```
#### Get Ingestion Status
```bash
curl -X GET "http://localhost:8000/api/ingestion/status" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Environment Setup

### .env Example
Create a `.env` file in the project root:
```env
POSTGRES_SERVER=db
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
CORS_ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
```

---

## Running with Docker

1. **Build and start all services:**
```bash
docker-compose up --build -d
```
2. **Stop all services:**
```bash
docker-compose down
```
3. **View logs:**
```bash
docker-compose logs -f
```
4. **Access the API:**
- FastAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Manual Local Setup (without Docker)

1. **Install dependencies:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. **Start PostgreSQL** and create the database/tables (see `init.sql` for schema).
3. **Set up your `.env` file** as above.
4. **Run the app:**
```bash
uvicorn app.main:app --reload
```

---

## Testing

1. **Run all tests:**
```bash
./run_tests.sh all
```
2. **Run a specific test file:**
```bash
pytest tests/test_documents.py
```
3. **Generate a coverage report:**
```bash
pytest --cov=app --cov-report=html
```
4. **View coverage report:**
Open `htmlcov/index.html` in your browser.

---

## Load Testing

1. **Start the app:**
```bash
docker-compose up -d
```
2. **Run load tests:**
```bash
./run_load_tests.sh
```
3. **Open Locust UI:**
[http://localhost:8089](http://localhost:8089)

---

## Database Schema

- `users` - User accounts
- `documents` - Document metadata and file info
- `ingestion_logs` - Ingestion process logs

See `init.sql` for full schema.

---

## Security
- Passwords hashed with bcrypt
- JWT authentication
- Role-based access control
- CORS configuration

---

## Error Handling
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

---

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## License
MIT License

---

## Support
For support, open an issue in the repository.