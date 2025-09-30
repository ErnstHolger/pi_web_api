import os
import warnings

import pytest
import urllib3

from pi_web_sdk.client import PIWebAPIClient
from pi_web_sdk.config import AuthMethod, PIWebAPIConfig
from pi_web_sdk.exceptions import PIWebAPIError


def _bool_from_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@pytest.fixture(scope="session")
def pi_web_api_client():
    """Provide a configured PI Web API client backed by the live controller."""
    base_url = os.getenv("PI_WEB_API_BASE_URL", "https://172.28.201.116/piwebapi")
    timeout = int(os.getenv("PI_WEB_API_TIMEOUT", "10"))
    verify_ssl = _bool_from_env("PI_WEB_API_VERIFY_SSL", default=False)
    auth_method_name = os.getenv("PI_WEB_API_AUTH_METHOD", "anonymous").strip().lower()

    try:
        auth_method = AuthMethod(auth_method_name)
    except ValueError as exc:
        pytest.skip(f"Unsupported auth method '{auth_method_name}': {exc}")

    config = PIWebAPIConfig(
        base_url=base_url,
        auth_method=auth_method,
        username=os.getenv("PI_WEB_API_USERNAME"),
        password=os.getenv("PI_WEB_API_PASSWORD"),
        token=os.getenv("PI_WEB_API_TOKEN"),
        verify_ssl=verify_ssl,
        timeout=timeout,
    )

    if not verify_ssl:
        warnings.filterwarnings(
            "ignore", category=urllib3.exceptions.InsecureRequestWarning
        )

    client = PIWebAPIClient(config)

    try:
        client.system.versions()
    except PIWebAPIError as exc:
        pytest.skip(f"PI Web API not reachable at {base_url}: {exc}")

    return client
