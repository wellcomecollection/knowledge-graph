from time import sleep

from httpx import Client, TimeoutException
from structlog import get_logger

log = get_logger()

http_client = Client(timeout=30)


def fetch_json(url, params=None):
    for i in range(0, 5):
        try:
            response = http_client.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(
                    f"{response.status_code} error when calling {url}"
                )
        except (TimeoutException) as e:
            log.exception(
                f"Timed out when calling {url} with params {params}", error=e
            )
            sleep(2 ** i)
        except Exception as e:
            log.exception(
                f"Error when calling {url} with params {params}", error=e
            )


def clean(input_string):
    return input_string.strip().lower().replace(",", "")


def clean_csv(input_string):
    return [clean(y) for y in str(input_string).split(", ") if y != ""]
