from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Transaction(Protocol):
    """
    Protocol defining the required interface for a transaction object.
    Any object that implements these attributes can be used as a transaction.
    """
    id: str
    amount: float
    currency: str
    description: str | None
    user_name: str | None
    user_email: str
    user_phone: str | None


class PaymentProvider(ABC):
    """
    Abstract base class for payment providers.
    """

    @abstractmethod
    async def initiate_payment(self, tx: Transaction) -> str:
        """
        Initiate a payment and return the checkout or redirection URL.
        """
        pass

    @abstractmethod
    async def verify_payment(self, transaction_id: str) -> dict[str, Any]:
        """
        Verify the status of a transaction.
        Returns a dictionary with:
        - "status": "SUCCESS", "FAILED", or "PENDING"
        - "raw_data": The original response from the provider's API
        """
        pass
