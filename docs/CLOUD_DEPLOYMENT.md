# Cloud Deployment Guide

Complete guide for deploying the churn prediction ML service to production cloud environments.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Docker Deployment](#docker-deployment)
3. [AWS Deployment (EKS)](#aws-deployment-eks)
4. [GCP Deployment (GKE)](#gcp-deployment-gke)
5. [Azure Deployment (AKS)](#azure-deployment-aks)
6. [CI/CD Integration](#cicd-integration)
7. [Monitoring & Observability](#monitoring--observability)

---

## Prerequisites

### Required Tools

```bash
# Docker
docker --version  # >= 20.10

# Kubernetes CLI
kubectl version --client  # >= 1.24

# Cloud CLIs
aws --version      # AWS
gcloud --version   # GCP
az --version       # Azure

# Optional but recommended
helm version       # Package manager for K8s
terraform --version  # Infrastructure as Code
```

### Trained Model

Ensure you have a trained model:

```bash
make train  # Creates models/churn_model.pkl and models/preprocessor.pkl
```

---

## Docker Deployment

### 1. Build Docker Image

```bash
# Build the image
docker build -t churn-prediction:1.0.0 .

# Or using make
make docker-build
```

### 2. Run Locally

```bash
# Run container
docker run -d \
  --name churn-api \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models:ro \
  churn-prediction:1.0.0

# Check logs
docker logs -f churn-api

# Test API
curl http://localhost:8000/health
```

### 3. Test Predictions

```bash
curl -X POST http://localhost:8000/predict/single \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.35,
    "TotalCharges": 840.20
  }'
```

### 4. Push to Container Registry

```bash
# Docker Hub
docker tag churn-prediction:1.0.0 yourusername/churn-prediction:1.0.0
docker push yourusername/churn-prediction:1.0.0

# AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag churn-prediction:1.0.0 <account-id>.dkr.ecr.us-east-1.amazonaws.com/churn-prediction:1.0.0
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/churn-prediction:1.0.0

# GCP GCR
gcloud auth configure-docker
docker tag churn-prediction:1.0.0 gcr.io/<project-id>/churn-prediction:1.0.0
docker push gcr.io/<project-id>/churn-prediction:1.0.0

# Azure ACR
az acr login --name <registry-name>
docker tag churn-prediction:1.0.0 <registry-name>.azurecr.io/churn-prediction:1.0.0
docker push <registry-name>.azurecr.io/churn-prediction:1.0.0
```

---

## AWS Deployment (EKS)

### 1. Create EKS Cluster

```bash
# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Create cluster
eksctl create cluster \
  --name ml-production \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 5 \
  --managed

# Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name ml-production
```

### 2. Create ECR Repository

```bash
# Create repository
aws ecr create-repository \
  --repository-name churn-prediction \
  --region us-east-1

# Get login credentials
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

### 3. Deploy to EKS

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create ConfigMap
kubectl apply -f k8s/configmap.yaml

# Create RBAC
kubectl apply -f k8s/rbac.yaml

# Create PVC (use EBS for AWS)
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-storage-pvc
  namespace: ml-production
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: gp3  # AWS EBS
  resources:
    requests:
      storage: 5Gi
EOF

# Update deployment with ECR image
# Edit k8s/deployment.yaml - change image to your ECR URL
kubectl apply -f k8s/deployment.yaml

# Create service
kubectl apply -f k8s/service.yaml

# Create HPA
kubectl apply -f k8s/hpa.yaml

# Install ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/aws/deploy.yaml

# Create ingress
kubectl apply -f k8s/ingress.yaml
```

### 4. Upload Model to PVC

```bash
# Create a pod to upload models
kubectl run -n ml-production model-uploader --image=busybox --restart=Never \
  --overrides='
{
  "spec": {
    "containers": [{
      "name": "model-uploader",
      "image": "busybox",
      "command": ["sleep", "3600"],
      "volumeMounts": [{
        "name": "models",
        "mountPath": "/models"
      }]
    }],
    "volumes": [{
      "name": "models",
      "persistentVolumeClaim": {
        "claimName": "model-storage-pvc"
      }
    }]
  }
}'

# Copy models
kubectl cp models/churn_model.pkl ml-production/model-uploader:/models/
kubectl cp models/preprocessor.pkl ml-production/model-uploader:/models/

# Delete uploader pod
kubectl delete pod -n ml-production model-uploader
```

### 5. Verify Deployment

```bash
# Check pods
kubectl get pods -n ml-production

# Check service
kubectl get svc -n ml-production

# Get LoadBalancer URL
kubectl get ingress -n ml-production

# Test API
INGRESS_URL=$(kubectl get ingress -n ml-production churn-prediction-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl http://$INGRESS_URL/health
```

### 6. Enable Auto-scaling

```bash
# Install Metrics Server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify HPA
kubectl get hpa -n ml-production

# Watch autoscaling
kubectl get hpa -n ml-production -w
```

---

## GCP Deployment (GKE)

### 1. Create GKE Cluster

```bash
# Set project
gcloud config set project <project-id>

# Create cluster
gcloud container clusters create ml-production \
  --region us-central1 \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 5 \
  --enable-autorepair \
  --enable-autoupgrade

# Get credentials
gcloud container clusters get-credentials ml-production --region us-central1
```

### 2. Create GCR Repository

```bash
# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Configure Docker
gcloud auth configure-docker

# Tag and push
docker tag churn-prediction:1.0.0 gcr.io/<project-id>/churn-prediction:1.0.0
docker push gcr.io/<project-id>/churn-prediction:1.0.0
```

### 3. Deploy to GKE

```bash
# Apply all manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/rbac.yaml

# Create PVC with GCP Persistent Disk
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-storage-pvc
  namespace: ml-production
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: standard-rwo  # GCP Persistent Disk
  resources:
    requests:
      storage: 5Gi
EOF

# Update deployment with GCR image
# Edit k8s/deployment.yaml - change image to gcr.io URL
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Install ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

kubectl apply -f k8s/ingress.yaml
```

### 4. Set up Cloud Load Balancer

```bash
# Get external IP
kubectl get svc -n ingress-nginx

# Configure DNS
# Point your domain to the external IP
```

---

## Azure Deployment (AKS)

### 1. Create AKS Cluster

```bash
# Create resource group
az group create --name ml-production-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group ml-production-rg \
  --name ml-production \
  --node-count 3 \
  --node-vm-size Standard_D2s_v3 \
  --enable-cluster-autoscaler \
  --min-count 2 \
  --max-count 5 \
  --enable-managed-identity \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group ml-production-rg --name ml-production
```

### 2. Create ACR Repository

```bash
# Create ACR
az acr create \
  --resource-group ml-production-rg \
  --name <registry-name> \
  --sku Basic

# Attach ACR to AKS
az aks update \
  --resource-group ml-production-rg \
  --name ml-production \
  --attach-acr <registry-name>

# Login and push
az acr login --name <registry-name>
docker tag churn-prediction:1.0.0 <registry-name>.azurecr.io/churn-prediction:1.0.0
docker push <registry-name>.azurecr.io/churn-prediction:1.0.0
```

### 3. Deploy to AKS

```bash
# Apply manifests (similar to AWS/GCP)
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/rbac.yaml

# Create PVC with Azure Disk
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-storage-pvc
  namespace: ml-production
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: managed-premium  # Azure Premium SSD
  resources:
    requests:
      storage: 5Gi
EOF

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml
```

---

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/deploy.yaml`:

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  IMAGE_NAME: churn-prediction
  K8S_NAMESPACE: ml-production

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ secrets.REGISTRY_URL }}
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ secrets.REGISTRY_URL }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
    
    - name: Deploy to K8s
      uses: azure/k8s-deploy@v4
      with:
        namespace: ${{ env.K8S_NAMESPACE }}
        manifests: |
          k8s/deployment.yaml
          k8s/service.yaml
        images: ${{ secrets.REGISTRY_URL }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
```

---

## Monitoring & Observability

### 1. Prometheus & Grafana

```bash
# Install Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Default: admin/prom-operator
```

### 2. Application Logs

```bash
# View logs
kubectl logs -n ml-production -l app=churn-prediction --tail=100 -f

# Install ELK stack or use cloud-native solutions
# AWS: CloudWatch
# GCP: Cloud Logging
# Azure: Azure Monitor
```

### 3. Data Drift Monitoring

```bash
# Run drift monitoring
make drift-monitor

# Schedule as CronJob in K8s
kubectl apply -f k8s/cronjobs/drift-monitor.yaml
```

---

## Cost Optimization

### AWS
- Use Spot Instances for non-critical workloads
- Enable Cluster Autoscaler
- Use Savings Plans

### GCP
- Use Preemptible VMs
- Enable node auto-provisioning
- Use Committed Use Discounts

### Azure
- Use Spot VMs
- Enable cluster autoscaler
- Use Reserved Instances

---

## Security Best Practices

1. **Network Security**
   - Use Network Policies
   - Enable Pod Security Policies
   - Use private subnets

2. **Secrets Management**
   - Use cloud-native secrets (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault)
   - Never commit secrets to Git

3. **RBAC**
   - Principle of least privilege
   - Separate service accounts per application

4. **Image Security**
   - Scan images for vulnerabilities
   - Use minimal base images
   - Sign images

---

## Troubleshooting

### Pod not starting

```bash
kubectl describe pod -n ml-production <pod-name>
kubectl logs -n ml-production <pod-name>
```

### Service not accessible

```bash
kubectl get svc -n ml-production
kubectl get endpoints -n ml-production
```

### Model not loading

```bash
# Check PVC
kubectl get pvc -n ml-production

# Check if models are in PVC
kubectl exec -n ml-production <pod-name> -- ls -la /app/models
```

---

## Rollback

```bash
# View deployment history
kubectl rollout history deployment/churn-prediction -n ml-production

# Rollback to previous version
kubectl rollout undo deployment/churn-prediction -n ml-production

# Rollback to specific revision
kubectl rollout undo deployment/churn-prediction -n ml-production --to-revision=2
```

---

## Next Steps

- [ ] Set up monitoring alerts
- [ ] Configure backup for models
- [ ] Implement A/B testing
- [ ] Add model versioning
- [ ] Set up automated retraining pipeline
- [ ] Implement canary deployments

---

**For production use, always:**
- Test in staging first
- Set up proper monitoring
- Configure alerts
- Document runbooks
- Perform load testing

