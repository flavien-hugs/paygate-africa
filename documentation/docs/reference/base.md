# Référence — base.py

Ce module définit le contrat commun à tous les providers.

## Protocol `Transaction`

Décrit l'interface attendue pour l'objet transaction passé à `initiate_payment`.
Grâce à `@runtime_checkable`, la conformité peut être vérifiée à l'exécution.

```python
from paygate.base import Transaction

isinstance(my_obj, Transaction)  # True si tous les attributs sont présents
```

::: paygate.base.Transaction

---

## Classe abstraite `PaymentProvider`

Tout provider doit hériter de cette classe et implémenter les deux méthodes.

::: paygate.base.PaymentProvider
