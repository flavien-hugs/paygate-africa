# Ajouter un nouveau provider

Ce guide explique comment intégrer un nouveau fournisseur de paiement en 3 étapes.

## Structure à créer

```
app/providers/
└── myprovider/
    ├── __init__.py
    ├── settings.py
    └── client.py
```

## Étape 1 — Settings

Crée `myprovider/settings.py` en lisant ta configuration depuis `os.environ` :

```python
import os
from functools import lru_cache


class MyProviderSettings:
    def __init__(self):
        self.MY_API_KEY: str = self._require("MY_API_KEY")
        self.MY_BASE_URL: str = os.environ.get(
            "MY_BASE_URL", "https://api.myprovider.com/v1/"
        )

    @staticmethod
    def _require(key: str) -> str:
        value = os.environ.get(key)
        if not value:
            raise RuntimeError(f"Missing required environment variable: {key}")
        return value


@lru_cache
def get_settings() -> MyProviderSettings:
    return MyProviderSettings()


conf = get_settings()
```

## Étape 2 — Client

Crée `myprovider/client.py` en implémentant les deux méthodes abstraites :

```python
import asyncio
import json
import urllib.error
import urllib.request
from typing import Any, Dict

from paygate_africa.base import PaymentProvider, Transaction
from .settings import conf


def _post_json(url: str, payload: dict, headers: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


class MyProvider(PaymentProvider):
    async def initiate_payment(self, tx: Transaction) -> str:
        url = f"{conf.MY_BASE_URL}payments"
        payload = {
            "amount": int(tx.amount),
            "currency": tx.currency,
            "reference": tx.id,
            "customer_email": tx.user_email,
        }
        data = await asyncio.to_thread(_post_json, url, payload)
        return data["payment_url"]

    async def verify_payment(self, transaction_id: str) -> Dict[str, Any]:
        url = f"{conf.MY_BASE_URL}payments/{transaction_id}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {conf.MY_API_KEY}")
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())

        raw_status = data.get("status", "").upper()
        status = "SUCCESS" if raw_status == "PAID" else (
            "PENDING" if raw_status == "PENDING" else "FAILED"
        )
        return {"status": status, "raw_data": data}
```

## Étape 3 — Enregistrer dans factory.py

Ajoute ton provider aux deux enums dans `factory.py` :

```python
@unique
class PaymentProviderPath(str, Enum):
    KKIAPAY   = "paygate_africa.kkiapay.client.KkiapayProvider"
    CINETPAY  = "paygate_africa.cinetpay.client.CinetPayProvider"
    MYPROVIDER = "paygate_africa.myprovider.client.MyProvider"  # (1)

@unique
class ProviderSettingsPath(str, Enum):
    KKIAPAY   = "paygate_africa.kkiapay.settings.KkiapaySettings"
    CINETPAY  = "paygate_africa.cinetpay.settings.CinetPaySettings"
    MYPROVIDER = "paygate_africa.myprovider.settings.MyProviderSettings"  # (2)
```

1. Dot-path vers la classe client de ton provider.
2. Dot-path vers la classe settings de ton provider.

!!! warning "Contrainte `@unique`"
    Les deux enums sont décorés `@unique` — chaque valeur dot-path doit être unique.

## Résultat

Ton provider est immédiatement disponible :

```python
provider = select_provider(PaymentProviderPath.MYPROVIDER)
url = await provider.initiate_payment(tx)
```

Consulte le [dossier d'exemples](../examples/basic-usage.md) pour un exemple complet avec PayDunya.
