# Quickstart Guide: Phase II Full-Stack Todo Web Application with Authentication

## Overview
This guide provides instructions for setting up and running the full-stack todo application with JWT-based authentication using Better Auth. The application includes Next.js frontend, FastAPI backend, and PostgreSQL database with user-specific task management.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL database (Neon serverless recommended)
- UV package manager (or pip)

## Backend Setup (FastAPI)

1. **Install Python dependencies:**
   ```bash
   cd backend
   uv venv  # or python -m venv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install fastapi uvicorn sqlmodel python-multipart python-jose[cryptography] better-auth
   ```

2. **Set up environment variables:**
   ```bash
   # Create .env file in backend directory
   DATABASE_URL="postgresql://username:password@localhost/dbname"
   BETTER_AUTH_SECRET="your-super-secret-jwt-secret-here"
   ```

3. **Run the backend server:**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

4. **API documentation:**
   - Access the auto-generated API documentation at `http://localhost:8000/docs`
   - Alternative schema at `http://localhost:8000/redoc`

## Frontend Setup (Next.js)

1. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   # or yarn install
   # Install Better Auth client
   npm install better-auth @better-auth/node
   ```

2. **Set up environment variables:**
   ```bash
   # Create .env.local file in frontend directory
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
   BETTER_AUTH_SECRET="your-super-secret-jwt-secret-here"
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   # or yarn dev
   ```

4. **Access the application:**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

## Database Setup (Neon PostgreSQL)

1. **Create a Neon project** and get your connection string
2. **Set the DATABASE_URL** in your backend .env file
3. **Run database migrations** (when implemented):
   ```bash
   python -m src.database.migrate
   ```

## Authentication Setup

### Better Auth Configuration
1. Configure Better Auth in your Next.js application with JWT plugin enabled
2. Ensure the same `BETTER_AUTH_SECRET` is used in both frontend and backend
3. Configure JWT to include `sub` (user_id), `email`, `iat`, and `exp` claims
4. Set up secure session cookies with HttpOnly, Secure (in production), and SameSite=Lax flags

## Running the Full Application

1. **Start the backend:**
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

2. **In a separate terminal, start the frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the application at `http://localhost:3000`**

## Key Endpoints

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Task Management (User-Specific)
- `GET /api/v1/users/{user_id}/tasks` - Get all tasks for a specific user
- `POST /api/v1/users/{user_id}/tasks` - Create a new task for a specific user
- `GET /api/v1/users/{user_id}/tasks/{id}` - Get a specific task for a user
- `PUT /api/v1/users/{user_id}/tasks/{id}` - Update a task for a user
- `DELETE /api/v1/users/{user_id}/tasks/{id}` - Delete a task for a user

## API Security

### JWT Token Usage
- All API requests require `Authorization: Bearer <JWT_TOKEN>` header
- JWT tokens are automatically included by the frontend client
- Backend verifies JWT using BETTER_AUTH_SECRET and HS256 algorithm
- User ID in JWT must match user_id in the request path

### Error Responses
- `401 Unauthorized` - Missing or invalid JWT token
- `403 Forbidden` - User ID in JWT does not match path parameter
- `404 Not Found` - User or task not found

## Development Workflow

1. **Backend development:**
   - Authentication logic in `backend/src/auth/`
   - API routes in `backend/src/api/`
   - Data models in `backend/src/models/`
   - Business logic in `backend/src/services/`

2. **Frontend development:**
   - Authentication components in `frontend/src/auth/`
   - UI components in `frontend/src/components/`
   - Pages in `frontend/src/pages/`
   - API calls in `frontend/src/services/`

3. **Testing:**
   - Backend: `pytest` in the backend directory
   - Frontend: `npm test` in the frontend directory