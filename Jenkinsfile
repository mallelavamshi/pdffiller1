pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'pdf-filler-api'
        DOCKER_TAG = "${BUILD_NUMBER}"
        APP_NAME = 'pdf-filler-api'
        DEPLOY_SERVER = 'localhost'  // Update if deploying to remote server
        DEPLOY_USER = 'ubuntu'
        APP_PORT = '8003'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                script {
                    sh """
                        docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} python -c "import main; print('Import successful')"
                    """
                }
            }
        }

        stage('Stop Old Container') {
            steps {
                echo 'Stopping old container...'
                script {
                    sh """
                        docker stop ${APP_NAME} || true
                        docker rm ${APP_NAME} || true
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying new container...'
                script {
                    sh """
                        # Run new container
                        docker run -d \
                            --name ${APP_NAME} \
                            -p ${APP_PORT}:${APP_PORT} \
                            -v \$(pwd)/templates:/app/templates \
                            -v \$(pwd)/outputs:/app/outputs \
                            -e PORT=${APP_PORT} \
                            --restart unless-stopped \
                            ${DOCKER_IMAGE}:latest

                        # Clean up old images
                        docker image prune -f
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                echo 'Performing health check...'
                script {
                    sleep(time: 10, unit: 'SECONDS')
                    sh """
                        curl -f http://localhost:${APP_PORT}/health || exit 1
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
            echo "Application running at: http://localhost:${APP_PORT}"
            echo "API Documentation: http://localhost:${APP_PORT}/docs"
        }
        failure {
            echo 'Deployment failed!'
            sh 'docker logs ${APP_NAME} || true'
        }
        always {
            echo 'Pipeline completed.'
        }
    }
}
