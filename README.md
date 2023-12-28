# stryker-campaign-backend

# Overview

Voice collection tool allows you to get the voice samples of user and store to cloud


# Note 

Appropriate environment variable need to be set in Dev/Prod app runner for AWS and JWT token.


# Flask 

Flask use to create Restful API Server for audio application.


## Installation

Install with pip:

```
$ pip install -r requirements.txt
```


## Flask Configuration

```
app = Flask(__name__ )
```


## Flask .env setup
1. To set environment variable for aws run following command to get security values for EC2 machine.  

```
aws sts assume-role --role-arn "arn:aws:iam::child_acc_no:role/role_name" --role-session-name "session_name"
```

2. Set values for AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN


 
## Run Flask
### Run flask for develop
```
$ flask run --reload
```
In flask, Default port is `5000`


### Run flask for production

# Assumption

- The machine is Ubuntu 18.04

## Prerequisites 

- docker >24.0.0
    - **Steps to install docker on your machine**

            sudo apt update

            sudo apt install apt-transport-https ca-certificates curl software-properties-common

            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

            sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"

            sudo apt update

            apt-cache policy docker-ce

            sudo apt install docker-ce

            sudo chmod 666 /var/run/docker.sock
            sudo chmod 777 ~/.docker/config.json
            

## Build command 
- sudo docker build -t stryker_backend:1 .

## Run command 
- sudo docker run -p 8080:8080 stryker_backend:1


## Cloud Config 

- aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
- **run.sh**
    - Run above  command from path ./stryker_backend It will run flask app in 8080 port            

