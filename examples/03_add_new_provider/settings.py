"""
settings.py — Configuration PayDunya
Étape 1 : définir les variables d'environnement nécessaires.
"""

import os
from functools import lru_cache


class PayDunyaSettings:
    def __init__(self):
        self.PAYDUNYA_MASTER_KEY: str = self._require("PAYDUNYA_MASTER_KEY")
        self.PAYDUNYA_PUBLIC_KEY: str = self._require("PAYDUNYA_PUBLIC_KEY")
        self.PAYDUNYA_PRIVATE_KEY: str = self._require("PAYDUNYA_PRIVATE_KEY")
        self.PAYDUNYA_TOKEN: str = self._require("PAYDUNYA_TOKEN")
        self.PAYDUNYA_BASE_URL: str = os.environ.get(
            "PAYDUNYA_BASE_URL", "https://app.paydunya.com/api/v1/"
        )
        self.PAYDUNYA_SANDBOX: bool = os.environ.get(
            "PAYDUNYA_SANDBOX", "true"
        ).lower() in ("true", "1", "yes")
        self.SITE_URL: str = os.environ.get("SITE_URL", "http://localhost:8080")

    @staticmethod
    def _require(key: str) -> str:
        value = os.environ.get(key)
        if not value:
            raise RuntimeError(f"Missing required environment variable: {key}")
        return value

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
    return PayDunyaSettings()


conf = get_paydunya_settings()
