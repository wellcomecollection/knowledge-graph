import json
import base64

import boto3
from botocore.exceptions import ClientError

from .logging import get_logger

log = get_logger(__name__)


def get_secrets(secret_name):
    session = boto3.session.Session(
        profile_name="platform-dev"
    )
    client = session.client(
        service_name="secretsmanager",
        region_name="eu-west-1"
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

    except ClientError as e:
        log.error(e)
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise e

    else:
        if "SecretString" in get_secret_value_response:
            secrets = get_secret_value_response["SecretString"]
        else:
            secrets = base64.b64decode(
                get_secret_value_response["SecretBinary"])

        return json.loads(secrets)
