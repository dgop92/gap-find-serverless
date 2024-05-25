import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as python from "@aws-cdk/aws-lambda-python-alpha";
import {
  getCloudFormationID,
  getResourceName,
  getRootOfExternalProject,
} from "../config/utils";
import { PYTHON_EXCLUDES } from "../config/excludeFiles";
import { StringParameter } from "aws-cdk-lib/aws-ssm";
import { Duration } from "aws-cdk-lib";

export interface LambdaSecret {
  id: string;
  paramName: string;
}

export interface LambdaMicroserviceProps {
  functionName: string;
  projectName: string;
  envVars?: { [key: string]: string };
  secrets?: LambdaSecret[];
}

export class LambdaMicroservice extends Construct {
  public readonly lambdaFunc: python.PythonFunction;

  constructor(scope: Construct, id: string, props: LambdaMicroserviceProps) {
    super(scope, id);
    const { functionName, projectName, secrets } = props;

    const codePath = getRootOfExternalProject(projectName);
    const pythonFunc = new python.PythonFunction(
      this,
      getCloudFormationID(id, functionName),
      {
        entry: codePath,
        runtime: lambda.Runtime.PYTHON_3_10,
        index: "index.py",
        handler: "handler",
        functionName: getResourceName(id, functionName),
        bundling: {
          assetExcludes: PYTHON_EXCLUDES,
        },
        environment: props.envVars,
        timeout: Duration.seconds(20),
      }
    );

    if (secrets) {
      secrets.forEach((secret) => {
        const param = StringParameter.fromSecureStringParameterAttributes(
          this,
          secret.id,
          { parameterName: secret.paramName }
        );
        param.grantRead(pythonFunc);
      });
    }

    this.lambdaFunc = pythonFunc;
  }
}
