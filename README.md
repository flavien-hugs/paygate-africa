# paygate-africa

[![CI/CD](https://github.com/flavien-hugs/paygate-africa/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/flavien-hugs/paygate-africa/actions/workflows/ci-cd.yml)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://flavien-hugs.github.io/paygate-africa/)
[![PyPI version](https://badge.fury.io/py/paygate-africa.svg)](https://badge.fury.io/py/paygate-africa)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**paygate-africa** est une passerelle d'abstraction Python ultra-légère conçue pour unifier les paiements en Afrique.
Intégrez **CinetPay**, **Kkiapay** et bien d'autres avec une seule interface, sans coupler votre code à des SDK tiers volumineux.

---

## Pourquoi paygate-africa ?

Intégrer les paiements africains est souvent synonyme de dépendances lourdes (`httpx`, `pydantic`, `requests`) et
de structures de données incompatibles. Nous avons créé ce module pour offrir une alternative **indépendante** et **unifiée**.

| Caractéristique | SDK Traditionnels | paygate-africa |
| :--- | :---: | :---: |
| **Dépendances** | 10MB+ (httpx, pydantic...) | **0MB (Standard Lib)** |
| **Utilisation** | SDK spécifique par provider | **Interface Unique (Factory)** |
| **Poids** | Lourd | **Ultra-léger (< 50KB)** |
| **Couplage** | Fort (modèles dictés) | **Faible (Duck Typing / Protocol)** |

---

## Fonctionnalités Clés

- **Unified Interface** : Une seule méthode `initiate_payment` et `verify_payment` pour tous les providers.
- **Asynchrone par défaut** : Conçu pour s'intégrer parfaitement avec FastAPI ou Django (avec `sync_to_async`).
- **Type Safety** : Utilisation des `Protocols` Python (PEP 544) pour une validation stricte sans dépendance `pydantic`.
- **Extensible** : Ajoutez un nouveau provider en créant seulement deux classes.
- **Zero Side-Effects** : Aucun logger imposé, aucune surcharge mémoire.

---

## Installation

```bash
pip install paygate-africa
```

---

## Exemple : Intégrer un paiement en 30 secondes

### 1. Définissez votre objet Transaction (Duck Typing)
Pas besoin d'hériter d'une classe. N'importe quel objet avec ces attributs fera l'affaire.

```python
class MyTransaction:
    id = "ORDER_123"
    amount = 5000.0
    currency = "XOF"
    user_email = "client@email.com"
    user_name = "Jean Dupont" # Optionnel
    description = "Achat Pack Pro" # Optionnel
    user_phone = "+22501020304" # Optionnel
```

### 2. Le code d'intégration
```python
import asyncio
from paygate_africa import select_provider, PaymentProviderPath

async def main():
    # Sélection dynamique (CINETPAY ou KKIAPAY)
    provider = select_provider(PaymentProviderPath.CINETPAY)

    tx = MyTransaction()

    # Initiation (redirection URL)
    payment_url = await provider.initiate_payment(tx)
    print(f"Lien de paiement : {payment_url}")

    # Vérification normalisée
    res = await provider.verify_payment(tx.id)
    if res["status"] == "SUCCESS":
        print("Paiement validé !")
```

---

## Providers Supportés

| Provider | Mécanique | Statut |
|---|---|---|
| **CinetPay** | Redirection sécurisée | Stable |
| **Kkiapay** | Widget Frontend (JS) | Stable |
| **PayDunya** | Redirection sécurisée | En cours |

---

## Folder Structure

```text
paygate-africa/
├── src/paygate_africa/
│   ├── base.py          # Interface commune (Protocol + ABC)
│   ├── factory.py       # Coeur dynamique
│   └── cinetpay/        # Implémentations spécifiques
└── tests/               # 100% de couverture mockée
```

---

## Contribution

Nous accueillons les contributions avec plaisir ! Surtout pour ajouter de nouveaux providers africains
(PayDunya, Fedapay, MonCash, etc.).

1. Clonez le dépôt et installez les dépendances dev : `poetry install`
2. Lancez les tests : `poetry run pytest`
3. Vérifiez le linting : `poetry run ruff check .`

---

## Licence

Ce projet est sous licence MIT. Libre pour usage commercial et personnel.
