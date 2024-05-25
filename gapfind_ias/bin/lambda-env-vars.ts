export type GenericEnvvar = {
  SERVICE_ENVIRONMENT: string;
  SECRETS_FROM: string;
};

export function getEnvironmentVariablesFromEnv(env: string): GenericEnvvar {
  if (env === "test") {
    return {
      SERVICE_ENVIRONMENT: "test",
      SECRETS_FROM: "ssm",
    };
  }

  if (env === "prod") {
    return {
      SERVICE_ENVIRONMENT: "prod",
      SECRETS_FROM: "ssm",
    };
  }

  if (env === "dev") {
    return {
      SERVICE_ENVIRONMENT: "dev",
      SECRETS_FROM: "ssm",
    };
  }

  throw new Error("Invalid environment");
}
