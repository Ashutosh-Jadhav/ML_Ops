pipeline {
    agent any
    triggers {
        githubPush()
    }
    environment {
        DOCKER_IMAGE_NAME = 'ashutoshj/qna_service'
        GITHUB_REPO_URL = 'https://github.com/Ashutosh-Jadhav/ML_Ops.git'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'v2', url: "${GITHUB_REPO_URL}"
                }
            }
        }

        stage('Testing of Qna_Service') {
            steps {
                script {
                    sh 'pytest qna_service/qna_testing.py -v'
                }
            }
        }

        stage('Model Training') {
            steps {
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG')]) {
                    sh '''
                        echo "Using Minikube context:"
                        kubectl apply -f train_model_manifests/
                        
                        echo "Waiting for model training job to complete..."
                        kubectl wait --for=condition=complete job/train-model-job -n training-model-env --timeout=1800s
                        
                        # Check if any job failed
                        if kubectl get jobs -o jsonpath='{.items[*].status.failed}' | grep -q "1"; then
                            echo "Model training job failed!"
                            kubectl logs job/$(kubectl get jobs -o jsonpath='{.items[0].metadata.name}')
                            exit 1
                        fi
                        
                        echo "Model training completed successfully!"
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE_NAME}" , "./qna_service")
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script{
                    docker.withRegistry('' , 'DockerHubCred') {
                        sh 'docker push ashutoshj/qna_service'
                    }
                }
            }
        }

        stage('Push Model Image') {
            steps {
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG'),file(credentialsId: 'K8S_SECRET_FILE', variable: 'SECRET_YAML')]) {
                    sh '''
                        echo "Using Minikube context:"
                        kubectl delete job kaniko-build-job --ignore-not-found
                        kubectl apply -f kaniko-build-job.yaml
                        
                        echo "Waiting for kaniko build job to complete..."
                        kubectl wait --for=condition=complete job/kaniko-build-job -n training-model-env --timeout=1800s
                        
                        # Check if job failed
                        if kubectl get job kaniko-build-job -o jsonpath='{.status.failed}' | grep -q "1"; then
                            echo "Kaniko build job failed!"
                            kubectl logs job/kaniko-build-job
                            exit 1
                        fi
                        
                        echo "Model image push completed successfully!"
                    '''
                }
            }
        }
        
        stage('Load Model') {
            steps {
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG')]) {
                    sh '''
                        echo "Using Minikube context:"
                        kubectl delete job copy-model-job --ignore-not-found
                        kubectl apply -f job_extract_model.yaml
                        
                        echo "Waiting for model loading job to complete..."
                        kubectl wait --for=condition=complete job/copy-model-job -n training-env --timeout=900s
                        
                        # Check if job failed
                        if kubectl get job copy-model-job -o jsonpath='{.status.failed}' | grep -q "1"; then
                            echo "Model loading job failed!"
                            kubectl logs job/copy-model-job
                            exit 1
                        fi
                        
                        echo "Model loading completed successfully!"
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG')]) {
                    sh '''
                        echo "Using Minikube context:"
                        kubectl config get-contexts
                        kubectl apply -f model-inference-manifests/
                        
                        echo "Waiting for deployment to be ready..."
                        kubectl wait --for=condition=available --timeout=600s deployment --all -n training-env
                        
                        echo "Deployment completed successfully!"
                    '''
                }
            }
        }
    }

    post {
        success{
            mail to: 'ashutosh.j001@gmail.com',
            subject: "Application Deployment SUCCESS: Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: "The build was successful!"
        }
        failure {
            mail to: 'ashutosh.j001@gmail.com',
            subject: "Application Deployment FAILURE: Build ${env.JOB_NAME} #{env.BUILD_NUMBER}",
            body: "The build failed."
        }
        always {
            cleanWs()
        }
    }

}