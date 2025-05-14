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
        IMAGE_TAG = "latest"
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

        stage('Deploy to EKS') {
            steps {
                container('kubectl') {
                   script {
                      sh """
                        kubectl apply -f app-deploy.yaml
                        kubectl expose deploy app-deploy --port=80 --target-port=8080 -n default
                        kubectl create ingress app-deploy --rule="app-deploy.exlservice.com/health=app-deploy:80" --class=nginx -n default
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