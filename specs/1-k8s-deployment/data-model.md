# Data Model: Local Kubernetes Deployment (Cloud Native + AIOps)

## Phase 1: Kubernetes Resources and Configuration

### Entity: Frontend Service
- **Fields**: image, replicas, ports, environment variables, resources
- **Relationships**: Depends on backend service for API calls
- **Validation rules**: Must expose correct port for UI access
- **State transitions**: Running → Terminating (during updates)

### Entity: Backend Service
- **Fields**: image, replicas, ports, environment variables, database connection config, resources
- **Relationships**: Connects to external Neon PostgreSQL database
- **Validation rules**: Must establish database connection successfully
- **State transitions**: Running → Terminating (during updates)

### Entity: Kubernetes Deployment
- **Fields**: name, namespace, replicas, selector, template, containers
- **Relationships**: Manages pods for frontend/backend services
- **Validation rules**: Must have proper resource requests and limits
- **State transitions**: Active → Updating → Active (during rollouts)

### Entity: Kubernetes Service
- **Fields**: name, type (ClusterIP/NodePort), ports, selector
- **Relationships**: Exposes deployments internally/externally
- **Validation rules**: Must route traffic to correct pods
- **State transitions**: Available → Unavailable (during disruptions)

### Entity: Kubernetes ConfigMap
- **Fields**: name, namespace, data (key-value pairs)
- **Relationships**: Referenced by deployments for configuration
- **Validation rules**: Must contain valid configuration values
- **State transitions**: Created → Updated → Deleted

### Entity: Kubernetes Secret
- **Fields**: name, namespace, data (base64 encoded)
- **Relationships**: Referenced by deployments for sensitive data
- **Validation rules**: Must contain required database credentials
- **State transitions**: Created → Updated → Deleted

### Entity: Helm Chart
- **Fields**: name, version, appVersion, dependencies, values
- **Relationships**: Contains templates for Kubernetes resources
- **Validation rules**: Must follow Helm best practices and templating
- **State transitions**: Packaging → Installation → Upgrade

### Entity: Helm Values
- **Fields**: replicas, image tags, resource limits, environment variables
- **Relationships**: Overrides default chart values
- **Validation rules**: Must contain valid configuration parameters
- **State transitions**: Default → Overridden → Applied