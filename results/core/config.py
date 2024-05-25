import os

from decouple import config


def config_as_str(key: str, **kwargs) -> str:
    return config(key, **kwargs)  # type: ignore


def config_as_bool(key: str, **kwargs) -> bool:
    return config(key, cast=bool, **kwargs)


def config_as_int(key: str, **kwargs) -> int:
    return config(key, cast=int, **kwargs)


class APPConfig:
    def __init__(self, load_secrets_from: str, env: str = "dev"):
        self.load_secrets_from = load_secrets_from
        self.env = env

        if self.env not in ["dev", "prod", "test"]:
            raise ValueError(
                f"Invalid environment: {self.env}, valid values: dev, prod and test"
            )

        self.aws_region = config_as_str("AWS_REGION", default="us-east-1")
        self.mock_repository = config_as_bool("MOCK_REPOSITORY", default=True)

        self._load_secrets()
        self._validate_settings()

    def _load_secrets(self):
        if self.load_secrets_from == "env":
            self._load_secrets_from_env()
        elif self.load_secrets_from == "ssm":
            self._load_secrets_from_ssm()
        else:
            raise ValueError(
                f"Invalid value for load_secrets_from: {self.load_secrets_from}, valid values: env and ssm"
            )

    def get_key_for_ssm(self, name: str):
        return f"/gapfind/{self.env}/{name}"

    def _load_secrets_from_ssm(self):
        import boto3

        ssm = boto3.client("ssm", region_name=self.aws_region)

        self.redis_url = ssm.get_parameter(
            Name=self.get_key_for_ssm("redis_url"), WithDecryption=True
        )["Parameter"]["Value"]

    def _load_secrets_from_env(self):
        self.redis_url = config_as_str("REDIS_URL", default="")

        self._set_aws_credentials()

    def _validate_settings(self):
        pass

    def _set_aws_credentials(self):
        aws_access_key_id = config_as_str("AWS_ACCESS_KEY_ID", default="")
        aws_secret_access_key = config_as_str("AWS_SECRET_ACCESS_KEY", default="")

        # decouple library does not set the env variables if available in a .env file
        # so we need to set them manually
        if aws_access_key_id != "":
            os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key_id
        if aws_secret_access_key != "":
            os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key


SERVICE_ENVIRONMENT = config_as_str("SERVICE_ENVIRONMENT", default="dev")
SECRETS_FROM = config_as_str("SECRETS_FROM", default="env")
APP_CONFIG = APPConfig(load_secrets_from=SECRETS_FROM, env=SERVICE_ENVIRONMENT)
