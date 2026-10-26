
pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        
    }

    stages {
        stage('Check AWS Identity') {
            steps {
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                sh 'aws sts get-caller-identity'
              }
                
            }
        }

        stage('Create File') {
            steps {
                sh '''
                    mkdir -p output
                    echo "Hello from Jenkins" > output/index.txt
                    date -u >> output/index.txt
                '''
            }
        }

        stage('Upload to S3') {
            steps {
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
             sh "aws s3 cp output/index.txt s3://qa-demo26/jenkins/index.txt"
                   
                 }
            }
        }

        stage('Verify Upload') {
            steps {
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                sh '''
                    aws s3 ls \
                    s3://qa-demo26/jenkins/
                    '''
                    }
                
            }
        }
    }

    post{
        success {
            echo 'Pipeline completed successfully!' 
        }
        failure {
            echo 'Pipeline failed. Please check the logs for details.'
        }
        exception {
            echo 'An exception occurred during the pipeline execution.'
        }
    } 
}
