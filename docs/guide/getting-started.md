# Démarrage rapide

## Prérequis

- Python 3.10+
- Une application FastAPI (ou compatible `asyncio`)

## Variables d'environnement

Chaque provider lit sa configuration depuis les variables d'environnement.
Crée un fichier `.env` à la racine de ton projet :

=== "CinetPay"

    ```env
    CINETPAY_API_KEY=your_api_key
    CINETPAY_SITE_ID=your_site_id
    CINETPAY_SECRET_KEY=your_secret_key
    CINETPAY_BASE_URL=https://api-checkout.cinetpay.com/v2/
    SITE_URL=https://monsite.com
    ```

=== "Kkiapay"

    ```env
    KKIAPAY_PUBLIC_KEY=your_public_key
    KKIAPAY_PRIVATE_KEY=your_private_key
    KKIAPAY_SECRET_KEY=your_secret_key
    KKIAPAY_SANDBOX=true
    ```

## Utilisation

### 1. Définir un objet transaction

N'importe quel objet exposant les attributs du [Protocol `Transaction`](../reference/base.md) est accepté :

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class MyTransaction:
    id: str
    amount: float
    currency: str
    user_email: str
    description: str | None = None
    user_name: str | None = None
    user_phone: str | None = None
```

### 2. Sélectionner un provider

```python
from paygate_africa.factory import PaymentProviderPath, select_provider

provider = select_provider(PaymentProviderPath.CINETPAY)
# ou
provider = select_provider(PaymentProviderPath.KKIAPAY)
```

### 3. Initier un paiement

```python
tx = MyTransaction(
    id="TXN-001",
    amount=5000.0,
    currency="XOF",
    user_email="client@example.com",
    user_name="Kouamé Yao",
    description="Pack Multi-Business PDF",
)

payment_url = await provider.initiate_payment(tx)
# Redirige l'utilisateur vers payment_url
```

### 4. Vérifier le statut (après callback webhook)

```python
result = await provider.verify_payment("TXN-001")

if result["status"] == "SUCCESS":
    # Activer la commande
    pass
elif result["status"] == "PENDING":
    # Vérifier plus tard
    pass
else:
    # Paiement échoué
    pass
```

!!! info "Format de retour normalisé"
    Tous les providers retournent le même format :
    ```python
    {
        "status": "SUCCESS" | "FAILED" | "PENDING",
        "raw_data": { ... }  # Réponse brute de l'API
    }
    ```
