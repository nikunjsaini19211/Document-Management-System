# Document Management System

A Python-based backend service for managing users and documents with role-based access control.

## Features

- User authentication and authorization
- Document management (CRUD operations)
- Role-based access control (Admin, Editor, Viewer)
- Document ingestion system
- RESTful API design
- PostgreSQL database integration
- JWT-based authentication

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token

### Document Management
- `POST /api/documents/` - Upload a new document
  ```bash
  curl -X POST "http://localhost:8000/api/documents/?title=Test%20Document&description=This%20is%20a%20test%20document&file_type=pdf" \
       -H "Authorization: Bearer $TOKEN" \
       -F "file=@test.pdf"
  ```
- `GET /api/documents/` - List all documents
- `GET /api/documents/{document_id}` - Get a specific document
- `DELETE /api/documents/{document_id}` - Delete a document

### User Management
- `GET /api/users/me` - Get current user information
- `GET /api/users/` - List all users (Admin only)
- `PUT /api/users/{user_id}` - Update user information (Admin only)

### Ingestion
- `POST /api/ingestion/trigger` - Trigger document ingestion
- `GET /api/ingestion/status` - Get ingestion status

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- PostgreSQL (if running locally)

## Project Structure

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd document-management-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
POSTGRES_SERVER=db
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Start the application:
```bash
docker-compose up -d
```

## Testing the API

1. Register a new user:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email":"user@example.com","password":"password123","full_name":"Test User"}'
```

2. Login to get access token:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username":"user@example.com","password":"password123"}'
```

3. Upload a document:
```bash
curl -X POST "http://localhost:8000/api/documents/?title=Test%20Document&description=This%20is%20a%20test%20document&file_type=pdf" \
     -H "Authorization: Bearer $TOKEN" \
     -F "file=@test.pdf"
```

4. List documents:
```bash
curl -X GET "http://localhost:8000/api/documents/" \
     -H "Authorization: Bearer $TOKEN"
```

## Database Schema

The system uses the following tables:

1. `users` - Stores user information
2. `documents` - Stores document metadata
3. `ingestion_logs` - Tracks document ingestion status

## Security Considerations

- All passwords are hashed using bcrypt
- JWT tokens are used for authentication
- Role-based access control is implemented
- File uploads are validated and sanitized

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the repository.