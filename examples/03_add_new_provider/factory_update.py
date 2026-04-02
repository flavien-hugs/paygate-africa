"""
factory_update.py — Étape 3 : enregistrer PayDunya dans factory.py
-------------------------------------------------------------------
Après avoir créé app/providers/paydunya/, ajouter PayDunya aux deux enums
dans factory.py pour le rendre disponible via select_provider().
"""

# Dans app/providers/factory.py, ajouter les entrées suivantes :

# from enum import Enum, unique
# import importlib
# from functools import lru_cache
#
#
# @unique
# class PaymentProviderPath(str, Enum):
#     """Dot-paths pointing to each provider's client class."""
#     KKIAPAY  = "paygate.kkiapay.client.KkiapayProvider"
#     CINETPAY = "paygate.cinetpay.client.CinetPayProvider"
#     PAYDUNYA = "paygate.paydunya.client.PayDunyaProvider"  # ← ajouter
#
#
# @unique
# class ProviderSettingsPath(str, Enum):
#     """Dot-paths pointing to each provider's settings class."""
#     KKIAPAY  = "paygate.kkiapay.settings.KkiapaySettings"
#     CINETPAY = "paygate.cinetpay.settings.CinetPaySettings"
#     PAYDUNYA = "paygate.paydunya.settings.PayDunyaSettings"  # ← ajouter


# ---------------------------------------------------------------------------
# Exemple d'utilisation une fois le provider enregistré
# ---------------------------------------------------------------------------
import asyncio
import os
import sys

# Ajout du chemin pour l'exemple standalone
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from paygate.factory import PaymentProviderPath, select_provider  # noqa: E402


async def main():
    provider = select_provider(PaymentProviderPath.PAYDUNYA)
    print(f"Provider : {type(provider).__name__}")


if __name__ == "__main__":
    asyncio.run(main())
