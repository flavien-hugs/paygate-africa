import os
from functools import lru_cache

from ..utils import require_env


class KkiapaySettings:
    """
    Configuration settings for Kkiapay.
    """

    def __init__(self):
        self.KKIAPAY_PUBLIC_KEY: str = require_env("KKIAPAY_PUBLIC_KEY")
        self.KKIAPAY_PRIVATE_KEY: str = require_env("KKIAPAY_PRIVATE_KEY")
        self.KKIAPAY_SECRET_KEY: str = require_env("KKIAPAY_SECRET_KEY")
        self.KKIAPAY_URL: str = os.environ.get("KKIAPAY_URL", "https://api.kkiapay.me")
        self.KKIAPAY_SANDBOX_URL: str = os.environ.get(
            "KKIAPAY_SANDBOX_URL", "https://api-sandbox.kkiapay.me"
        )
        self.KKIAPAY_TRANSACTION_STATUS_URL: str = os.environ.get(
            "KKIAPAY_TRANSACTION_STATUS_URL", "/api/v1/transactions/status"
        )
        self.KKIAPAY_SANDBOX: bool = os.environ.get(
            "KKIAPAY_SANDBOX", "true"
        ).lower() in ("true", "1", "yes")
        self.KKIAPAY_RENDER_URL_TEMPLATE: str = os.environ.get(
            "KKIAPAY_RENDER_URL_TEMPLATE", "/payment/render/{id}"
        )


@lru_cache
def get_kkiapay_settings() -> KkiapaySettings:
    """
    Returns a cached instance of KkiapaySettings.
    """
    return KkiapaySettings()
