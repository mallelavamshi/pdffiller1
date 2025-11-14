pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'pdf-filler-api'
        DOCKER_TAG = "${BUILD_NUMBER}"
        APP_NAME = 'pdf-filler-api'
        DEPLOY_SERVER = 'localhost'
        DEPLOY_USER = 'ubuntu'
        APP_PORT = '8003'
        WORKSPACE_DIR = "${WORKSPACE}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Prepare Directories') {
            steps {
                echo 'Preparing directories...'
                script {
                    sh '''
                        # Create directories if they don't exist
                        mkdir -p templates
                        mkdir -p outputs
                        mkdir -p uploads

                        # Check if template exists
                        if [ ! -f "templates/Letter_of_Representation_Fillable.pdf" ]; then
                            echo "WARNING: PDF template not found in templates directory"
                            echo "Please copy Letter_of_Representation_Fillable.pdf to templates/"
                        else
                            echo "PDF template found"
                        fi

                        ls -la templates/ || true
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh '''
                        docker build -t pdf-filler-api:${BUILD_NUMBER} .
                        docker tag pdf-filler-api:${BUILD_NUMBER} pdf-filler-api:latest
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                script {
                    sh '''
                        docker run --rm pdf-filler-api:${BUILD_NUMBER} python -c "import main; print('Import successful')"
                    '''
                }
            }
        }

        stage('Stop Old Container') {
            steps {
                echo 'Stopping old container...'
                script {
                    sh '''
                        docker stop pdf-filler-api || true
                        docker rm pdf-filler-api || true
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying new container...'
                script {
                    sh '''
                        # Get absolute path of workspace
                        WORKSPACE_PATH=$(pwd)

                        # Run new container
                        docker run -d \
                            --name pdf-filler-api \
                            -p 8003:8003 \
                            -v ${WORKSPACE_PATH}/templates:/app/templates \
                            -v ${WORKSPACE_PATH}/outputs:/app/outputs \
                            -e PORT=8003 \
                            --restart unless-stopped \
                            pdf-filler-api:latest

                        echo "Container started successfully"
                        docker ps | grep pdf-filler-api
                    '''
                }
            }
        }

        stage('Health Check') {
            steps {
                echo 'Performing health check...'
                script {
                    sleep(time: 10, unit: 'SECONDS')
                    sh '''
                        echo "Testing health endpoint..."
                        curl -f http://localhost:8003/health || exit 1
                        echo "Health check passed!"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
            echo 'Application running at: http://localhost:8003'
            echo 'API Documentation: http://localhost:8003/docs'
        }
        failure {
            echo 'Deployment failed!'
            sh 'docker logs pdf-filler-api 2>&1 | tail -50 || echo "Container not found"'
        }
        always {
            echo 'Pipeline completed.'
        }
    }
}
