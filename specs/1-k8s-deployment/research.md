# Research: Local Kubernetes Deployment (Cloud Native + AIOps)

## Phase 0: Research & Unknown Resolution

### Decision: Technology Stack for AI-Assisted Deployment
**Rationale**: Need to understand and validate the required tools for this Phase IV deployment. The specification requires Docker, Minikube, Helm, and AI tools like Gordon, kubectl-ai, and kagent.
**Alternatives considered**:
- Traditional manual Kubernetes YAML deployment vs. AI-assisted
- Different container runtimes (Docker vs. Podman vs. containerd)
- Different local Kubernetes solutions (Minikube vs. kind vs. k3d)

### Decision: Containerization Approach
**Rationale**: The application needs to be containerized with the frontend and backend as separate services. Using Docker AI Agent (Gordon) is preferred as specified.
**Alternatives considered**:
- Single container with both frontend and backend
- Multi-stage builds vs. single-stage builds
- Different base images (Alpine vs. Ubuntu vs. distroless)

### Decision: Helm Chart Structure
**Rationale**: Need to create separate Helm charts for frontend and backend to maintain modularity and follow best practices. This allows independent scaling and configuration.
**Alternatives considered**:
- Single monolithic chart with subcharts
- Combined chart for both services
- Multiple charts with shared templates

### Decision: Database Connection Pattern
**Rationale**: Using Kubernetes Secrets for database credentials and ConfigMaps for other configuration. This follows security best practices for external database connections.
**Alternatives considered**:
- Environment variables directly in deployment
- External secret managers
- Direct database connection strings in values.yaml

### Decision: Service Exposure Strategy
**Rationale**: Using NodePort or LoadBalancer services to expose the frontend to the local machine. For Minikube, various options are available including service tunnels.
**Alternatives considered**:
- Ingress controllers
- Port forwarding
- Minikube tunnel service
- Ingress with custom DNS

### Research: Existing Application Structure
**Finding**: The Phase III Todo Chatbot has:
- Frontend: ChatKit-based UI in the `./frontend` directory
- Backend: FastAPI server with OpenAI Agents SDK and MCP in the `./backend` directory
- Current architecture is web-based with frontend communicating to backend API
- Backend connects to Neon PostgreSQL database externally

### Research: AI Tool Availability
**Finding**: Need to validate availability of:
- Docker AI Agent (Gordon) for Dockerfile generation
- kubectl-ai for Kubernetes operations
- Kagent for cluster analysis
- Fallback to Claude Code if AI tools unavailable

### Research: Current Phase III Requirements
**Finding**: Based on the backend/frontend structure, need to identify:
- Backend port (likely 8000 for FastAPI)
- Frontend port (likely 3000 for web app)
- Environment variables needed for database connection
- Required dependencies and build steps