#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { loadEnvironmentVariables } from "../config/app-env-vars";
import { getStackName } from "../config/utils";
import { MainStack } from "./main-stack";

const app = new cdk.App();

function getConfig() {
  let envName = app.node.tryGetContext("config") as string;
  if (!envName) {
    throw new Error(
      "Context variable missing on CDK command. Pass in as `-c config=XXX`"
    );
  }

  const buildConfig = loadEnvironmentVariables(envName);
  return buildConfig;
}

const config = getConfig();

const mainStackName = getStackName(config.appName, "main", config.env);

const mainStack = new MainStack(app, mainStackName, {
  env: {
    region: config.region,
    account: config.accountId,
  },
  config: config,
});
cdk.Tags.of(mainStack).add("project:name", config.appName);
cdk.Tags.of(mainStack).add("project:env", config.env);
cdk.Tags.of(mainStack).add("project:stack", "main");
