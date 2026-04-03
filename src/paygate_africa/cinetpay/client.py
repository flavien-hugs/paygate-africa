import asyncio
import logging
import os
import socket
import urllib.error
from typing import Any

from ..base import PaymentProvider, Transaction
from ..utils import post_json
from .settings import get_cinetpay_settings

logger = logging.getLogger(__name__)


class CinetPayProvider(PaymentProvider):
    """
    Payment provider implementation for CinetPay.
    """

    @property
    def conf(self):
        """
        Returns the CinetPay configuration settings.
        """
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

        # Network debug logging
        is_debug = os.environ.get("DEBUG", "false").lower() in ("true", "1", "yes")
        if is_debug:
            hostname = self.conf.CINETPAY_BASE_URL.split("//")[-1].split("/")[0]
            try:
                ip = socket.gethostbyname(hostname)
                logger.debug(f"DNS Resolution: {hostname} -> {ip}")
                with socket.create_connection((hostname, 443), timeout=5):
                    logger.debug(f"TCP Connection to {hostname}:443 successful")
            except Exception as e:
                logger.warning(f"Connectivity check failed for {hostname}: {e}")

        logger.info(f"Initiating payment via CinetPay: {tx.id}")
        try:
            data = await asyncio.to_thread(post_json, url, payload)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            logger.error(f"CinetPay API Error: {body}")
            raise RuntimeError(f"CinetPay API Error: {body}") from exc

        if isinstance(data, dict) and str(data.get("code")) == "201":
            return data.get("data", {}).get("payment_url", "")

        logger.error(f"Unexpected CinetPay API response: {data}")
        raise RuntimeError(f"Unexpected CinetPay API response: {data}")

    async def verify_payment(self, transaction_id: str) -> dict[str, Any]:
        """
        Verify the status of a transaction on CinetPay.
        """
        url = f"{self.conf.CINETPAY_BASE_URL}payment/check"
        payload = {
            "apikey": self.conf.CINETPAY_API_KEY,
            "site_id": self.conf.CINETPAY_SITE_ID,
            "transaction_id": transaction_id,
        }

        try:
            data = await asyncio.to_thread(post_json, url, payload)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"CinetPay API Error: {body}") from exc

        status_code = data.get("code")
        cp_data = data.get("data", {})
        cp_status = cp_data.get("status") if isinstance(cp_data, dict) else None
        is_success = status_code == "00" or cp_status == "ACCEPTED"

        return {
            "status": "SUCCESS" if is_success else "FAILED",
            "raw_data": data,
        }
