# Protocol Transaction

`Transaction` est un `Protocol` Python — pas une classe à hériter.
N'importe quel objet exposant les bons attributs est accepté (duck typing).

## Attributs requis

| Attribut | Type | Obligatoire |
|---|---|---|
| `id` | `str` | ✅ |
| `amount` | `float` | ✅ |
| `currency` | `str` | ✅ |
| `user_email` | `str` | ✅ |
| `description` | `str | None` | ❌ |
| `user_name` | `str | None` | ❌ |
| `user_phone` | `str | None` | ❌ |

## Exemples de types compatibles

=== "dataclass"

    ```python
    from dataclasses import dataclass
    from typing import Optional

    @dataclass
    class OrderTransaction:
        id: str
        amount: float
        currency: str
        user_email: str
        description: str | None = None
        user_name: str | None = None
        user_phone: str | None = None
    ```

=== "Objet ORM (SQLAlchemy)"

    ```python
    # Aucun héritage nécessaire — les attributs suffisent
    class Transaction(Base):
        __tablename__ = "transactions"

        id = Column(String, primary_key=True)
        amount = Column(Float)
        currency = Column(String, default="XOF")
        user_email = Column(String)
        description = Column(String, nullable=True)
        user_name = Column(String, nullable=True)
        user_phone = Column(String, nullable=True)
    ```

=== "Objet simple"

    ```python
    class MyTx:
        id = "TX-99"
        amount = 2500.0
        currency = "XOF"
        user_email = "user@example.com"
        description = None
        user_name = None
        user_phone = None
    ```

## Vérification à l'exécution

```python
from paygate.base import Transaction

obj = OrderTransaction(id="X", amount=100, currency="XOF", user_email="a@b.com")
print(isinstance(obj, Transaction))  # True
```

!!! info "@runtime_checkable"
    Le Protocol est décoré `@runtime_checkable`, ce qui autorise `isinstance()`.
    Cela ne vérifie que la **présence des attributs**, pas leurs types.
