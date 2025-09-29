# PI Web API Python SDK

A modular Python SDK for interacting with the OSIsoft PI Web API. The codebase has been reorganised from a single monolithic module into a structured package that groups related controllers, configuration primitives, and the HTTP client.

## Features
- Typed configuration via `PIWebAPIConfig` and enums for authentication and WebID formats.
- Reusable `PIWebAPIClient` wrapper around `requests.Session` with centralised error handling.
- Controllers split by domain (system, assets, data, streams, etc.) for easier navigation and extension.
- Backwards-compatible `aveva_web_api.py` re-export for existing imports.

## Installation
This project depends on `requests`. Install it with:

```bash
pip install requests
```

## Quick Start
```python
from pi_web_api import AuthMethod, PIWebAPIClient, PIWebAPIConfig

config = PIWebAPIConfig(
    base_url="https://your-pi-server/piwebapi",
    auth_method=AuthMethod.ANONYMOUS,
    verify_ssl=False,  # enable in production
)

client = PIWebAPIClient(config)
print(client.home.get())
```

All controller instances are available as attributes on `PIWebAPIClient` (for example, `client.asset_server`, `client.stream`, `client.batch`).

## Package Layout
- `pi_web_api/config.py` – enums and the configuration dataclass.
- `pi_web_api/exceptions.py` – custom exception types.
- `pi_web_api/client.py` – session management and HTTP helpers.
- `pi_web_api/controllers/` – individual controller modules grouped by domain.
- `aveva_web_api.py` – compatibility shim that re-exports the public API.

## Extending the SDK
Each controller inherits from `BaseController`, which exposes helper methods and the configured client session. Add new endpoint support by placing methods on the relevant controller or creating a new module under `pi_web_api/controllers/` and registering it inside `pi_web_api/controllers/__init__.py` and `pi_web_api/client.py`.

## Documentation & Examples
Refer to `pi_web_api_reference_8-6-2025_markitdown.md` for endpoint specifics. Future improvements can include auto-generated docs and richer controller implementations.
