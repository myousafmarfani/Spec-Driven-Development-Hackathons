# REST API Endpoints Specification

## Base URL
`/api/v1`

## Authentication
All endpoints except authentication require a valid JWT token in the Authorization header:
`Authorization: Bearer {token}`

## Endpoints

### Authentication
- `POST /auth/register` - Register new user
  - Request: `{email, password, name}`
  - Response: `{token, user: {id, email, name}}`

- `POST /auth/login` - Login user
  - Request: `{email, password}`
  - Response: `{token, user: {id, email, name}}`

- `POST /auth/refresh` - Refresh token
  - Request: `{refresh_token}`
  - Response: `{token}`

- `POST /auth/logout` - Logout user
  - Request: `{token}`
  - Response: `{success: true}`

### Tasks
- `GET /tasks` - Get user's tasks
  - Query params: `status`, `priority`, `page`, `limit`
  - Response: `{tasks: [...], pagination}`

- `POST /tasks` - Create task
  - Request: `{title, description?, status?, priority?, due_date?}`
  - Response: `{task: {...}}`

- `GET /tasks/{id}` - Get specific task
  - Response: `{task: {...}}`

- `PUT /tasks/{id}` - Update task
  - Request: `{title?, description?, status?, priority?, due_date?}`
  - Response: `{task: {...}}`

- `DELETE /tasks/{id}` - Delete task
  - Response: `{success: true}`

## Error Responses
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Invalid/expired token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Common Response Format
```json
{
  "success": true,
  "data": {},
  "error": null
}
```

For errors:
```json
{
  "success": false,
  "data": null,
  "error": {
    "message": "Error description",
    "code": "ERROR_CODE"
  }
}
```