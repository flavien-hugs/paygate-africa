"""
Shared utility functions for the Paygate Africa library.
"""

import json
import os
import urllib.request


def post_json(url: str, payload: dict | None = None, headers: dict | None = None, method: str = "POST") -> dict:
    """
    Perform a synchronous JSON HTTP request using urllib.
    """
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")

    if headers:
        for key, value in headers.items():
            req.add_header(key, value)

    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read())


def require_env(key: str) -> str:
    """
    Retrieve an environment variable or raise a RuntimeError if not set.
    """
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value
