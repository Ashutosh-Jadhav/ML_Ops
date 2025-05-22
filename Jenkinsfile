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
        stage('checkout') {
            steps {
                script {
                    git branch: 'main', url: "${GITHUB_REPO_URL}"
                }
            }
        }

        stage('test') {
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

        stage('Deploy to Minikube') {
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