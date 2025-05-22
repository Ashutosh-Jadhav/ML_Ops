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
                    git branch: 'main', url: "${GITHUB_REPO_URL}"
                }
            }
        }

        stage('Train the Model') {
            steps {
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG')]) {
                    sh '''
                        echo "Using Minikube context:"
                        kubectl apply -f $SECRET_FILE
                        kubectl apply -f train_model_manifests/
                    '''
                }
            }
        }

        stage('Test Qna Service') {
            steps {
                script {
                    sh 'pytest qna_service/qna_testing.py -v'
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
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG'),file(credentialsId: 'K8S_SECRET_FILE', variable: 'SECRET_FILE')]) {
                    sh '''
                        echo "Using Minikube context:"
                        kubectl apply -f $SECRET_FILE
                        kubectl apply -f kaniko-build-job.yaml
                    '''
                }

            }
        }

        stage('Deploy Model to Minikube') {
            steps {
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG')]) {
                    sh '''
                        echo "Using Minikube context:"
                        kubectl apply -f job_extract_model.yaml
                    '''
                }
            }
        }

        stage('Deploy QnaService to Minikube') {
            steps {
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG')]) {
                    sh '''
                        echo "Using Minikube context:"
                        kubectl delete job copy-model-job --ignore-not-found
                        kubectl config get-contexts
                        kubectl apply -f model-inference-manifests/
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