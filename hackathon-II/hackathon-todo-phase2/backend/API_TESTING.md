# API Testing Instructions

## Testing the Backend API Endpoints

This document provides instructions for testing the Todo Application API endpoints.

## Prerequisites

1. Ensure you have Python 3.13+ installed
2. Install the project dependencies:
   ```bash
   cd backend
   pip install -e .
   # Or if using uv:
   uv pip install -e .
   ```

## Starting the Development Server

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a `.env` file with the required configuration:
   ```bash
   # Create the environment file
   cp .env.example .env

   # Edit .env to add your actual values:
   # - Generate a strong secret for BETTER_AUTH_SECRET
   # - Add your actual DATABASE_URL
   # - Set FRONTEND_URL to your frontend URL
   ```

3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoint Testing

### Authentication Testing
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <valid_token>
```

### Available Endpoints

1. **GET** `/api/{user_id}/tasks`
   - Get all tasks for a user
   - Query parameter: `status` (optional: "pending", "completed")
   - Requires: Valid token with matching user_id

2. **POST** `/api/{user_id}/tasks`
   - Create a new task
   - Request body: `{"title": "...", "description": "..."}`
   - Requires: Valid token with matching user_id

3. **GET** `/api/{user_id}/tasks/{task_id}`
   - Get a specific task
   - Requires: Valid token with matching user_id

4. **PUT** `/api/{user_id}/tasks/{task_id}`
   - Update a task
   - Request body: `{"title": "...", "description": "...", "completed": true/false}`
   - Requires: Valid token with matching user_id

5. **DELETE** `/api/{user_id}/tasks/{task_id}`
   - Delete a task
   - Requires: Valid token with matching user_id

6. **PATCH** `/api/{user_id}/tasks/{task_id}/complete`
   - Toggle task completion status
   - Request body: `{"completed": true/false}`
   - Requires: Valid token with matching user_id

### Manual Testing with curl

Example curl commands (replace `<token>` with a valid JWT token and `<user_id>` with actual user ID):

```bash
# Get user's tasks
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/<user_id>/tasks

# Create a task
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title":"Test task","description":"This is a test task"}' \
  http://localhost:8000/api/<user_id>/tasks

# Update a task
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title":"Updated task","completed":true}' \
  http://localhost:8000/api/<user_id>/tasks/1

# Delete a task
curl -X DELETE \
  -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/<user_id>/tasks/1

# Toggle task completion
curl -X PATCH \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"completed":true}' \
  http://localhost:8000/api/<user_id>/tasks/1
```

### Automated Testing

Run the automated test script:
```bash
python test_api.py
```

## Security Testing

The API includes the following security measures:
- JWT token verification on all endpoints
- User ID validation (path parameter must match token's user ID)
- Data isolation (users can only access their own tasks)
- Proper error responses for unauthorized access

## Health Check

The API includes a health check endpoint:
```
GET /
GET /health
```

## Expected Responses

All endpoints return appropriate HTTP status codes:
- 200: Success
- 201: Created (for POST requests)
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (attempting to access another user's data)
- 404: Not Found (resource doesn't exist)
- 500: Server Error (internal server error)