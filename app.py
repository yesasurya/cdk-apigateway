#####################
## README.short.md ##
#####################
## Below is a short documentation which may help you to run this program.

## Before running this program, please do the followings:
## 1. Configure your AWS credential using aws-cli. You can execute:
##     aws configure
## 2. Install all the requirements needed. You can execute:
##     pip3 install -r requirements.txt
## 3. Lambda accepts several ways of loading the code, e.g. from S3.
##    Fortunately, CDK offers you a feature where you can put your code in your local computer to be loaded into Lambda.
##    How does this work?
##    CDK will upload your code into an auto-generated S3 bucket and make a reference to that file, AUTOMATICALLY.
##    You just need to execute:
##     cdk bootstrap aws://unknown-account/unknown-region

## This app.py file is the main program, one that will run at the first time.
## For generating a CloudFormation template of all the stacks, you can execute:
##     cdk synth --all
## For deploying all the stacks, you can execute:
##     cdk deploy --all
## For destroying all the stacks, you can execute:
##     cdk destroy --all


from aws_cdk import core
from stack_apigateway.stack_apigateway import StackApiGateway
from parameters import DEFAULT_STACK_NAME_APIGATEWAY


if __name__ == '__main__':
    app = core.App()

    stack_apigateway = StackApiGateway(app, DEFAULT_STACK_NAME_APIGATEWAY)
    app.synth()
