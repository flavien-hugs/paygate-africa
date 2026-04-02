"""
02_custom_transaction.py
------------------------
Démonstration du Protocol `Transaction` (duck typing).

Le Protocol est @runtime_checkable : n'importe quel objet Python exposant
les bons attributs est valide — pas besoin d'hériter d'une classe de base.
Cela permet d'utiliser vos propres modèles (SQLAlchemy, dataclass, dict-like…)
sans modifier le package.
"""

import asyncio
from dataclasses import dataclass, field

from paygate.base import Transaction
from paygate.factory import PaymentProviderPath, select_provider


# ---------------------------------------------------------------------------
# Exemple 1 : dataclass standard
# ---------------------------------------------------------------------------
@dataclass
class OrderTransaction:
    """Modèle métier "commande" compatible avec le Protocol Transaction."""
    id: str
    amount: float
    currency: str
    user_email: str
    description: str | None = None
    user_name: str | None = None
    user_phone: str | None = None
    # Champs supplémentaires propres à votre domaine :
    order_ref: str = field(default="")
    product_slug: str = field(default="")


# ---------------------------------------------------------------------------
# Exemple 2 : objet SQLAlchemy (simulé)
# ---------------------------------------------------------------------------
class FakeDBTransaction:
    """Simule un enregistrement ORM — aucun héritage requis."""

    def __init__(self, row: dict):
        self.id = row["id"]
        self.amount = float(row["amount"])
        self.currency = row.get("currency", "XOF")
        self.description = row.get("description")
        self.user_name = row.get("user_name")
        self.user_email = row["user_email"]
        self.user_phone = row.get("user_phone")


def check_protocol_compliance(obj):
    """Vérifie à l'exécution si un objet respecte le Protocol Transaction."""
    if isinstance(obj, Transaction):
        print(f"✅ {type(obj).__name__} est compatible avec Transaction")
    else:
        print(f"❌ {type(obj).__name__} ne respecte pas le Protocol Transaction")


async def main():
    # Vérification de conformité au Protocol
    order = OrderTransaction(
        id="ORD-2024-001",
        amount=9990.0,
        currency="XOF",
        user_email="client@example.com",
        user_name="Ama Kofi",
        description="Pack PDF + Audio",
        order_ref="REF-ABC",
        product_slug="pack-multi-business-full",
    )
    db_row = FakeDBTransaction({
        "id": "DB-42",
        "amount": "6990",
        "user_email": "autre@example.com",
        "user_name": "Koffi Mensah",
    })

    check_protocol_compliance(order)
    check_protocol_compliance(db_row)

    # Les deux objets peuvent être passés directement au provider
    provider = select_provider(PaymentProviderPath.KKIAPAY)
    render_url = await provider.initiate_payment(order)
    print(f"\nKkiapay render URL : {render_url}")


if __name__ == "__main__":
    asyncio.run(main())
