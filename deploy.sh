#
#!/usr/bin/python3.8 
#
# File: deploy.sh
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: Deploy docker image on ECR AWS service
# for the stryker's audio data capturing tool application. 
#
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag <name>:latest <acount-id>.dkr.ecr.us-east-1.amazonaws.com/<name>:latest

docker push <acount-id>.dkr.ecr.us-east-1.amazonaws.com/<name>r:latest