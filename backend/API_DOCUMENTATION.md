# AI Todo Chatbot API Documentation

## Overview

The AI Todo Chatbot API provides a conversational interface for managing todo tasks using natural language. The API is built with FastAPI and follows RESTful principles.

## Base URL

The API is served at: `http://localhost:8000` (development) or your deployed domain.

## Authentication

All API endpoints require authentication using JWT (JSON Web Tokens). Include the token in the Authorization header as follows:

```
Authorization: Bearer <your-jwt-token>
```

Tokens are obtained by authenticating through the Better Auth system.

## Endpoints

### Chat Endpoint

Process a user message in a conversation.

- **URL**: `POST /{user_id}/chat`
- **Description**: Process a user message with the AI agent to perform todo operations
- **Headers**:
  - `Authorization: Bearer <token>` (required)
- **Path Parameters**:
  - `user_id` (integer, required): The ID of the user making the request. Must match the user ID in the JWT token.
- **Request Body**:
  ```json
  {
    "conversation_id": 123,
    "message": "Add a task to buy groceries"
  }
  ```
  - `conversation_id`: Optional existing conversation ID (creates new conversation if not provided)
  - `message`: The user's natural language message (required)
- **Response**:
  ```json
  {
    "conversation_id": 123,
    "response": "I've added the task 'buy groceries' to your list.",
    "tool_calls": [
      {
        "id": "call_abc123",
        "type": "function",
        "function": {
          "name": "add_task",
          "arguments": "{\"user_id\": 123, \"title\": \"buy groceries\"}"
        }
      }
    ],
    "task_summary": {
      "total_count": 5,
      "pending_count": 3,
      "completed_count": 2
    }
  }
  ```

### Health Check Endpoint

Check the health status of the API.

- **URL**: `GET /health`
- **Description**: Verify that the API service is running and healthy
- **Response**:
  ```json
  {
    "status": "healthy",
    "service": "ai-todo-chatbot"
  }
  ```

### Task Endpoints (Inherited from Phase II)

The API also includes the original task management endpoints from Phase II:

- `GET /api/v1/users/{user_id}/tasks` - Get all tasks for the specified user
- `POST /api/v1/users/{user_id}/tasks` - Create a new task for the specified user
- `GET /api/v1/users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/users/{user_id}/tasks/{task_id}` - Update a task
- `PATCH /api/v1/users/{user_id}/tasks/{task_id}/toggle-completion` - Toggle task completion
- `DELETE /api/v1/users/{user_id}/tasks/{task_id}` - Delete a task

### Auth Endpoints (Inherited from Phase II)

The API also includes authentication endpoints from Phase II:

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and obtain JWT token
- `POST /api/auth/logout` - Logout

## Request/Response Formats

### Chat Request

```json
{
  "conversation_id": 123,
  "message": "Show me my tasks"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| conversation_id | integer | No | Existing conversation ID (new conversation created if absent) |
| message | string | Yes | User's natural language input |

### Chat Response

```json
{
  "conversation_id": 123,
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [...],
  "task_summary": {...}
}
```

| Field | Type | Description |
|-------|------|-------------|
| conversation_id | integer | Active conversation ID (newly created or existing) |
| response | string | AI assistant's response to the user |
| tool_calls | array | List of MCP tools that were invoked |
| task_summary | object | Summary of the user's tasks after processing |

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request - invalid input
- `401`: Unauthorized - invalid or missing JWT
- `403`: Forbidden - user_id in JWT doesn't match path parameter
- `404`: Not Found - resource not found
- `500`: Internal Server Error - unexpected error occurred

Error responses follow the format:

```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "path": "/api/endpoint"
}
```

## Security

- All endpoints require valid JWT authentication
- User ID in JWT token must match the user ID in the path parameter
- Input validation is performed on all requests
- Rate limiting is applied to prevent abuse
- Sensitive data is protected and not exposed in responses

## Rate Limits

The API implements rate limiting to prevent abuse:

- 100 requests per minute per user
- 1000 requests per hour per IP address

## Best Practices

1. Always include the Authorization header with a valid JWT token
2. Match the user_id in the path with the authenticated user
3. Handle errors gracefully in your client application
4. Implement retry logic for failed requests with exponential backoff
5. Use conversation_id to maintain context across multiple interactions
6. Process the AI's response to provide feedback to users

## Examples

### Adding a Task
```bash
curl -X POST http://localhost:8000/123/chat \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy milk"
  }'
```

### Listing Tasks
```bash
curl -X POST http://localhost:8000/123/chat \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What tasks do I have?"
  }'
```

### Completing a Task
```bash
curl -X POST http://localhost:8000/123/chat \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Complete the first task"
  }'
```