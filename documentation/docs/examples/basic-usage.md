# Utilisation de base

Exemple complet : sélectionner un provider, initier un paiement, vérifier le statut.

## Code

```python linenums="1"
import asyncio
from paygate.factory import PaymentProviderPath, select_provider


class SampleTransaction:
    id = "TXN-001"
    amount = 5000.0
    currency = "XOF"
    description = "Pack Multi-Business PDF"
    user_name = "Kouamé Yao"
    user_email = "kouame@example.com"
    user_phone = "+22500000000"


async def main():
    tx = SampleTransaction()

    # 1. Charger le provider
    provider = select_provider(PaymentProviderPath.CINETPAY)

    # 2. Initier le paiement → URL de redirection
    payment_url = await provider.initiate_payment(tx)
    print(f"Rediriger l'utilisateur vers : {payment_url}")

    # 3. Vérifier après le callback webhook
    result = await provider.verify_payment(tx.id)
    print(f"Statut : {result['status']}")


asyncio.run(main())
```

## Changer de provider

Il suffit de changer l'enum sans toucher au reste du code :

```python
provider = select_provider(PaymentProviderPath.KKIAPAY)
```

!!! tip "Sélection dynamique depuis la config"
    ```python
    import os
    from paygate.factory import PaymentProviderPath, select_provider, validate_payment_provider

    name = validate_payment_provider(os.environ.get("PAYMENT_PROVIDER", "cinetpay"))
    provider = select_provider(PaymentProviderPath[name])
    ```
