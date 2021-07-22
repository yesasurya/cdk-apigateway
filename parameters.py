from aws_cdk import core as cdk


DEFAULT_STACK_NAME_APIGATEWAY = 'cdk-stack-apigateway'


class StackParameters():
    def __init__(self, stack_name, param_keys):
        self.stack_name = stack_name
        self.param_keys = param_keys

    def build_parameter(self, cdk_stack, key):
        return cdk.CfnParameter(cdk_stack, id=key)


class StackApiGatewayParameters(StackParameters):
    def __init__(self, stack_name=DEFAULT_STACK_NAME_APIGATEWAY):        
        ## You can add parameter key for the stack here.
        ## Make sure to add the parameter key you added in the parameter keys list
        self.PARAM_KEY_LAMBDA_ARN = 'lambdaArn'
        self.PARAM_KEY_API_NAME = 'apiName'
        self.PARAM_KEY_API_KEY = 'apiKey'

        PARAM_KEYS = [
            self.PARAM_KEY_LAMBDA_ARN,
            self.PARAM_KEY_API_NAME,
            self.PARAM_KEY_API_KEY
        ]

        super().__init__(stack_name, PARAM_KEYS)
