from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Transaction(Protocol):
    """
    Protocol describing the expected interface of a transaction object.
    Any object exposing these attributes is accepted — no hard dependency on app.models.
    """
    id: str
    amount: float
    currency: str
    description: str | None
    user_name: str | None
    user_email: str
    user_phone: str | None


class PaymentProvider(ABC):
    @abstractmethod
    async def initiate_payment(self, tx: Transaction) -> str:
        """
        Initiate a payment and return the redirection or rendering URL.
        """
        pass

    @abstractmethod
    async def verify_payment(self, transaction_id: str) -> dict[str, Any]:
        """
        Verify the status of a transaction.
        Should return a dictionary containing at least:
        - "status": "SUCCESS" or "FAILED" or "PENDING"
        - "raw_data": The full response from the provider API
        """
        pass
