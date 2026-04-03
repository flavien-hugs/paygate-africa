# Ajouter un nouveau provider

Ce guide explique comment intégrer un nouveau fournisseur de paiement en 3 étapes, en suivant l'architecture de la bibliothèque.

## Structure à créer

Ton nouveau provider doit être placé dans le sous-dossier `src/paygate_africa/` :

```text
src/paygate_africa/
└── myprovider/
    ├── __init__.py
    ├── settings.py
    └── client.py
```

## Étape 1 — Configuration (`settings.py`)

Utilise l'utilitaire `require_env` pour valider tes variables d'environnement.

```python
import os
from functools import lru_cache
from ..utils import require_env

class MyProviderSettings:
    """Configuration du nouveau provider."""
    
    def __init__(self):
        # require_env lève une RuntimeError si la variable est absente
        self.MY_API_KEY: str = require_env("MY_API_KEY")
        self.MY_BASE_URL: str = os.environ.get(
            "MY_BASE_URL", "https://api.myprovider.com/v1/"
        )

@lru_cache
def get_settings() -> MyProviderSettings:
    """Récupère l'instance singleton des settings."""
    return MyProviderSettings()
```

## Étape 2 — Client (`client.py`)

Implémente l'interface `PaymentProvider`. Utilise `post_json` de `..utils` pour tes appels API (elle gère les headers et l'encodage JSON via `urllib`).

```python
import asyncio
import urllib.error
from typing import Any

from ..base import PaymentProvider, Transaction
from ..utils import post_json
from .settings import get_settings

class MyProvider(PaymentProvider):
    """Implémentation du provider MyProvider."""

    @property
    def conf(self):
        return get_settings()

    async def initiate_payment(self, tx: Transaction) -> str:
        url = f"{self.conf.MY_BASE_URL}payments"
        payload = {
            "amount": int(tx.amount),
            "currency": tx.currency,
            "reference": tx.id,
            "email": tx.user_email,
        }
        
        # Exécute l'appel bloquant (urllib) dans un thread séparé
        data = await asyncio.to_thread(post_json, url, payload)
        return data["checkout_url"]

    async def verify_payment(self, transaction_id: str) -> dict[str, Any]:
        url = f"{self.conf.MY_BASE_URL}status/{transaction_id}"
        headers = {"Authorization": f"Bearer {self.conf.MY_API_KEY}"}
        
        try:
            data = await asyncio.to_thread(post_json, url, {}, headers)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"Erreur API : {exc.read()}") from exc

        # Normalisation du statut
        raw = data.get("status", "").upper()
        status = "SUCCESS" if raw == "PAID" else (
            "PENDING" if raw == "INITIATED" else "FAILED"
        )
        
        return {"status": status, "raw_data": data}
```

## Étape 3 — Enregistrement (`factory.py`)

Pour que ton provider soit accessible via `select_provider()`, ajoute-le aux enums de `src/paygate_africa/factory.py` :

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

1.  **Dot-path** vers la classe du client.
2.  **Dot-path** vers la classe de configuration.

!!! success "Terminé !"
    Ton provider est maintenant disponible via :
    ```python
    from paygate_africa import select_provider, PaymentProviderPath
    provider = select_provider(PaymentProviderPath.MYPROVIDER)
    ```
