import os
from functools import lru_cache

from ..utils import require_env


class CinetPaySettings:
    """
    Configuration settings for CinetPay.
    """

    def __init__(self):
        self.CINETPAY_SITE_ID: str = require_env("CINETPAY_SITE_ID")
        self.CINETPAY_API_KEY: str = require_env("CINETPAY_API_KEY")
        self.CINETPAY_SECRET_KEY: str = require_env("CINETPAY_SECRET_KEY")
        self.CINETPAY_BASE_URL: str = require_env("CINETPAY_BASE_URL")
        self.SITE_URL: str = os.environ.get("SITE_URL", "http://localhost:8080")

    @property
    def CINETPAY_NOTIFY_URL(self) -> str:
        """
        The URL to which CinetPay will send payment notifications.
        """
        return f"{self.SITE_URL}/webhooks/cinetpay"

    @property
    def CINETPAY_RETURN_URL(self) -> str:
        """
        The URL to which the customer will be redirected after payment.
        """
        return f"{self.SITE_URL}/payment/success"


@lru_cache
def get_cinetpay_settings() -> CinetPaySettings:
    """
    Returns a cached instance of CinetPaySettings.
    """
    return CinetPaySettings()
