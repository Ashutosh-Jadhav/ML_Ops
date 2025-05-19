# DevOps Project Report: QnA Application Deployment with Kubernetes and ELK Stack

## 1. Introduction to DevOps

DevOps is a set of practices that combines software development (Dev) and IT operations (Ops) with the goal of shortening the development lifecycle and providing continuous delivery of high-quality software. It focuses on breaking down silos between development and operations teams, promoting collaboration, automation, and continuous improvement.

### Why DevOps?

- **Faster Time to Market**: Automates development, testing, and deployment processes
- **Improved Collaboration**: Breaks down barriers between development and operations
- **Enhanced Quality and Reliability**: Through automated testing and continuous integration
- **Increased Efficiency**: Automation reduces manual tasks and human error
- **Better Scalability**: Infrastructure as code and containerization enable flexible scaling
- **Continuous Improvement**: Regular feedback loops and monitoring

## 2. Project Overview

This project implements a complete DevOps pipeline for a Question-Answer (QnA) application built with FastAPI. The application uses an extractive QA model loaded from Hugging Face, with PostgreSQL for data storage and Redis for caching. The entire stack is deployed on Kubernetes with monitoring via the ELK (Elasticsearch, Logstash, Kibana) Stack.

## 3. Technologies Used

### Version Control: Git and GitHub
- Enables collaborative development
- Tracks code changes and maintains version history
- Facilitates code reviews through pull requests

### CI/CD Automation
- **Jenkins**: Orchestrates the CI/CD pipeline
- **GitHub Hook Trigger for GITScm Polling**: Initiates builds on code commits
- **Jenkins Pipelines**: Defines build, test, and deployment steps as code

### Containerization
- **Docker**: Creates consistent, portable application environments
- **Docker Compose**: Defines multi-container applications locally before K8s deployment

### Configuration Management
- **Ansible Playbooks**: Automates infrastructure provisioning and configuration
- Used for setting up Minikube and the ELK Stack

### Orchestration and Scaling
- **Kubernetes (K8s)**: Manages containerized applications at scale
- **Horizontal Pod Autoscaler (HPA)**: Automatically scales pods based on CPU/memory usage

### Monitoring and Logging
- **ELK Stack**:
  - **Elasticsearch**: Stores and indexes logs and metrics
  - **Logstash**: Processes and transforms logs (implied in the setup)
  - **Kibana**: Visualizes data with dashboards
- **Metricbeat**: Collects system and service metrics

### Database and Caching
- **PostgreSQL**: Primary database for QnA data storage
- **Redis**: In-memory data structure store used for caching

## 4. Architecture & CI/CD Flow

### Application Architecture
1. **Frontend**: Web interface for users to submit questions
2. **FastAPI Backend**: Processes requests and interfaces with the QA model
3. **Extractive QA Model**: Loaded from Hugging Face for answering questions
4. **PostgreSQL**: Stores questions, answers, and feedback
5. **Redis**: Caches frequently accessed data
6. **Kubernetes**: Orchestrates all components
7. **ELK Stack**: Monitors and logs system performance

### CI/CD Pipeline Flow
1. **Code Changes**: Developers push code to GitHub repository
2. **Automated Trigger**: GitHub webhook triggers Jenkins build
3. **Build Phase**: 
   - Code checkout
   - Dependencies installation
   - Unit tests execution
4. **Containerization**:
   - Docker image build
   - Image tagging with build number
   - Push to container registry
5. **Deployment**:
   - Kubernetes manifests applied
   - Rolling updates for zero-downtime deployment
6. **Monitoring**:
   - Deployment verification
   - Performance metrics collection via Metricbeat
   - Logs aggregation in Elasticsearch

## 5. Project Components Analysis

### FastAPI Application
- **Structure**: Modular design with API versioning (v1)
- **Features**: Question answering, feedback collection, view tracking
- **Endpoints**:
  - `/api/v1/qna/ask`: Submit questions
  - `/api/v1/qna/feedback/{qa_id}`: Provide feedback on answers
  - `/api/v1/qna/qa/{qa_id}`: Retrieve specific Q&A pairs
  - `/api/v1/qna/popular-questions`: List most viewed questions
  - `/health`: Health check endpoint

### Database Models
- **QuestionAnswer**: Stores questions, answers, and view counts
- **Feedback**: Tracks user ratings on answers

### Kubernetes Deployment
- **Namespaces**:
  - `default`: Application components (FastAPI, PostgreSQL, Redis)
  - `elastic-system`: ELK Stack and monitoring tools
- **Resources**:
  - **ConfigMaps**: Non-sensitive configuration
  - **Secrets**: Sensitive data and connection strings
  - **Deployments**: FastAPI application, Redis
  - **StatefulSets**: PostgreSQL (for persistent storage)
  - **Services**: Internal and external access points
  - **HPA**: Automatic scaling based on resource usage

## 6. Setup and Deployment Instructions

### Prerequisites
- Git
- Docker and Docker Compose
- Ansible
- kubectl
- Helm

### Step 1: Clone the Repository
```bash
git clone [repository-url]
cd [repository-directory]
```

### Step 2: Set Up Minikube and ELK Stack
```bash
ansible-playbook elastic_stack_setup.yaml
```
This playbook:
- Starts Minikube if not running
- Creates the `elastic-system` namespace
- Installs Elasticsearch, Kibana, and Metricbeat via Helm
- Sets up port forwarding

### Step 3: Deploy Core Infrastructure
```bash
# Apply secrets (encoded values provided in k8s-secrets.yaml)
kubectl apply -f k8s-secrets.yaml

# Deploy PostgreSQL StatefulSet
kubectl apply -f k8s-postgres.yaml

# Deploy Redis
kubectl apply -f k8s-redis.yaml

# Apply ConfigMap
kubectl apply -f k8s-configmap.yaml
```

### Step 4: Deploy FastAPI Application
```bash
# Apply the FastAPI deployment
kubectl apply -f k8s-fastapi.yaml

# Set up Horizontal Pod Autoscaler
kubectl apply -f k8s-fastapi-hpa.yaml

# Track deployment status
./deployment-track.sh fastapi-app
```

### Step 5: Verify Deployment
```bash
# Check pods status
./get_pods.sh

# Monitor HPA
./hpa-usage.sh fastapi-app-hpa
```

### Step 6: Access Services
```bash
# FastAPI service
minikube service fastapi-service --url

# Kibana dashboard
./start-kibana.sh
```

### Step 7: Testing Load Scaling (Optional)
```bash
# Deploy load generator
kubectl apply -f load-generator-deployment.yaml
```

## 7. Key Features and Advantages

### Containerization Benefits
- **Environment Consistency**: Same environment across development, testing, and production
- **Isolation**: Application dependencies encapsulated within containers
- **Portability**: Runs the same way on any platform supporting Docker
- **Resource Efficiency**: Lightweight compared to traditional VMs

### Kubernetes Advantages
- **Declarative Configuration**: Infrastructure as code
- **Self-Healing**: Automatic replacement of failed containers
- **Load Balancing**: Traffic distribution across pods
- **Service Discovery**: Automatic detection of new services
- **Horizontal Scaling**: Automatic scaling via HPA based on metrics
- **Rolling Updates**: Zero-downtime deployments
- **Resource Allocation**: CPU and memory limits for optimal performance

### ELK Stack Monitoring Benefits
- **Centralized Logging**: All logs in one searchable location
- **Real-Time Monitoring**: Live performance tracking
- **Visualization**: Custom dashboards for metrics
- **Anomaly Detection**: Identify issues before they impact users
- **Performance Analysis**: Tracking response times and resource usage

### Ansible Automation Benefits
- **Reproducible Infrastructure**: Consistent environment setup
- **Idempotent Operations**: Safe to run multiple times
- **Reduced Manual Work**: Automated Minikube and ELK setup
- **Simplified Onboarding**: New team members can set up environment quickly

### HPA (Horizontal Pod Autoscaler) Benefits
- **Dynamic Scaling**: Automatically adjusts pod count based on CPU/memory usage
- **Cost Efficiency**: Only uses necessary resources
- **Improved Reliability**: Handles traffic spikes gracefully
- **Configuration Simplicity**: Easily tunable min/max replicas and target utilization

## 8. PostgreSQL and Redis Implementation

### PostgreSQL
- **Implementation**: Deployed as a StatefulSet for persistent storage
- **Data**: Stores QnA pairs, feedback, and usage metrics
- **Schema**: Defined using SQLAlchemy models
- **Connection**: Managed via environment variables from Kubernetes secrets
- **Advantages**:
  - ACID compliance for data integrity
  - Rich querying capabilities for analytics
  - Persistent storage across pod restarts

### Redis
- **Implementation**: Deployed as a Kubernetes Deployment
- **Usage**: Caching layer for frequently accessed data
- **Configuration**: Connected via environment variables
- **Advantages**:
  - In-memory performance for faster responses
  - Reduced database load
  - Support for various data structures
  - Option for persistent storage if needed

## 9. Conclusion

This DevOps project successfully implements a complete pipeline for deploying and managing a FastAPI-based QnA application on Kubernetes. The architecture demonstrates modern DevOps practices including infrastructure as code, containerization, orchestration, automated deployment, and comprehensive monitoring.

Key achievements include:
- Fully automated deployment process
- Scalable architecture with auto-scaling capabilities
- Comprehensive monitoring with the ELK Stack
- Persistent storage for database and logs
- Load testing capabilities

The project serves as an excellent template for deploying similar applications with a focus on reliability, scalability, and observability.
