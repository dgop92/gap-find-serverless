import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import { AwsEnvStackProps } from "../config/custom-types";
import { getCloudFormationID, getResourceName } from "../config/utils";
import { HttpApi } from "aws-cdk-lib/aws-apigatewayv2";
import { HttpLambdaIntegration } from "aws-cdk-lib/aws-apigatewayv2-integrations";
import { HttpMethod } from "aws-cdk-lib/aws-events";
import { LambdaMicroservice } from "./lambda-microservice";
import { getEnvironmentVariablesFromEnv } from "./lambda-env-vars";

export class MainStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: AwsEnvStackProps) {
    super(scope, id, props);

    // Lambda functions

    const envVars = getEnvironmentVariablesFromEnv(props.config.env);

    const manualRegisterLambda = new LambdaMicroservice(
      this,
      getCloudFormationID(id, "manual-service"),
      {
        projectName: "manual_register",
        functionName: "manual-register-lambda",
        secrets: [
          {
            id: "manual-register-redis-url-param",
            paramName: `/${props.config.appName}/${props.config.env}/redis_url`,
          },
        ],
        envVars,
      }
    );
    const resultsLambda = new LambdaMicroservice(
      this,
      getCloudFormationID(id, "results-service"),
      {
        projectName: "results",
        functionName: "results-lambda",
        secrets: [
          {
            id: "results-register-redis-url-param",
            paramName: `/${props.config.appName}/${props.config.env}/redis_url`,
          },
        ],
        envVars,
      }
    );
    const analyzeLambda = new LambdaMicroservice(
      this,
      getCloudFormationID(id, "analyze-service"),
      {
        projectName: "analyze",
        functionName: "analyze-lambda",
        secrets: [
          {
            id: "analyze-register-redis-url-param",
            paramName: `/${props.config.appName}/${props.config.env}/redis_url`,
          },
        ],
        envVars,
      }
    );

    // Create an API Gateway

    const httpApi = new HttpApi(this, getCloudFormationID(id, "api-gateway"), {
      apiName: getResourceName(id, "api-gateway"),
    });

    // Create integrations

    const manualRegisterLambdaIntegration = new HttpLambdaIntegration(
      "manual-register-lambda-integration",
      manualRegisterLambda.lambdaFunc
    );
    const resultsLambdaIntegration = new HttpLambdaIntegration(
      "results-lambda-integration",
      resultsLambda.lambdaFunc
    );
    const analyzeLambdaIntegration = new HttpLambdaIntegration(
      "analyze-lambda-integration",
      analyzeLambda.lambdaFunc
    );

    // Add routes

    httpApi.addRoutes({
      path: "/manual",
      methods: [HttpMethod.POST],
      integration: manualRegisterLambdaIntegration,
    });
    httpApi.addRoutes({
      path: "/results",
      methods: [HttpMethod.POST],
      integration: resultsLambdaIntegration,
    });
    httpApi.addRoutes({
      path: "/analyze",
      methods: [HttpMethod.POST],
      integration: analyzeLambdaIntegration,
    });
  }
}
