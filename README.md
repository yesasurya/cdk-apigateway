# cdk-apigateway

### What is this?
You should know first that AWS has [CDK](https://aws.amazon.com/cdk/) service (Cloud Development Kit). It basically helps you provision resources on AWS using your favorites language.

Behind the scene, it will actually convert your code into CloudFormation template.

This CDK configuration will generate followings
1. An API Gateway which will route the request to an existing Lambda function
