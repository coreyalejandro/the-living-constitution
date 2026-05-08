#!/bin/bash
set -euo pipefail

# The Living Constitution - Enterprise Deployment Script
# This script deploys the TLC platform to production Kubernetes cluster

# Configuration
NAMESPACE="tlc-production"
MONITORING_NAMESPACE="tlc-monitoring"
HELM_CHART_PATH="./helm/tlc-chart"
DOCKER_REGISTRY="ghcr.io"
IMAGE_TAG="${IMAGE_TAG:-latest}"
ENVIRONMENT="${ENVIRONMENT:-production}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if kubectl is installed and configured
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed or not in PATH"
        exit 1
    fi
    
    # Check if helm is installed
    if ! command -v helm &> /dev/null; then
        log_error "helm is not installed or not in PATH"
        exit 1
    fi
    
    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check kubectl connectivity
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    # Check required environment variables
    required_vars=(
        "DATABASE_PASSWORD"
        "ANTHROPIC_API_KEY"
        "JWT_SECRET"
        "ENCRYPTION_KEY"
        "SESSION_SECRET"
        "GUARDIAN_API_KEY"
    )
    
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            log_error "Required environment variable $var is not set"
            exit 1
        fi
    done
    
    log_success "Prerequisites check passed"
}

# Build and push Docker images
build_and_push_images() {
    log_info "Building and pushing Docker images..."
    
    # Build control plane image
    log_info "Building control-plane image..."
    docker build -f docker/control-plane.Dockerfile -t "${DOCKER_REGISTRY}/tlc-control-plane:${IMAGE_TAG}" .
    docker push "${DOCKER_REGISTRY}/tlc-control-plane:${IMAGE_TAG}"
    
    # Build semgraph image
    log_info "Building semgraph image..."
    docker build -f docker/semgraph.Dockerfile -t "${DOCKER_REGISTRY}/tlc-semgraph:${IMAGE_TAG}" .
    docker push "${DOCKER_REGISTRY}/tlc-semgraph:${IMAGE_TAG}"
    
    # Build guardian image
    log_info "Building guardian image..."
    docker build -f docker/guardian.Dockerfile -t "${DOCKER_REGISTRY}/tlc-guardian:${IMAGE_TAG}" .
    docker push "${DOCKER_REGISTRY}/tlc-guardian:${IMAGE_TAG}"
    
    log_success "Docker images built and pushed successfully"
}

# Create namespaces
create_namespaces() {
    log_info "Creating namespaces..."
    
    kubectl apply -f k8s/namespace.yaml
    
    # Create monitoring namespace
    kubectl create namespace ${MONITORING_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
    
    log_success "Namespaces created"
}

# Deploy infrastructure components
deploy_infrastructure() {
    log_info "Deploying infrastructure components..."
    
    # Apply ConfigMap
    kubectl apply -f k8s/configmap.yaml
    
    # Create secrets
    kubectl create secret generic tlc-secrets \
        --from-literal=DATABASE_PASSWORD="${DATABASE_PASSWORD}" \
        --from-literal=DATABASE_URL="postgresql://tlc_user:${DATABASE_PASSWORD}@postgres-service:5432/tlc_db" \
        --from-literal=ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
        --from-literal=OPENAI_API_KEY="${OPENAI_API_KEY:-}" \
        --from-literal=GOOGLE_API_KEY="${GOOGLE_API_KEY:-}" \
        --from-literal=JWT_SECRET="${JWT_SECRET}" \
        --from-literal=ENCRYPTION_KEY="${ENCRYPTION_KEY}" \
        --from-literal=SESSION_SECRET="${SESSION_SECRET}" \
        --from-literal=GUARDIAN_API_KEY="${GUARDIAN_API_KEY}" \
        --from-literal=GRAFANA_ADMIN_PASSWORD="${GRAFANA_ADMIN_PASSWORD:-admin123}" \
        --namespace=${NAMESPACE} \
        --dry-run=client -o yaml | kubectl apply -f -
    
    kubectl create secret generic postgres-secret \
        --from-literal=POSTGRES_DB="tlc_db" \
        --from-literal=POSTGRES_USER="tlc_user" \
        --from-literal=POSTGRES_PASSWORD="${DATABASE_PASSWORD}" \
        --namespace=${NAMESPACE} \
        --dry-run=client -o yaml | kubectl apply -f -
    
    # Deploy database
    kubectl apply -f k8s/database.yaml
    log_info "Waiting for database to be ready..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=database -n ${NAMESPACE} --timeout=300s
    
    # Deploy Redis
    kubectl apply -f k8s/redis.yaml
    log_info "Waiting for Redis to be ready..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=redis -n ${NAMESPACE} --timeout=300s
    
    log_success "Infrastructure components deployed"
}

# Deploy application services
deploy_applications() {
    log_info "Deploying application services..."
    
    # Update image tags in deployment files
    sed -i.bak "s|image: ghcr.io/.*|image: ${DOCKER_REGISTRY}/tlc-guardian:${IMAGE_TAG}|g" k8s/guardian-deployment.yaml
    sed -i.bak "s|image: ghcr.io/.*|image: ${DOCKER_REGISTRY}/tlc-semgraph:${IMAGE_TAG}|g" k8s/semgraph-deployment.yaml
    sed -i.bak "s|image: ghcr.io/.*|image: ${DOCKER_REGISTRY}/tlc-control-plane:${IMAGE_TAG}|g" k8s/control-plane-deployment.yaml
    
    # Deploy Guardian service
    kubectl apply -f k8s/guardian-deployment.yaml
    log_info "Waiting for Guardian to be ready..."
    kubectl rollout status deployment/guardian -n ${NAMESPACE} --timeout=600s
    
    # Deploy Semgraph service
    kubectl apply -f k8s/semgraph-deployment.yaml
    log_info "Waiting for Semgraph to be ready..."
    kubectl rollout status deployment/semgraph -n ${NAMESPACE} --timeout=600s
    
    # Deploy Control Plane
    kubectl apply -f k8s/control-plane-deployment.yaml
    log_info "Waiting for Control Plane to be ready..."
    kubectl rollout status deployment/control-plane -n ${NAMESPACE} --timeout=600s
    
    # Restore original deployment files
    mv k8s/guardian-deployment.yaml.bak k8s/guardian-deployment.yaml
    mv k8s/semgraph-deployment.yaml.bak k8s/semgraph-deployment.yaml
    mv k8s/control-plane-deployment.yaml.bak k8s/control-plane-deployment.yaml
    
    log_success "Application services deployed"
}

# Deploy monitoring stack
deploy_monitoring() {
    log_info "Deploying monitoring stack..."
    
    kubectl apply -f k8s/monitoring.yaml
    
    log_info "Waiting for Prometheus to be ready..."
    kubectl rollout status deployment/prometheus -n ${MONITORING_NAMESPACE} --timeout=300s
    
    log_info "Waiting for Grafana to be ready..."
    kubectl rollout status deployment/grafana -n ${MONITORING_NAMESPACE} --timeout=300s
    
    log_success "Monitoring stack deployed"
}

# Deploy networking
deploy_networking() {
    log_info "Deploying networking components..."
    
    kubectl apply -f k8s/ingress.yaml
    
    log_success "Networking components deployed"
}

# Run health checks
run_health_checks() {
    log_info "Running health checks..."
    
    # Wait a bit for services to stabilize
    sleep 30
    
    # Check Control Plane health
    log_info "Checking Control Plane health..."
    if kubectl run health-check-control-plane --image=curlimages/curl:latest --rm -i --restart=Never -- \
        curl -f http://control-plane-service.${NAMESPACE}.svc.cluster.local:3000/api/health; then
        log_success "Control Plane health check passed"
    else
        log_error "Control Plane health check failed"
        return 1
    fi
    
    # Check Semgraph health
    log_info "Checking Semgraph health..."
    if kubectl run health-check-semgraph --image=curlimages/curl:latest --rm -i --restart=Never -- \
        curl -f http://semgraph-service.${NAMESPACE}.svc.cluster.local:8000/health; then
        log_success "Semgraph health check passed"
    else
        log_error "Semgraph health check failed"
        return 1
    fi
    
    # Check Guardian health
    log_info "Checking Guardian health..."
    if kubectl run health-check-guardian --image=curlimages/curl:latest --rm -i --restart=Never -- \
        curl -f http://guardian-service.${NAMESPACE}.svc.cluster.local:8001/health; then
        log_success "Guardian health check passed"
    else
        log_error "Guardian health check failed"
        return 1
    fi
    
    # Check database connectivity
    log_info "Checking database connectivity..."
    if kubectl run db-check --image=postgres:15-alpine --rm -i --restart=Never --env="PGPASSWORD=${DATABASE_PASSWORD}" -- \
        psql -h postgres-service.${NAMESPACE}.svc.cluster.local -U tlc_user -d tlc_db -c "SELECT 1;"; then
        log_success "Database connectivity check passed"
    else
        log_error "Database connectivity check failed"
        return 1
    fi
    
    # Check Redis connectivity
    log_info "Checking Redis connectivity..."
    if kubectl run redis-check --image=redis:7-alpine --rm -i --restart=Never -- \
        redis-cli -h redis-service.${NAMESPACE}.svc.cluster.local ping; then
        log_success "Redis connectivity check passed"
    else
        log_error "Redis connectivity check failed"
        return 1
    fi
    
    log_success "All health checks passed"
}

# Run constitutional validation
run_constitutional_validation() {
    log_info "Running constitutional validation..."
    
    kubectl run constitutional-validation --image=python:3.11-slim --rm -i --restart=Never -- \
        bash -c "pip install requests && python -c \"
import requests
import sys

# Test constitutional AI endpoints
try:
    response = requests.get('http://control-plane-service.${NAMESPACE}.svc.cluster.local:3000/api/constitutional/validate', timeout=30)
    if response.status_code == 200:
        print('Constitutional validation endpoint: OK')
    else:
        print(f'Constitutional validation endpoint failed: {response.status_code}')
        
    response = requests.get('http://guardian-service.${NAMESPACE}.svc.cluster.local:8001/invariants/check', timeout=30)
    if response.status_code == 200:
        print('Guardian invariants endpoint: OK')
    else:
        print(f'Guardian invariants endpoint failed: {response.status_code}')
        
    print('Constitutional validation checks completed')
except Exception as e:
    print(f'Constitutional validation failed: {e}')
    sys.exit(1)
\""
    
    log_success "Constitutional validation completed"
}

# Display deployment status
show_deployment_status() {
    log_info "Deployment Status:"
    echo
    echo "Pods:"
    kubectl get pods -n ${NAMESPACE}
    echo
    echo "Services:"
    kubectl get services -n ${NAMESPACE}
    echo
    echo "Ingress:"
    kubectl get ingress -n ${NAMESPACE}
    echo
    
    # Get external IP/URL if available
    EXTERNAL_IP=$(kubectl get ingress tlc-ingress -n ${NAMESPACE} -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
    if [[ -n "$EXTERNAL_IP" ]]; then
        log_success "Application is accessible at: http://${EXTERNAL_IP}"
    else
        log_info "External IP not yet assigned. Check ingress status with: kubectl get ingress -n ${NAMESPACE}"
    fi
}

# Rollback function
rollback_deployment() {
    log_warning "Rolling back deployment..."
    
    kubectl rollout undo deployment/control-plane -n ${NAMESPACE}
    kubectl rollout undo deployment/semgraph -n ${NAMESPACE}
    kubectl rollout undo deployment/guardian -n ${NAMESPACE}
    
    kubectl rollout status deployment/control-plane -n ${NAMESPACE} --timeout=300s
    kubectl rollout status deployment/semgraph -n ${NAMESPACE} --timeout=300s
    kubectl rollout status deployment/guardian -n ${NAMESPACE} --timeout=300s
    
    log_success "Rollback completed"
}

# Main deployment function
main() {
    log_info "Starting The Living Constitution deployment..."
    log_info "Environment: ${ENVIRONMENT}"
    log_info "Image Tag: ${IMAGE_TAG}"
    log_info "Namespace: ${NAMESPACE}"
    
    # Trap to handle errors
    trap 'log_error "Deployment failed. Check the logs above for details."; exit 1' ERR
    
    check_prerequisites
    
    if [[ "${SKIP_BUILD:-false}" != "true" ]]; then
        build_and_push_images
    else
        log_info "Skipping image build (SKIP_BUILD=true)"
    fi
    
    create_namespaces
    deploy_infrastructure
    deploy_applications
    deploy_monitoring
    deploy_networking
    
    if run_health_checks; then
        run_constitutional_validation
        show_deployment_status
        log_success "Deployment completed successfully!"
    else
        log_error "Health checks failed. Rolling back..."
        rollback_deployment
        exit 1
    fi
}

# Handle command line arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "rollback")
        rollback_deployment
        ;;
    "health-check")
        run_health_checks
        ;;
    "status")
        show_deployment_status
        ;;
    *)
        echo "Usage: $0 [deploy|rollback|health-check|status]"
        echo "  deploy      - Full deployment (default)"
        echo "  rollback    - Rollback to previous version"
        echo "  health-check - Run health checks only"
        echo "  status      - Show deployment status"
        exit 1
        ;;
esac