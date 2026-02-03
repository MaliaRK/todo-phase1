# Quickstart Guide: Phase III AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Branch**: 001-ai-chatbot
**Created**: 2026-01-12

## Prerequisites

### System Requirements
- Python 3.13+
- PostgreSQL-compatible database (Neon DB recommended)
- Better Auth configured and running
- Cohere API key
- Node.js 18+ (for frontend if needed)

### Environment Setup
Before starting, ensure you have the following environment variables configured:

```bash
# Database Configuration
DATABASE_URL="postgresql://username:password@host:port/database_name"

# API Keys
COHERE_API_KEY="your-cohere-api-key-here"

# Authentication
BETTER_AUTH_SECRET="your-better-auth-secret"
BETTER_AUTH_URL="https://your-domain.better-auth.com"

# Application Settings
APP_ENV="development"  # or "production"
LOG_LEVEL="INFO"
```

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
git checkout 001-ai-chatbot  # Switch to Phase III branch
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies using uv
uv venv  # Create virtual environment
source .venv/bin/activate  # Activate virtual environment (Linux/Mac)
# On Windows: .venv\Scripts\activate

uv pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Run database migrations to create required tables
python -m alembic upgrade head

# Or if using SQLModel directly:
python create_tables.py
```

## Configuration

### 1. Environment Variables
Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/ai_chatbot
COHERE_API_KEY=your_actual_cohere_api_key_here
BETTER_AUTH_SECRET=your_better_auth_secret
BETTER_AUTH_URL=https://your-domain.better-auth.com
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. MCP Server Configuration
The MCP server will be configured automatically when the application starts. It will expose the following tools:
- `add_task`: Create a new task
- `list_tasks`: Retrieve user's tasks
- `complete_task`: Mark a task as completed
- `delete_task`: Remove a task
- `update_task`: Modify task details

## Running the Application

### 1. Start the Backend Server
```bash
# Make sure you're in the backend directory and virtual environment is activated
cd backend
source .venv/bin/activate  # If not already activated

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`.

### 2. Frontend Setup (OpenAI ChatKit)
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Configure ChatKit to connect to your backend
# Update the API endpoint in your ChatKit configuration
```

### 3. ChatKit Configuration
In your ChatKit configuration, point to your backend endpoint:

```javascript
const chatClient = createClient({
  projectId: 'your-project-id',
  // Point to your backend chat endpoint
  apiEndpoint: 'http://localhost:8000/api/{user_id}/chat',
});
```

## Usage Examples

### 1. Making API Requests
Once the server is running, you can test the chat endpoint:

```bash
curl -X POST http://localhost:8000/api/123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

### 2. Starting a New Conversation
```bash
curl -X POST http://localhost:8000/api/123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "message": "What tasks do I have?"
  }'
```

### 3. Continuing an Existing Conversation
```bash
curl -X POST http://localhost:8000/api/123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "conversation_id": 456,
    "message": "Complete the first task"
  }'
```

## API Endpoints

### Main Chat Endpoint
- **URL**: `POST /api/{user_id}/chat`
- **Description**: Process natural language input and manage todos
- **Authentication**: JWT Bearer token required
- **Rate Limit**: 100 requests per minute per user

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify DATABASE_URL is correctly configured
   - Ensure database server is running and accessible
   - Check firewall settings if connecting remotely

2. **Authentication Failures**
   - Verify JWT token is valid and not expired
   - Ensure BETTER_AUTH configuration matches your setup
   - Check that user_id in JWT matches the path parameter

3. **Cohere API Issues**
   - Verify COHERE_API_KEY is valid and has sufficient quota
   - Check network connectivity to Cohere API
   - Ensure using correct API endpoint format

4. **MCP Server Not Responding**
   - Check that the MCP server is properly initialized
   - Verify tool definitions are correctly registered
   - Review logs for any initialization errors

### Checking Application Logs
```bash
# View application logs
tail -f logs/app.log

# Or if using Docker
docker logs ai-chatbot-backend
```

## Development

### Running Tests
```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Run all tests with coverage
python -m pytest --cov=src tests/
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade (if needed)
alembic downgrade -1
```

## Production Deployment

### Environment Variables for Production
```env
APP_ENV=production
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://prod-credentials
COHERE_API_KEY=production-cohere-key
BETTER_AUTH_SECRET=production-auth-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
SENTRY_DSN=your-sentry-dsn-if-enabled
```

### Deployment Commands
```bash
# Build production image (if using Docker)
docker build -t ai-chatbot:latest .

# Run in production mode
docker run -d --env-file .env.production -p 80:8000 ai-chatbot:latest
```

## Next Steps

1. **Customize AI Instructions**: Modify the agent's behavior by updating the system prompt
2. **Extend MCP Tools**: Add additional tools for more complex operations
3. **Enhance Frontend**: Customize the ChatKit interface to match your brand
4. **Monitor Performance**: Set up monitoring and alerting for production use