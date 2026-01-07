# Full-Stack Todo Web Application

This is a full-stack todo application built with Next.js for the frontend and FastAPI for the backend, using SQLModel for data modeling and PostgreSQL for persistence. The application includes user authentication and authorization with JWT tokens.

## Features

- Create, read, update, and delete todo tasks
- Mark tasks as complete/incomplete
- View all tasks in a list
- User authentication (register/login)
- Secure task access (users can only access their own tasks)
- Responsive web interface

## Tech Stack

- **Frontend**: Next.js, React, JavaScript/CSS
- **Backend**: FastAPI, Python
- **Database**: PostgreSQL (with SQLModel ORM)
- **Authentication**: JWT tokens with HS256 algorithm
- **Deployment**: Docker, docker-compose

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL database
- Docker and Docker Compose (optional)

## Setup

### Option 1: Using Docker (Recommended)

1. Clone the repository
2. Update the database connection string and authentication secrets in `backend/.env` if needed
3. Run the application using Docker Compose:

```bash
docker-compose up --build
```

The frontend will be available at `http://localhost:3000` and the backend API at `http://localhost:8000`.

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
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
```bash
cp .env.example .env  # Update with your database credentials and authentication secrets
```

5. Run the backend:
```bash
uvicorn src.main:app --reload
```

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.local.example .env.local  # Update with your API base URL
```

4. Run the development server:
```bash
npm run dev
```

## Authentication Setup

### Environment Variables

#### Backend (.env)

- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Secret key for Better Auth (should be at least 32 characters, used for JWT signing)
- `ALGORITHM` - Algorithm for JWT tokens (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 15 minutes for security)

#### Frontend (.env.local)

- `NEXT_PUBLIC_API_BASE_URL` - Base URL for API calls (e.g., http://localhost:8000)

### Generating BETTER_AUTH_SECRET

To generate a secure secret for `BETTER_AUTH_SECRET`, run:

```bash
openssl rand -base64 32
```

Or use an online secure random generator to create a 32+ character random string.

### Authentication Endpoints

The authentication API is available at `http://localhost:8000/api/auth/`:

- `POST /auth/register` - Register a new user with email and password
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout (client-side token removal)

### User Registration and Login Flow

1. New users can register at `/register` page with email and password
2. Existing users can login at `/login` page with their credentials
3. After successful authentication, JWT tokens are securely stored and managed
4. All API requests include the JWT token in the Authorization header as "Bearer {token}"
5. The system enforces user isolation - users can only access their own tasks
6. Session cookies are configured with HttpOnly, Secure, and SameSite=Lax flags for security

### Secure Task Access

The application enforces user-specific task access through:

- User ID validation: The user ID in the JWT token must match the user ID in the API path
- Task filtering: The backend only returns tasks belonging to the authenticated user
- Authorization headers: All requests must include a valid JWT token
- Path-based access control: Task endpoints require user_id in the path (e.g., `/api/v1/users/{user_id}/tasks`)

### Frontend Authentication Provider

The frontend uses an authentication context provider that:

- Manages user session state
- Handles login and logout operations
- Stores JWT tokens securely
- Intercepts API requests to add authorization headers
- Redirects unauthenticated users to login page
- Handles 401 responses by redirecting to login

## API Endpoints

The API is available at `http://localhost:8000/api/v1/`:

- `GET /users/{user_id}/tasks` - Get all tasks for the specified user (must match authenticated user)
- `POST /users/{user_id}/tasks` - Create a new task for the specified user (must match authenticated user)
- `GET /users/{user_id}/tasks/{task_id}` - Get a specific task (must belong to specified user and authenticated user)
- `PUT /users/{user_id}/tasks/{task_id}` - Update a task (must belong to specified user and authenticated user)
- `PATCH /users/{user_id}/tasks/{task_id}/toggle-completion` - Toggle task completion status (must belong to specified user and authenticated user)
- `DELETE /users/{user_id}/tasks/{task_id}` - Delete a task (must belong to specified user and authenticated user)

All endpoints require a valid JWT token in the Authorization header with "Bearer" prefix. The user_id in the path must match the user_id in the JWT token for security validation.

## Project Structure

```
backend/
├── src/
│   ├── models/          # Database models
│   ├── services/        # Business logic
│   ├── api/             # API routes
│   ├── auth/            # Authentication logic
│   └── main.py          # Application entry point
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables

frontend/
├── src/
│   ├── auth/            # Authentication provider
│   ├── components/      # React components
│   ├── pages/           # Next.js pages
│   ├── services/        # API services
│   └── contexts/        # React contexts
├── package.json         # Node.js dependencies
└── .env.local           # Environment variables
```

## Development

For development, run both the backend and frontend in separate terminals:

Backend:
```bash
cd backend
uvicorn src.main:app --reload
```

Frontend:
```bash
cd frontend
npm run dev
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.