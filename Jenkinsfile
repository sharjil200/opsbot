pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'opsbot'
        CONTAINER_NAME = 'opsbot-app'
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                // Pulls the latest code from your GitHub repository
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // Builds the updated Docker image using the Dockerfile
                sh "sudo docker build -t ${IMAGE_NAME} ."
            }
        }
        
        stage('Deploy Container') {
            steps {
                script {
                    // Stop and remove the old container safely (ignores error if it doesn't exist yet)
                    sh "sudo docker stop ${CONTAINER_NAME} || true"
                    sh "sudo docker rm ${CONTAINER_NAME} || true"
                    
                    // Run the new container on port 5000
                    sh "sudo docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                }
            }
        }
    }
    
    post {
        success {
            echo '🎉 OpsBot pipeline built and deployed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check the console logs for details.'
        }
    }
}
