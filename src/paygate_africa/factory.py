import importlib
from enum import Enum, unique
from functools import lru_cache

from .base import PaymentProvider


@unique
class PaymentProviderPath(str, Enum):
    """
    Registry of dot-paths pointing to each provider's implementation.
    """
    KKIAPAY = "paygate_africa.kkiapay.client.KkiapayProvider"
    CINETPAY = "paygate_africa.cinetpay.client.CinetPayProvider"


@unique
class ProviderSettingsPath(str, Enum):
    """
    Registry of dot-paths pointing to each provider's settings.
    """
    KKIAPAY = "paygate_africa.kkiapay.settings.KkiapaySettings"
    CINETPAY = "paygate_africa.cinetpay.settings.CinetPaySettings"


def validate_payment_provider(provider_name: str) -> str:
    """
    Ensures a given provider name is recognized by the library.
    """
    if provider_name.upper() not in PaymentProviderPath.__members__:
        raise ValueError(f"Unknown payment provider: {provider_name}")
    return provider_name.upper()


@lru_cache
def load_provider_class(dot_path: str):
    """
    Dynamically loads a class from its dot-path.
    """
    module_path, class_name = dot_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def select_provider(dot_path: str) -> PaymentProvider:
    """
    Factory function to instantiate a provider from its dot-path.
    """
    provider_class = load_provider_class(dot_path)
    return provider_class()
