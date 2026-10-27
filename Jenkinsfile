pipeline {
    agent any
    
    environment {
        OPSBOT_HOST = 'ubuntu@13.127.67.172'
        CREDENTIALS_ID = 'opsbot-server-ssh'
        IMAGE_NAME = 'opsbot'
        CONTAINER_NAME = 'opsbot-app'
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Transfer Code to OpsBot Server') {
            steps {
                sshagent(credentials: [env.CREDENTIALS_ID]) {
                    // Create the workspace directory first, then scp files securely
                    sh "ssh -o StrictHostKeyChecking=no ${env.OPSBOT_HOST} 'mkdir -p ~/opsbot-workspace'"
                    sh "scp -o StrictHostKeyChecking=no -r . ${env.OPSBOT_HOST}:~/opsbot-workspace"
                }
            }
        }
        
        stage('Deploy on OpsBot Server') {
            steps {
                sshagent(credentials: [env.CREDENTIALS_ID]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${env.OPSBOT_HOST} << 'EOF'
                            cd ~/opsbot-workspace
                            /usr/bin/docker build -t ${IMAGE_NAME} .
                            /usr/bin/docker stop ${CONTAINER_NAME} || true
                            /usr/bin/docker rm ${CONTAINER_NAME} || true
                            /usr/bin/docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}
                        EOF
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo '🎉 OpsBot successfully deployed to the remote OpsBot server!'
        }
        failure {
            echo '❌ Remote deployment failed. Check logs.'
        }
    }
}
