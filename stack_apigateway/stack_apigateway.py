from aws_cdk import (
    core as cdk,
    aws_lambda as cdk_lambda,
    aws_apigateway as cdk_apigateway
)
from parameters import StackApiGatewayParameters
from utils import generate_unique_id


class StackApiGateway(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ## Parse the parameters
        stack_apigateway_parameters = StackApiGatewayParameters()
        lambda_arn = stack_apigateway_parameters.build_parameter(self,
            stack_apigateway_parameters.PARAM_KEY_LAMBDA_ARN
        ).value_as_string
        api_name = stack_apigateway_parameters.build_parameter(self,
            stack_apigateway_parameters.PARAM_KEY_API_NAME
        ).value_as_string
        api_key = stack_apigateway_parameters.build_parameter(self,
            stack_apigateway_parameters.PARAM_KEY_API_KEY
        ).value_as_string

        ## Get existing Lambda function by its ARN
        lambda_function = cdk_lambda.Function.from_function_arn(self,
            id=generate_unique_id(),
            function_arn=lambda_arn
        )

        ## Require API Key to connect to REST API
        rest_api_method_options = cdk_apigateway.MethodOptions(
            api_key_required=True
        )

        ## Create REST API using Lambda Proxy Integration
        rest_api = cdk_apigateway.LambdaRestApi(self,
            id=generate_unique_id(),
            handler=lambda_function,
            rest_api_name=api_name,
            default_method_options=rest_api_method_options
        )

        ## Create Usage Plan for the REST API
        rest_api_usage_plan = cdk_apigateway.UsagePlanPerApiStage(
            api=rest_api,
            stage=rest_api.deployment_stage
        )

        ## Create API Key
        cdk_api_key = cdk_apigateway.ApiKey(self,
            id=generate_unique_id(),
            value=api_key
        )

        ## Create Usage Plan
        cdk_apigateway.UsagePlan(self,
            id=generate_unique_id(),
            api_key=cdk_api_key,
            api_stages=[rest_api_usage_plan]
        )

        ## Add resource-based policy in Lambda for allowing invocation by REST API
        cdk_lambda.CfnPermission(self,
            id=generate_unique_id(),
            action="lambda:InvokeFunction",
            function_name=lambda_function.function_name,
            principal="apigateway.amazonaws.com",
            source_arn=rest_api.methods[0].method_arn
        )
