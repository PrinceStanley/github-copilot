pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('PrinceDockerhub') // Replace with your Jenkins credentials ID
        DOCKER_IMAGE = 'princestanley/github-copilot' // Replace with your DockerHub username and image name
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig-credentials') // Replace with your Jenkins credentials ID for kubeconfig
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                script {
                    sh '''
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                    docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                        sh '''
                        kubectl apply -f app-deploy.yaml
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}