import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { AwsEnvStackProps } from "../config/custom-types";
import {
  getCloudFormationID,
  getResourceName,
  getRootOfExternalProject,
} from "../config/utils";
import { CorsHttpMethod, HttpApi } from "aws-cdk-lib/aws-apigatewayv2";
import { HttpLambdaIntegration } from "aws-cdk-lib/aws-apigatewayv2-integrations";
import { HttpMethod } from "aws-cdk-lib/aws-events";

export class MainStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: AwsEnvStackProps) {
    super(scope, id, props);

    const codePath = getRootOfExternalProject("gapfind_core");

    // a simple lambda function
    const helloLambda = new lambda.Function(
      this,
      getCloudFormationID(id, "my-hello-lambda"),
      {
        runtime: lambda.Runtime.PYTHON_3_10,
        handler: "hello_hanlder.handler",
        code: lambda.Code.fromAsset(codePath),
        memorySize: 128,
        functionName: getResourceName(id, "my-hello-lambda"),
      }
    );

    // Create an API Gateway
    const httpApi = new HttpApi(this, "MyApi", {
      apiName: "My API",
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

    const templateLambdaIntegration = new HttpLambdaIntegration(
      "TemplateIntegration",
      helloLambda
    );

    // Create a resource and method for the API
    httpApi.addRoutes({
      path: "/hello",
      methods: [HttpMethod.GET],
      integration: templateLambdaIntegration,
    });
  }
}
