pipeline {
    agent {
        kubernetes {
            yaml """
                apiVersion: v1
                kind: Pod
                metadata:
                  labels:
                    jenkins: jenkins-pod
                spec:
                  containers:
                  - name: docker
                    image: docker:latest
                    command:
                    - cat
                    tty: true
                  - name: kubectl
                    image: bitnami/kubectl:latest
                    command:
                    - cat
                    tty: true
            """
        }
    }

    environment {
        DOCKERHUB_CREDENTIALS = credentials('PrinceDockerhub')
        DOCKERHUB_REPO = 'princestanley/github-copilot'
        IMAGE_TAG = "latest"
        AWS_REGION = 'us-east-1'
        EKS_CLUSTER_NAME = 'uc-devops-eks-cluster'
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    container('docker') {
                      docker.build("${DOCKERHUB_REPO}:${IMAGE_TAG}")
                    }
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    container('docker') {
                      docker.withRegistry('https://registry.hub.docker.com', 'DOCKERHUB_CREDENTIALS') {
                          docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}").push()
                    }
                    }
                }
            }
        }

        stage('Update Kubeconfig') {
            steps {
                container('kubectl') {
                  withCredentials([file(credentialsId: 'kubeconfig-credentials', variable: 'KUBECONFIG')]) {
                      sh 'export KUBECONFIG=$KUBECONFIG'
                    }
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                container('kubectl') {
                   script {
                      sh """
                          kubectl apply -f ./app-deploy.yaml
                        """
                    }
                }
            }
        }
    }
    post {
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Deployment successful!'
        }
    }
}