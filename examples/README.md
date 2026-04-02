# Exemples d'utilisation

Ce dossier contient des exemples autonomes illustrant les cas d'usage du package `payment-providers`.

| Fichier | Description |
|---|---|
| `01_basic_usage.py` | Utilisation du factory pour initier et vérifier un paiement |
| `02_custom_transaction.py` | Utiliser le Protocol `Transaction` avec un objet métier personnalisé |
| `03_add_new_provider/` | Guide complet pour ajouter un nouveau provider (ex: PayDunya) |

> Les exemples utilisent des stubs pour simuler `app.config` et `app.providers`
> afin de pouvoir être lus et compris sans avoir toute l'application configurée.
