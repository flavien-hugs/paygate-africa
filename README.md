# payment-providers

Module Python d'abstraction des passerelles de paiement. Il fournit une interface unifiée
pour intégrer plusieurs fournisseurs de paiement sans coupler le reste de l'application à
un SDK tiers.

**Dépendances externes : aucune** — uniquement la bibliothèque standard Python.

---

## Architecture

```
payment-providers/
├── base.py          # Contrat abstrait (ABC) + Protocol Transaction
├── factory.py       # Chargement dynamique des providers
├── cinetpay/
│   ├── client.py    # Implémentation CinetPay
│   └── settings.py  # Configuration via variables d'environnement
└── kkiapay/
    ├── client.py    # Implémentation Kkiapay
    └── settings.py  # Configuration via variables d'environnement
```

### Patron de conception

Le module implémente le patron **Strategy + Factory** :

- `PaymentProvider` (ABC) définit le contrat commun à tous les providers.
- `Transaction` (Protocol) décrit l'objet attendu en entrée — n'importe quel objet Python
    exposant les bons attributs est accepté (duck typing).
- `factory.py` charge dynamiquement le bon provider via `importlib`, avec mise en cache via
    `lru_cache`.

---

## Contrat

Chaque provider implémente deux méthodes asynchrones :

```python
async def initiate_payment(self, tx: Transaction) -> str:
    """Initialise un paiement. Retourne l'URL de redirection ou de rendu."""

async def verify_payment(self, transaction_id: str) -> dict:
    """Vérifie le statut d'une transaction. Retourne un dict normalisé."""
```

### Format de retour de `verify_payment`

```python
{
    "status": "SUCCESS" | "FAILED" | "PENDING",
    "raw_data": { ... }  # Réponse brute de l'API du provider
}
```

### Protocol `Transaction`

```python
class Transaction(Protocol):
    id: str
    amount: float
    currency: str
    description: str | None
    user_name: str | None
    user_email: str
    user_phone: str | None
```

---

## Providers

### CinetPay

Paiement via redirection : `initiate_payment` renvoie une URL de paiement hébergée sur CinetPay.

**Variables d'environnement requises :**

| Variable | Description |
|---|---|
| `CINETPAY_API_KEY` | Clé API CinetPay |
| `CINETPAY_SITE_ID` | Identifiant du site |
| `CINETPAY_SECRET_KEY` | Clé secrète |
| `CINETPAY_BASE_URL` | URL de base de l'API (ex: `https://api-checkout.cinetpay.com/v2/`) |
| `SITE_URL` | URL publique du site (défaut : `http://localhost:8080`) |

Les URLs de notification et de retour sont construites automatiquement :
- `notify_url` → `{SITE_URL}/webhooks/cinetpay`
- `return_url` → `{SITE_URL}/payment/success`

---

### Kkiapay

Paiement via widget frontend : `initiate_payment` renvoie une URL de rendu interne
(`/payment/kkiapay/render/{tx.id}`).
La vérification se fait via l'API Kkiapay avec le `transactionId` retourné par le widget.

**Variables d'environnement requises :**

| Variable | Description |
|---|---|
| `KKIAPAY_PUBLIC_KEY` | Clé publique |
| `KKIAPAY_PRIVATE_KEY` | Clé privée |
| `KKIAPAY_SECRET_KEY` | Clé secrète |

**Variables optionnelles :**

| Variable | Défaut |
|---|---|
| `KKIAPAY_URL` | `https://api.kkiapay.me` |
| `KKIAPAY_SANDBOX_URL` | `https://api-sandbox.kkiapay.me` |
| `KKIAPAY_TRANSACTION_STATUS_URL` | `/api/v1/transactions/status` |
| `KKIAPAY_SANDBOX` | `true` |

---

## Utilisation

### Sélectionner un provider dynamiquement

```python
from app.providers.factory import PaymentProviderPath, select_provider

provider = select_provider(PaymentProviderPath.CINETPAY)
url = await provider.initiate_payment(tx)
```

### Valider la valeur d'un provider

```python
from app.providers.factory import validate_payment_provider

name = validate_payment_provider("cinetpay")  # "CINETPAY"
```

### Ajouter un nouveau provider

1. Créer un dossier `myprovider/` avec `__init__.py`, `client.py`, `settings.py`.
2. Implémenter `MyProvider(PaymentProvider)` avec `initiate_payment` et `verify_payment`.
3. Ajouter les entrées dans `factory.py` :

```python
class PaymentProviderPath(str, Enum):
    MYPROVIDER = "app.providers.myprovider.client.MyProvider"

class ProviderSettingsPath(str, Enum):
    MYPROVIDER = "app.providers.myprovider.settings.MyProviderSettings"
```

---

## Notes

- Les appels HTTP sont réalisés avec `urllib.request` (stdlib) encapsulé dans
  `asyncio.to_thread` pour rester compatible avec un contexte async (FastAPI, etc.).
- La configuration est chargée une seule fois au démarrage grâce à `lru_cache`.
- Le diagnostic réseau CinetPay (DNS + TCP) n'est activé qu'en mode `DEBUG`.
