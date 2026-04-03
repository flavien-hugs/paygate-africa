import os
from functools import lru_cache

from paygate_africa.utils import require_env


class PayDunyaSettings:
    """
    Configuration settings for PayDunya.
    """

    def __init__(self):
        # Utilise l'utilitaire de la lib pour la validation
        self.PAYDUNYA_MASTER_KEY: str = require_env("PAYDUNYA_MASTER_KEY")
        self.PAYDUNYA_PUBLIC_KEY: str = require_env("PAYDUNYA_PUBLIC_KEY")
        self.PAYDUNYA_PRIVATE_KEY: str = require_env("PAYDUNYA_PRIVATE_KEY")
        self.PAYDUNYA_TOKEN: str = require_env("PAYDUNYA_TOKEN")
        self.PAYDUNYA_BASE_URL: str = os.environ.get(
            "PAYDUNYA_BASE_URL", "https://app.paydunya.com/api/v1/"
        )
        self.PAYDUNYA_SANDBOX: bool = os.environ.get(
            "PAYDUNYA_SANDBOX", "true"
        ).lower() in ("true", "1", "yes")
        self.SITE_URL: str = os.environ.get("SITE_URL", "http://localhost:8080")

    @property
    def PAYDUNYA_CALLBACK_URL(self) -> str:
        return f"{self.SITE_URL}/webhooks/paydunya"

    @property
    def PAYDUNYA_RETURN_URL(self) -> str:
        return f"{self.SITE_URL}/payment/success"

    @property
    def PAYDUNYA_CANCEL_URL(self) -> str:
        return f"{self.SITE_URL}/payment/cancel"


@lru_cache
def get_paydunya_settings() -> PayDunyaSettings:
    """
    Returns a cached instance of PayDunyaSettings.
    """
    return PayDunyaSettings()


conf = get_paydunya_settings()
