
pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        AMI_ID = 'ami-0754c17a9e90ed320'
        SUBNET_ID = 'subnet-0e06fbeb9bc9c562f'
        SECURITY_GROUP_ID = 'sg-0320c65626ad85de1'
        KEY_NAME = 'new-key'
    }

    stages {
        stage('Verify AWS') {
            steps {
                withCredentials([
                    aws(
                        credentialsId: 'aws-2',
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh 'aws sts get-caller-identity'
                }
            }
        }

        stage('Launch EC2') {
            steps {
                withCredentials([
                    aws(
                        credentialsId: 'aws-2',
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        set -eu

                        aws ec2 run-instances \
                          --image-id "$AMI_ID" \
                          --instance-type t3.micro \
                          --subnet-id "$SUBNET_ID" \
                          --security-group-ids "$SECURITY_GROUP_ID" \
                          --key-name "$KEY_NAME" \
                          --count 1 \
                          --tag-specifications \
                          'ResourceType=instance,Tags=[{Key=Name,Value=Jenkins-EC2-Lab}]' \
                          --query 'Instances[0].InstanceId' \
                          --output text
                    '''
                }
            }
        }

        stage('Verify EC2') {
            steps {
                withCredentials([
                    aws(
                        credentialsId: 'aws-2',
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        aws ec2 describe-instances \
                          --filters "Name=tag:Name,Values=Jenkins-EC2-Lab" \
                          --query 'Reservations[].Instances[].[InstanceId,State.Name,InstanceType]' \
                          --output table
                    '''
                }
            }
        }
    }

    post{
        success {
            echo 'Pipeline completed successfully!' 
            emailext (
             body: '"Build succesfull Check logs: ${env.BUILD_URL}"', 
             subject: 'Build succesfull: ${env.JOB_NAME}',
            to: 'sourabhpatil00007@gmail.com'
       ) }
        failure {
            echo 'Pipeline failed. Please check the logs for details.'
        }
        always {
            cleanWs()
            
        }
    } 
}
