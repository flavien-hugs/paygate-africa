import asyncio
import urllib.error
from typing import Any
from urllib.parse import urljoin

from ..base import PaymentProvider, Transaction
from ..utils import post_json
from .settings import get_kkiapay_settings


class KkiapayProvider(PaymentProvider):
    """
    Payment provider implementation for Kkiapay.
    """

    @property
    def conf(self):
        """
        Returns the Kkiapay configuration settings.
        """
        return get_kkiapay_settings()

    async def initiate_payment(self, tx: Transaction) -> str:
        """
        Return the render URL for Kkiapay.
        Kkiapay usually requires a frontend widget; this URL directs to the widget renderer.
        """
        return self.conf.KKIAPAY_RENDER_URL_TEMPLATE.format(id=tx.id)

    async def verify_payment(self, transaction_id: str) -> dict[str, Any]:
        """
        Verify the status of a transaction with the Kkiapay API.
        """
        base_url = self.conf.KKIAPAY_SANDBOX_URL if self.conf.KKIAPAY_SANDBOX else self.conf.KKIAPAY_URL
        url = urljoin(base_url, self.conf.KKIAPAY_TRANSACTION_STATUS_URL)
        headers = {
            "X-SECRET-KEY": self.conf.KKIAPAY_SECRET_KEY,
            "X-API-KEY": self.conf.KKIAPAY_PUBLIC_KEY,
            "X-PRIVATE-KEY": self.conf.KKIAPAY_PRIVATE_KEY,
        }
        payload = {"transactionId": transaction_id}

        try:
            data = await asyncio.to_thread(post_json, url, payload, headers)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Kkiapay API Error: {body}") from exc

        raw_status = data.get("status", "").upper()
        if raw_status in ("SUCCESS", "COMPLETE", "COMPLETED"):
            status = "SUCCESS"
        elif raw_status in ("PENDING", "INITIATED"):
            status = "PENDING"
        else:
            status = "FAILED"

        return {
            "status": status,
            "raw_data": data,
        }
