import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import { AwsEnvStackProps } from "../config/custom-types";
import { getCloudFormationID, getResourceName } from "../config/utils";
import { CorsHttpMethod, HttpApi } from "aws-cdk-lib/aws-apigatewayv2";
import { HttpLambdaIntegration } from "aws-cdk-lib/aws-apigatewayv2-integrations";
import { HttpMethod } from "aws-cdk-lib/aws-events";
import { LambdaMicroservice } from "./lambda-microservice";

export class MainStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: AwsEnvStackProps) {
    super(scope, id, props);

    // Lambda functions

    const manualRegisterLambda = new LambdaMicroservice(this, id, {
      projectName: "manual_register",
      functionName: "manual-register-lambda",
    });

    // Create an API Gateway

    const httpApi = new HttpApi(this, getCloudFormationID(id, "api-gateway"), {
      apiName: getResourceName(id, "api-gateway"),
      corsPreflight: {
        allowMethods: [
          CorsHttpMethod.GET,
          CorsHttpMethod.DELETE,
          CorsHttpMethod.PUT,
          CorsHttpMethod.POST,
        ],
        allowOrigins: ["*"],
      },
    });

    const manualRegisterLambdaIntegration = new HttpLambdaIntegration(
      "manual-register-lambda-integration",
      manualRegisterLambda.lambdaFunc
    );

    // Create a resource and method for the API
    httpApi.addRoutes({
      path: "/manual",
      methods: [HttpMethod.POST],
      integration: manualRegisterLambdaIntegration,
    });
  }
}
