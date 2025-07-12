# ADR-006: Docker Containerization and Deployment Strategy

## Metadata
- **Status**: Accepted
- **Date**: 2025-07-12
- **Deciders**: AI Agent, DevOps Engineer
- **Technical Story**: US-007 - Docker Production Deployment
- **Rule Compliance**: rules-101 v1.2+, rules-102 v1.2+, rules-103 v1.2+

## Context and Problem Statement

The AI Linguistics Agent requires a robust, scalable, and consistent deployment strategy across development, staging, and production environments. The system consists of multiple components (FastAPI application, PostgreSQL, Neo4j, ChromaDB) that need orchestration, networking, and persistent storage management.

**Key Requirements:**
- Consistent deployment across all environments
- Multi-service orchestration (API, databases, web interface)
- Production-ready configuration with health checks
- Scalable architecture supporting horizontal scaling
- Development environment parity with production
- Automated deployment and rollback capabilities

## Decision Drivers

- **Consistency**: Identical environments across dev/staging/production
- **Scalability**: Support for horizontal scaling and load balancing
- **Isolation**: Service isolation and dependency management
- **Portability**: Platform-independent deployment
- **Automation**: Automated deployment and configuration management
- **Monitoring**: Health checks and observability integration
- **Security**: Container security and network isolation

## Considered Options

### Option 1: Docker Compose for Full Stack Orchestration
- **Pros**:
  - Simple multi-service orchestration
  - Excellent for development and small-scale production
  - Built-in networking and volume management
  - Easy environment variable configuration
  - Good integration with CI/CD pipelines
- **Cons**:
  - Limited scaling capabilities compared to Kubernetes
  - Single-host deployment limitation
  - Less sophisticated health checking

### Option 2: Kubernetes with Helm Charts
- **Pros**:
  - Enterprise-grade orchestration and scaling
  - Advanced health checking and self-healing
  - Sophisticated networking and service discovery
  - Excellent for large-scale deployments
- **Cons**:
  - High complexity for smaller deployments
  - Steep learning curve
  - Overkill for initial requirements

### Option 3: Docker Swarm
- **Pros**:
  - Native Docker orchestration
  - Simpler than Kubernetes
  - Good scaling capabilities
- **Cons**:
  - Less ecosystem support than Kubernetes
  - Limited advanced features
  - Declining community adoption

### Option 4: Traditional VM Deployment
- **Pros**:
  - Familiar deployment model
  - Full OS control
- **Cons**:
  - Resource inefficiency
  - Complex dependency management
  - Inconsistent environments

## Decision Outcome

**Chosen option**: Option 1 - Docker Compose for Full Stack Orchestration

**Rationale:**
1. **Simplicity**: Appropriate complexity for current scale and requirements
2. **Development Parity**: Identical environments from development to production
3. **Multi-Service Support**: Excellent orchestration for our service architecture
4. **Rapid Deployment**: Quick setup and deployment cycles
5. **Future Migration Path**: Easy migration to Kubernetes when scaling needs increase
6. **Community Support**: Excellent documentation and community resources

## Positive Consequences

- **Environment Consistency**: Identical configuration across all environments
- **Rapid Development**: Quick local development environment setup
- **Service Isolation**: Clean separation of concerns between services
- **Easy Scaling**: Simple horizontal scaling within single-host limits
- **Simplified Deployment**: Single-command deployment and updates
- **Resource Efficiency**: Optimal resource utilization with containers

## Negative Consequences

- **Single-Host Limitation**: Cannot scale beyond single host without orchestrator
- **Limited High Availability**: No built-in multi-host failover
- **Monitoring Complexity**: Requires additional tooling for comprehensive monitoring
- **Network Complexity**: Advanced networking features require additional configuration

## Implementation Details

### Docker Compose Architecture
```yaml
# docker-compose.yml
version: '3.8'

services:
  # Main Application
  linguistics-agent:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@postgres:5432/linguistics_agent
      - NEO4J_URI=bolt://neo4j:7687
      - CHROMADB_HOST=chromadb
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      neo4j:
        condition: service_healthy
      chromadb:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
    networks:
      - linguistics-network

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=linguistics_agent
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - linguistics-network

  # Neo4j Graph Database
  neo4j:
    image: neo4j:5.13-community
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
      - NEO4J_PLUGINS=["apoc"]
      - NEO4J_dbms_security_procedures_unrestricted=apoc.*
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "${NEO4J_PASSWORD}", "RETURN 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    restart: unless-stopped
    networks:
      - linguistics-network

  # ChromaDB Vector Database
  chromadb:
    image: chromadb/chroma:latest
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_PORT=8001
    volumes:
      - chromadb_data:/chroma/chroma
    ports:
      - "8001:8001"
    restart: unless-stopped
    networks:
      - linguistics-network

  # React Web Interface
  web-interface:
    build:
      context: ./web-interface
      dockerfile: Dockerfile
      target: production
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - linguistics-agent
    restart: unless-stopped
    networks:
      - linguistics-network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - linguistics-agent
      - web-interface
    restart: unless-stopped
    networks:
      - linguistics-network

volumes:
  postgres_data:
    driver: local
  neo4j_data:
    driver: local
  neo4j_logs:
    driver: local
  chromadb_data:
    driver: local

networks:
  linguistics-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Multi-Stage Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create application user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set work directory
WORKDIR /app

# Development stage
FROM base as development

# Install development dependencies
COPY requirements/dev.txt .
RUN pip install -r dev.txt

# Copy source code
COPY . .

# Change ownership to appuser
RUN chown -R appuser:appuser /app
USER appuser

# Development command
CMD ["uvicorn", "linguistics_agent.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production

# Install production dependencies only
COPY requirements/prod.txt .
RUN pip install -r prod.txt

# Copy application code
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Change ownership to appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command
CMD ["gunicorn", "linguistics_agent.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Environment Configuration
```bash
# .env.production
POSTGRES_PASSWORD=secure_production_password
NEO4J_PASSWORD=secure_neo4j_password
JWT_SECRET_KEY=your_super_secure_jwt_secret_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Application settings
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG=false

# Database settings
DATABASE_URL=postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@postgres:5432/linguistics_agent
NEO4J_URI=bolt://neo4j:7687
CHROMADB_HOST=chromadb

# Security settings
ALLOWED_HOSTS=["localhost", "your-domain.com"]
CORS_ORIGINS=["https://your-domain.com"]
```

### Nginx Configuration
```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream linguistics_api {
        server linguistics-agent:8000;
    }

    upstream web_interface {
        server web-interface:3000;
    }

    # API Server
    server {
        listen 80;
        server_name api.linguistics-agent.com;

        location / {
            proxy_pass http://linguistics_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check endpoint
        location /health {
            proxy_pass http://linguistics_api/health;
            access_log off;
        }
    }

    # Web Interface
    server {
        listen 80;
        server_name linguistics-agent.com;

        location / {
            proxy_pass http://web_interface;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # API proxy for web interface
        location /api/ {
            proxy_pass http://linguistics_api/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Deployment Scripts
```bash
#!/bin/bash
# deploy.sh - Production deployment script

set -e

echo "🚀 Starting AI Linguistics Agent deployment..."

# Load environment variables
if [ -f .env.production ]; then
    export $(cat .env.production | grep -v '#' | xargs)
fi

# Pull latest images
echo "📦 Pulling latest images..."
docker-compose pull

# Build application images
echo "🔨 Building application images..."
docker-compose build --no-cache

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose run --rm linguistics-agent alembic upgrade head

# Start services
echo "🎯 Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
timeout 300 bash -c 'until docker-compose ps | grep -q "healthy"; do sleep 5; done'

# Run health checks
echo "🏥 Running health checks..."
curl -f http://localhost:8000/health || exit 1

echo "✅ Deployment completed successfully!"
```

### Monitoring and Logging
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  # Prometheus for metrics
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - linguistics-network

  # Grafana for visualization
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
    networks:
      - linguistics-network

  # Log aggregation
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./monitoring/loki.yml:/etc/loki/local-config.yaml
      - loki_data:/loki
    networks:
      - linguistics-network

volumes:
  prometheus_data:
  grafana_data:
  loki_data:
```

## Security Considerations

### Container Security
```dockerfile
# Security-hardened Dockerfile additions
FROM python:3.11-slim as base

# Security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    curl gcc && \
    rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Secure file permissions
COPY --chown=appuser:appuser . .
USER appuser

# Read-only root filesystem
VOLUME ["/tmp"]
```

### Network Security
```yaml
# Network isolation
networks:
  linguistics-network:
    driver: bridge
    internal: false  # Allow external access only where needed
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1

  internal-network:
    driver: bridge
    internal: true  # Internal-only network for database communication
```

### Secrets Management
```bash
# Use Docker secrets for sensitive data
echo "secure_password" | docker secret create postgres_password -
echo "jwt_secret_key" | docker secret create jwt_secret -

# Reference in compose file
services:
  postgres:
    secrets:
      - postgres_password
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password
```

## Scaling Strategy

### Horizontal Scaling
```yaml
# docker-compose.scale.yml
services:
  linguistics-agent:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

  # Load balancer
  nginx:
    depends_on:
      - linguistics-agent
    deploy:
      replicas: 1
```

### Resource Limits
```yaml
services:
  linguistics-agent:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

## Backup Strategy

### Database Backups
```bash
#!/bin/bash
# backup.sh - Automated backup script

# PostgreSQL backup
docker-compose exec postgres pg_dump -U postgres linguistics_agent > backup_$(date +%Y%m%d_%H%M%S).sql

# Neo4j backup
docker-compose exec neo4j neo4j-admin dump --database=neo4j --to=/backups/neo4j_$(date +%Y%m%d_%H%M%S).dump

# ChromaDB backup
docker-compose exec chromadb tar -czf /backups/chromadb_$(date +%Y%m%d_%H%M%S).tar.gz /chroma/chroma
```

## Testing Strategy

### Container Testing
```python
# test_docker_deployment.py
import pytest
import docker
import requests
import time

@pytest.fixture
def docker_client():
    return docker.from_env()

def test_container_startup(docker_client):
    """Test that all containers start successfully."""
    # Start services
    subprocess.run(["docker-compose", "up", "-d"], check=True)

    # Wait for health checks
    time.sleep(60)

    # Verify all services are running
    containers = docker_client.containers.list()
    service_names = [c.name for c in containers]

    assert "linguistics-agent" in service_names
    assert "postgres" in service_names
    assert "neo4j" in service_names
    assert "chromadb" in service_names

def test_api_health_check():
    """Test API health check endpoint."""
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_database_connectivity():
    """Test database connectivity."""
    # Test PostgreSQL
    response = requests.get("http://localhost:8000/api/v1/health/database")
    assert response.status_code == 200

    # Test Neo4j
    response = requests.get("http://localhost:8000/api/v1/health/neo4j")
    assert response.status_code == 200
```

## Compliance and Validation

### Rule Compliance
- **rules-101**: TDD approach with comprehensive deployment testing
- **rules-102**: Documented architectural decision with deployment rationale
- **rules-103**: Implementation follows containerization best practices
- **rules-104**: Addresses US-007 deployment requirements completely

### Production Requirements
- 99.9% uptime with health checks and restart policies
- Horizontal scaling capability within single-host limits
- Automated deployment and rollback procedures
- Comprehensive monitoring and logging

## Related Decisions

- **ADR-003**: FastAPI Framework Selection (containerized API)
- **ADR-004**: PostgreSQL State Management (database containerization)
- **ADR-008**: React Web Interface (frontend containerization)

## Migration Strategy

Future migration to Kubernetes:
1. **Helm Chart Creation**: Convert Docker Compose to Helm charts
2. **Service Mesh**: Implement Istio for advanced networking
3. **Horizontal Pod Autoscaling**: Implement automatic scaling
4. **Persistent Volume Claims**: Migrate to Kubernetes storage
5. **Ingress Controllers**: Replace Nginx with Kubernetes ingress

## Notes

- Monitor container resource usage and optimize as needed
- Consider implementing container image scanning for security
- Evaluate migration to Kubernetes when scaling beyond single host
- Plan for multi-region deployment for high availability

---

**Decision Status**: ✅ Accepted
**Implementation Status**: Ready for Development
**Next Review**: 2025-08-12 (monthly review)
**Rule Compliance**: ✅ rules-101 v1.2+, rules-102 v1.2+, rules-103 v1.2+
