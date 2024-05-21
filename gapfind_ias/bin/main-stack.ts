import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as python from "@aws-cdk/aws-lambda-python-alpha";
import { AwsEnvStackProps } from "../config/custom-types";
import {
  getCloudFormationID,
  getResourceName,
  getRootOfExternalProject,
} from "../config/utils";
import { CorsHttpMethod, HttpApi } from "aws-cdk-lib/aws-apigatewayv2";
import { HttpLambdaIntegration } from "aws-cdk-lib/aws-apigatewayv2-integrations";
import { HttpMethod } from "aws-cdk-lib/aws-events";
import { PYTHON_EXCLUDES } from "../config/excludeFiles";

export class MainStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: AwsEnvStackProps) {
    super(scope, id, props);

    // Lambda functions

    const codePath = getRootOfExternalProject("gapfind_core");
    const manualRegisterLambda = new python.PythonFunction(
      this,
      getCloudFormationID(id, "manual-register-lambda"),
      {
        entry: codePath,
        runtime: lambda.Runtime.PYTHON_3_10,
        index: "manual_register.py",
        handler: "handler",
        functionName: getResourceName(id, "manual-register-lambda"),
        bundling: {
          assetExcludes: PYTHON_EXCLUDES,
        },
      }
    );

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
      manualRegisterLambda
    );

    // Create a resource and method for the API
    httpApi.addRoutes({
      path: "/manual",
      methods: [HttpMethod.POST],
      integration: manualRegisterLambdaIntegration,
    });
  }
}
