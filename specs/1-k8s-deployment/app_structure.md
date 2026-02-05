# Phase III Application Structure and Requirements

## Application Overview
- **Application Type**: AI-powered Todo Chatbot using OpenAI Agents SDK + MCP
- **Architecture**: Microservice with frontend and backend components
- **Data Storage**: Neon PostgreSQL (external managed service)

## Directory Structure
```
.
├── backend/
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── tests/
└── ...
```

## Backend Service
- **Framework**: FastAPI
- **Technologies**: OpenAI Agents SDK, MCP Server, Neon PostgreSQL
- **Expected Port**: 8000 (typical for FastAPI)
- **Environment Variables Needed**:
  - DATABASE_URL (Neon PostgreSQL connection string)
  - OPENAI_API_KEY
  - MCP_SERVER_CONFIG

## Frontend Service
- **Framework**: ChatKit-based UI
- **Expected Port**: 3000 (typical for web apps)
- **Environment Variables Needed**:
  - REACT_APP_BACKEND_URL (for API calls to backend)

## Deployment Requirements
- Both services must be containerized separately
- Database connection must be established via external Neon PostgreSQL
- Services must communicate with each other within the Kubernetes cluster
- Application must maintain statelessness while relying on external database for persistence