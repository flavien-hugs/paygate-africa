import asyncio
import json
import logging
import os
import socket
import urllib.error
import urllib.request
from typing import Any

from ..base import PaymentProvider, Transaction
from .settings import get_cinetpay_settings

logger = logging.getLogger(__name__)


def _post_json(url: str, payload: dict, headers: dict | None = None) -> dict:
    """Synchronous JSON POST via urllib — wrapped with asyncio.to_thread for async use."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read())


class CinetPayProvider(PaymentProvider):
    @property
    def conf(self):
        return get_cinetpay_settings()

    async def initiate_payment(self, tx: Transaction) -> str:
        """
        Initiate a payment with CinetPay and return the redirection URL.
        """
        url = f"{self.conf.CINETPAY_BASE_URL}payment"
        name_parts = tx.user_name.split() if tx.user_name else []
        payload = {
            "apikey": self.conf.CINETPAY_API_KEY,
            "site_id": self.conf.CINETPAY_SITE_ID,
            "transaction_id": tx.id,
            "amount": int(tx.amount),
            "currency": tx.currency,
            "description": tx.description or "Paiement en ligne",
            "notify_url": self.conf.CINETPAY_NOTIFY_URL,
            "return_url": self.conf.CINETPAY_RETURN_URL,
            "customer_name": name_parts[0] if name_parts else "Client",
            "customer_surname": name_parts[-1] if len(name_parts) > 1 else "",
            "customer_email": tx.user_email,
            "customer_phone_number": tx.user_phone or "",
        }

        # Diagnostic Réseau (activé uniquement en mode DEBUG)
        is_debug = os.environ.get("DEBUG", "false").lower() in ("true", "1", "yes")
        if is_debug:
            hostname = self.conf.CINETPAY_BASE_URL.split("//")[-1].split("/")[0]
            try:
                ip = socket.gethostbyname(hostname)
                logger.info(f"Diagnostic - DNS Resolution: {hostname} -> {ip}")
                with socket.create_connection((hostname, 443), timeout=5):
                    logger.info(f"Diagnostic - TCP Connection to {hostname}:443 successful")
            except Exception as diag_exc:
                logger.error(f"Diagnostic - Network failure for {hostname}: {diag_exc}")

        logger.info(f"Initiating payment at URL: {url}")
        try:
            data = await asyncio.to_thread(_post_json, url, payload)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            logger.error(f"HTTP Error: {body}")
            raise RuntimeError(f"HTTP Error: {body}") from exc

        if isinstance(data, dict) and str(data.get("code")) == "201":
            return data.get("data", {}).get("payment_url", "")

        logger.error(f"Unexpected CinetPay response: {data}")
        raise RuntimeError(f"Unexpected CinetPay response: {data}")

    async def verify_payment(self, transaction_id: str) -> dict[str, Any]:
        """
        Check the status of a transaction on CinetPay.
        Returns a normalized dict with:
        - "status": "SUCCESS" | "FAILED"
        - "raw_data": the full response from the CinetPay API
        """
        url = f"{self.conf.CINETPAY_BASE_URL}payment/check"
        payload = {
            "apikey": self.conf.CINETPAY_API_KEY,
            "site_id": self.conf.CINETPAY_SITE_ID,
            "transaction_id": transaction_id,
        }

        try:
            data = await asyncio.to_thread(_post_json, url, payload)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP Error: {body}") from exc

        status_code = data.get("code")
        cp_data = data.get("data", {})
        cp_status = cp_data.get("status") if isinstance(cp_data, dict) else None
        is_success = status_code == "00" or cp_status == "ACCEPTED"

        return {
            "status": "SUCCESS" if is_success else "FAILED",
            "raw_data": data,
        }
