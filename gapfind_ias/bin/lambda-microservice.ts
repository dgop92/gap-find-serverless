import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as python from "@aws-cdk/aws-lambda-python-alpha";
import {
  getCloudFormationID,
  getResourceName,
  getRootOfExternalProject,
} from "../config/utils";
import { PYTHON_EXCLUDES } from "../config/excludeFiles";

export interface LambdaMicroserviceProps {
  functionName: string;
  projectName: string;
}

export class LambdaMicroservice extends Construct {
  public readonly lambdaFunc: python.PythonFunction;

  constructor(scope: Construct, id: string, props: LambdaMicroserviceProps) {
    super(scope, id);
    const { functionName, projectName } = props;

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
      }
    );

    this.lambdaFunc = pythonFunc;
  }
}
