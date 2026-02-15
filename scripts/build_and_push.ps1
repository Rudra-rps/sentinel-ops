param(
    [string]$Registry = "your-registry",
    [string]$Org = "your-org",
    [string]$Tag = "latest"
)

$backend = "$Registry/$Org/sentinelops-backend:$Tag"
$frontend = "$Registry/$Org/sentinelops-frontend:$Tag"

Write-Host "Building backend: $backend"
docker build -f Dockerfile.backend -t $backend .

Write-Host "Building frontend: $frontend"
docker build -f frontend/Dockerfile.frontend -t $frontend frontend

Write-Host "Pushing images"
docker push $backend
docker push $frontend

Write-Host "Done. Images pushed: $backend, $frontend"
