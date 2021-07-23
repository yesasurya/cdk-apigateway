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

        ## Create REST API
        rest_api = cdk_apigateway.LambdaRestApi(self,
            id=generate_unique_id(),
            handler=lambda_function,
            rest_api_name=api_name,
            proxy=False,
            deploy_options=cdk_apigateway.StageOptions(
                stage_name="v1"
            )
        )

        ## As the value of 'proxy' is False when creating the REST API, we need to create these by our own:
        ## 1. Resource
        ## 2. Method
        resource_event = rest_api.root.add_resource(
            path_part='events',
            default_method_options=cdk_apigateway.MethodOptions(
                api_key_required=True
            )
        )
        resource_event_post_method = resource_event.add_method(
            http_method='POST'
        )

        ## Add resource-based policy in Lambda for allowing invocation by resource_event_post_method
        cdk_lambda.CfnPermission(self,
            id=generate_unique_id(),
            action="lambda:InvokeFunction",
            function_name=lambda_function.function_name,
            principal="apigateway.amazonaws.com",
            source_arn=resource_event_post_method.method_arn
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
