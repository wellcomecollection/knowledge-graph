import json
import os
from pathlib import Path
from time import sleep

import structlog
from httpx import Client, Request, TimeoutException

http_client = Client(timeout=30)

base_cache_dir = Path(os.environ["CACHE_DIRECTORY"])
base_cache_dir.mkdir(exist_ok=True)

log_level = structlog.stdlib._NAME_TO_LEVEL[
    os.environ.get("LOG_LEVEL", "INFO").lower()
]
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(log_level),
)


def get_logger(name=None):
    return structlog.get_logger(name)


log = get_logger(__name__)


def fetch_json(url, params=None):
    try:
        json = cache_fetch_json(url, params)
    except FileNotFoundError:
        json = http_fetch_json(url, params)
    return json


def build_full_url(url, params):
    return str(Request("GET", url, params=params).url)


def build_cache_path(url, params):
    full_url = build_full_url(url, params)
    return base_cache_dir / f"{hash(full_url)}.json"


def cache_fetch_json(url, params=None):
    cache_path = build_cache_path(url, params)
    with open(cache_path, "r") as f:
        log.debug(f"Loading from cache {cache_path}")
        return json.load(f)


def cache_result(url, params, result):
    cache_path = build_cache_path(url, params)
    with open(cache_path, "w") as f:
        json.dump(result, f)


def http_fetch_json(url, params=None, cache=True):
    for i in range(0, 5):
        try:
            response = http_client.get(url, params=params)
            if response.status_code == 200:
                result = response.json()
                log.debug(f"Fetched {response.url}", params=params)
                if cache:
                    log.debug(f"Caching {response.url}")
                    cache_result(url, params, result)
                return result
            else:
                raise ValueError(
                    f"{response.status_code} error when calling {url}"
                )
        except (TimeoutException) as e:
            log.exception(
                f"Timed out when calling {url} with params {params}", error=e
            )
            sleep(2**i)
        except Exception as e:
            log.exception(
                f"Error when calling {url} with params {params}", error=e
            )


def clean(input_string):
    return input_string.strip().lower().replace(",", "")


def clean_csv(input_string):
    return [clean(y) for y in str(input_string).split(", ") if y != ""]
