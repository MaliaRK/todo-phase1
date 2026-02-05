# Quickstart Guide: Local Kubernetes Deployment (Cloud Native + AIOps)

## Prerequisites

- Docker Desktop installed and running
- Minikube installed
- kubectl installed
- Helm installed
- kubectl-ai (optional but recommended for AI-assisted operations)
- kagent (optional but recommended for AI-assisted cluster analysis)

## Setup Steps

### 1. Start Minikube Cluster
```bash
minikube start --driver=docker
```

### 2. Verify Cluster Status
```bash
kubectl cluster-info
kubectl get nodes
```

### 3. Prepare AI Tools (if available)
```bash
# Verify Docker AI Agent (Gordon) is accessible
# Verify kubectl-ai is installed
kubectl-ai --version

# Verify kagent is installed
kagent --version
```

### 4. Build Docker Images
Use Docker AI Agent (Gordon) or Claude Code to:
- Generate Dockerfile for backend (FastAPI + Agents SDK + MCP)
- Build backend container image
- Generate Dockerfile for frontend (ChatKit UI)
- Build frontend container image

### 5. Create Helm Charts
Use AI tools to generate Helm charts for:
- Frontend service with configurable parameters
- Backend service with database connection settings
- Support for replica scaling and resource configuration

### 6. Deploy to Minikube
```bash
# Install Helm charts
helm install todo-frontend ./charts/frontend -f values.yaml
helm install todo-backend ./charts/backend -f values.yaml
```

### 7. Access the Application
```bash
# Get frontend service URL
minikube service todo-frontend-service --url

# Or expose via NodePort
kubectl expose deployment todo-frontend-deployment --type=NodePort --port=80
```

### 8. Validate Deployment
- Access the frontend UI in your browser
- Test chat interactions with the backend
- Verify data persistence with Neon PostgreSQL
- Use kubectl-ai to scale services as needed

## AI-Assisted Operations

### Using kubectl-ai
```bash
# Scale backend replicas
kubectl-ai "scale backend deployment to 3 replicas"

# Check service status
kubectl-ai "show me the status of all services"

# Debug pod issues
kubectl-ai "why is my backend pod not starting?"
```

### Using kagent
```bash
# Analyze cluster health
kagent analyze

# Get optimization recommendations
kagent optimize
```

## Troubleshooting

1. **Pods not starting**: Check logs with `kubectl logs <pod-name>`
2. **Service not accessible**: Verify service type and ports with `kubectl get services`
3. **Database connection issues**: Check if Neon PostgreSQL credentials are correctly configured in Secrets
4. **Frontend cannot reach backend**: Verify service names and network connectivity