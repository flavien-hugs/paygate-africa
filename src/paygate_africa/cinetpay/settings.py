import os
from functools import lru_cache


class CinetPaySettings:
    def __init__(self):
        self.CINETPAY_SITE_ID: str = self._require("CINETPAY_SITE_ID")
        self.CINETPAY_API_KEY: str = self._require("CINETPAY_API_KEY")
        self.CINETPAY_SECRET_KEY: str = self._require("CINETPAY_SECRET_KEY")
        self.CINETPAY_BASE_URL: str = self._require("CINETPAY_BASE_URL")
        self.SITE_URL: str = os.environ.get("SITE_URL", "http://localhost:8080")

    @staticmethod
    def _require(key: str) -> str:
        value = os.environ.get(key)
        if not value:
            raise RuntimeError(f"Missing required environment variable: {key}")
        return value

    @property
    def CINETPAY_NOTIFY_URL(self) -> str:
        return f"{self.SITE_URL}/webhooks/cinetpay"

    @property
    def CINETPAY_RETURN_URL(self) -> str:
        return f"{self.SITE_URL}/payment/success"


@lru_cache
def get_cinetpay_settings() -> CinetPaySettings:
    return CinetPaySettings()
