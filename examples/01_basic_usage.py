"""
01_basic_usage.py
-----------------
Exemple de base : sélectionner un provider via le factory,
initier un paiement et vérifier son statut.
"""

import asyncio

# ---------------------------------------------------------------------------
# Dans votre application, ces imports viendraient directement du package :
#
#   from paygate_africa.factory import PaymentProviderPath, select_provider
#
# ---------------------------------------------------------------------------
from paygate_africa.factory import PaymentProviderPath, select_provider


# ---------------------------------------------------------------------------
# Objet transaction minimal respectant le Protocol `Transaction`
# ---------------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # 1. Sélectionner le provider via l'enum (chargement dynamique)
    # ------------------------------------------------------------------
    provider = select_provider(PaymentProviderPath.CINETPAY)
    print(f"Provider chargé : {type(provider).__name__}")

    # ------------------------------------------------------------------
    # 2. Initier le paiement → retourne l'URL de redirection
    # ------------------------------------------------------------------
    payment_url = await provider.initiate_payment(tx)
    print(f"URL de paiement : {payment_url}")

    # ------------------------------------------------------------------
    # 3. Vérifier le statut (après callback du provider)
    # ------------------------------------------------------------------
    result = await provider.verify_payment(tx.id)
    print(f"Statut  : {result['status']}")
    print(f"Données brutes : {result['raw_data']}")


if __name__ == "__main__":
    asyncio.run(main())
