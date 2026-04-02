"""
client.py — Implémentation PayDunya
Étape 2: implémenter PaymentProvider avec les deux méthodes obligatoires.
"""

import asyncio
import json
import urllib.error
import urllib.request
from typing import Any

from paygate_africa.base import PaymentProvider, Transaction
from paygate_africa.cinetpay.settings import conf


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


class PayDunyaProvider(PaymentProvider):
    """
    Provider PayDunya.
    Doc API : https://paydunya.com/developers
    """

    @property
    def _headers(self) -> dict:
        return {
            "PAYDUNYA-MASTER-KEY": conf.PAYDUNYA_MASTER_KEY,
            "PAYDUNYA-PUBLIC-KEY": conf.PAYDUNYA_PUBLIC_KEY,
            "PAYDUNYA-PRIVATE-KEY": conf.PAYDUNYA_PRIVATE_KEY,
            "PAYDUNYA-TOKEN": conf.PAYDUNYA_TOKEN,
        }

    async def initiate_payment(self, tx: Transaction) -> str:
        """
        Crée une facture PayDunya et retourne l'URL de paiement.
        """
        url = f"{conf.PAYDUNYA_BASE_URL}checkout-invoice/create"
        payload = {
            "invoice": {
                "items": {
                    "item_0": {
                        "name": tx.description or "Paiement en ligne",
                        "quantity": 1,
                        "unit_price": str(int(tx.amount)),
                        "total_price": str(int(tx.amount)),
                    }
                },
                "total_amount": int(tx.amount),
                "description": tx.description or "Paiement en ligne",
            },
            "store": {"name": "Ma Boutique"},
            "actions": {
                "cancel_url": conf.PAYDUNYA_CANCEL_URL,
                "return_url": conf.PAYDUNYA_RETURN_URL,
                "callback_url": conf.PAYDUNYA_CALLBACK_URL,
            },
            "custom_data": {
                "transaction_id": tx.id,
                "customer_email": tx.user_email,
            },
        }

        try:
            data = await asyncio.to_thread(_post_json, url, payload, self._headers)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"PayDunya HTTP Error: {body}") from exc

        if data.get("response_code") == "00":
            return data.get("response_text", "")  # URL de la page de paiement

        raise RuntimeError(f"PayDunya error: {data.get('response_text')}")

    async def verify_payment(self, transaction_id: str) -> dict[str, Any]:
        """
        Vérifie le statut d'une facture PayDunya.
        `transaction_id` correspond au `token` de la facture PayDunya.
        """
        url = f"{conf.PAYDUNYA_BASE_URL}checkout-invoice/confirm/{transaction_id}"
        req = urllib.request.Request(url, method="GET")
        for key, value in self._headers.items():
            req.add_header(key, value)

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read())
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"PayDunya HTTP Error: {body}") from exc

        raw_status = data.get("status", "").lower()
        if raw_status == "completed":
            status = "SUCCESS"
        elif raw_status in ("pending", "pending_customer"):
            status = "PENDING"
        else:
            status = "FAILED"

        return {
            "status": status,
            "raw_data": data,
        }
