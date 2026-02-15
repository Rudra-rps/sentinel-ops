#!/usr/bin/env bash
set -euo pipefail

REGISTRY=${1:-your-registry}
ORG=${2:-your-org}
TAG=${3:-latest}

BACKEND_IMAGE="$REGISTRY/$ORG/sentinelops-backend:$TAG"
FRONTEND_IMAGE="$REGISTRY/$ORG/sentinelops-frontend:$TAG"

echo "Building backend image: $BACKEND_IMAGE"
docker build -f Dockerfile.backend -t "$BACKEND_IMAGE" .

echo "Building frontend image: $FRONTEND_IMAGE"
docker build -f frontend/Dockerfile.frontend -t "$FRONTEND_IMAGE" frontend

echo "Pushing images to registry"
docker push "$BACKEND_IMAGE"
docker push "$FRONTEND_IMAGE"

echo "Done. Images pushed:"
echo "  $BACKEND_IMAGE"
echo "  $FRONTEND_IMAGE"
