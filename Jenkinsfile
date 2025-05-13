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
                    image: docker:20.10-dind
                    securityContext:
                      privileged: true
                    volumeMounts:
                    - name: docker-graph-storage
                      mountPath: /var/lib/docker
                  - name: kubectl
                    image: lachlanevenson/k8s-kubectl:latest
                    command:
                    - /bin/sh
                    args:
                    - '-c'
                    - sleep infinity
                  volumes:
                  - name: docker-graph-storage
                    emptyDir: {}
            """
            defaultContainer 'docker'
        }
    }

    environment {
        DOCKERHUB_CREDENTIALS = 'PrinceDockerhub'
        DOCKERHUB_REPO = 'princestanley/github-copilot'
        IMAGE_TAG = "v${BUILD_NUMBER}"
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
                        docker.withRegistry('https://registry.hub.docker.com', "${DOCKERHUB_CREDENTIALS}") {
                          def customImage = docker.build("${DOCKERHUB_REPO}:${IMAGE_TAG}")
                          customImage.push()
                        }
                    }
                }
            }
        }

        /*stage('Push to DockerHub') {
            steps {
                script {
                    container('docker') {
                      docker.withRegistry('https://registry.hub.docker.com', ${DOCKERHUB_CREDENTIALS}) {
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
        }*/
        stage('Deploy to EKS') {
            steps {
                container('kubectl') {
                   script {
                        def deploymentFile = readFile('app-deploy.yaml')
                        def updatedDeploymentFile = deploymentFile.replaceAll(/image:\s.*$/, "image: ${DOCKERHUB_REPO}:${IMAGE_TAG}")
                        writeFile file: 'app-deploy.yaml', text: updatedDeploymentFile
                        sh 'kubectl apply -f app-deploy.yaml'
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