import asyncio
import json as json_lib
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urljoin

from ..base import PaymentProvider, Transaction
from .settings import get_kkiapay_settings


def _post_json(url: str, payload: dict, headers: dict | None = None) -> dict:
    """Synchronous JSON POST via urllib — wrapped with asyncio.to_thread for async use."""
    data = json_lib.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json_lib.loads(response.read())


class KkiapayProvider(PaymentProvider):
    @property
    def conf(self):
        return get_kkiapay_settings()

    async def initiate_payment(self, tx: Transaction) -> str:
        """
        Return the render URL for Kkiapay since it requires a frontend widget.
        The URL is built from the KKIAPAY_RENDER_URL_TEMPLATE setting.
        """
        return self.conf.KKIAPAY_RENDER_URL_TEMPLATE.format(id=tx.id)

    async def verify_payment(self, transaction_id: str) -> dict[str, Any]:
        """
        Check the status of a transaction using Kkiapay API.
        Returns a normalized dict with:
        - "status": "SUCCESS" | "FAILED" | "PENDING"
        - "raw_data": the full response from the Kkiapay API
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
            data = await asyncio.to_thread(_post_json, url, payload, headers)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP Error: {body}") from exc

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
