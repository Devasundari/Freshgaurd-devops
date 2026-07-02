@echo off

echo =======================================
echo Deploying FreshGuard to Kubernetes...
echo =======================================

kubectl apply -f k8s\deployment.yml
kubectl apply -f k8s\service.yml

kubectl get deployments
kubectl get pods
kubectl get services

echo Deployment completed successfully!
pause