
pipeline {
    agent any

    parameters {
        string(
            name: 'GITHUB_REPO',
            defaultValue: 'https://github.com/its-sourabh-01/Aws-Demo.git',
            description: 'GitHub repository URL'
        )

        string(
            name: 'BRANCH',
            defaultValue: 'main',
            description: 'GitHub branch'
        )

        string(
            name: 'SUB_NET',
            defaultValue: '',
            description: 'Existing AWS subnet ID'
        )
    }

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        STACK_NAME = 'independent-ec2-s3'
        TEMPLATE_FILE = 's3_template.yml'
    }

    stages {

        stage('Checkout GitHub') {
            steps {
                git branch: "${params.BRANCH}",
                    credentialsId: 'github-credentials', 
                    url: "${params.GITHUB_REPO}"
            }
        }

        stage('Verify Template') {
            steps {
                sh '''
                    ls -l
                    test -f "$TEMPLATE_FILE"
                '''
            }
        }

        stage('Check AWS Credentials') {
            steps {
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')])
                {
                    sh '''
                        aws sts get-caller-identity
                    '''
                }
            }
        }

        stage('Validate Template') {
            steps {
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')])
                {
                    sh '''
                        aws cloudformation validate-template \
                        --template-body file://$TEMPLATE_FILE \
                        --region $AWS_DEFAULT_REGION
                    '''
                }
            }
        }

        stage('Deploy CloudFormation') {
            steps {
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')])
                {
                    sh '''
                        if [ -z "$SUBNET_ID" ]; then
                            echo "Subnet ID is required"
                            exit 1
                        fi

                        aws cloudformation deploy \
                        --template-file "$TEMPLATE_FILE" \
                        --stack-name "$STACK_NAME" \
                        --region "$AWS_DEFAULT_REGION" \
                        --parameter-overrides \
                        SubnetId="$SUBNET_ID" \
                        InstanceType=t3.micro \
                        --no-fail-on-empty-changeset
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')])
                {
                    sh '''
                        aws cloudformation describe-stacks \
                        --stack-name "$STACK_NAME" \
                        --region "$AWS_DEFAULT_REGION" \
                        --query "Stacks[0].StackStatus" \
                        --output text
                    '''
                }
            }
        }
    }
}
