export type GenericEnvvar = {
  SERVICE_ENVIRONMENT: string;
  SECRETS_FROM: string;
  MOCK_REPOSITORY: string;
};

export function getEnvironmentVariablesFromEnv(env: string): GenericEnvvar {
  if (env === "test") {
    return {
      SERVICE_ENVIRONMENT: "test",
      SECRETS_FROM: "ssm",
      MOCK_REPOSITORY: "True",
    };
  }

  if (env === "prod") {
    return {
      SERVICE_ENVIRONMENT: "prod",
      SECRETS_FROM: "ssm",
      MOCK_REPOSITORY: "False",
    };
  }

  if (env === "dev") {
    return {
      SERVICE_ENVIRONMENT: "dev",
      SECRETS_FROM: "ssm",
      MOCK_REPOSITORY: "False",
    };
  }

  throw new Error("Invalid environment");
}
