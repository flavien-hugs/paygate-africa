"""
Paygate Africa: A unified interface for African payment gateways.
"""

from .base import PaymentProvider, Transaction
from .factory import PaymentProviderPath, select_provider

__version__ = "0.1.2"
__all__ = ["PaymentProvider", "Transaction", "select_provider", "PaymentProviderPath", "__version__"]
