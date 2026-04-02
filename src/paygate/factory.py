import importlib
from enum import Enum, unique
from functools import lru_cache


@unique
class PaymentProviderPath(str, Enum):
    """Dot-paths pointing to each provider's client class."""
    KKIAPAY = "paygate.kkiapay.client.KkiapayProvider"
    CINETPAY = "paygate.cinetpay.client.CinetPayProvider"


@unique
class ProviderSettingsPath(str, Enum):
    """Dot-paths pointing to each provider's settings class."""
    KKIAPAY = "paygate.kkiapay.settings.KkiapaySettings"
    CINETPAY = "paygate.cinetpay.settings.CinetPaySettings"


def validate_payment_provider(value):
    if value.upper() not in PaymentProviderPath.__members__:
        raise ValueError(f"Invalid payment provider: {value}")
    return value.upper()


@lru_cache
def load_provider_class(dot_path: str):
    module_path, class_name = dot_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    provider_class = getattr(module, class_name)
    return provider_class


def select_provider(dotpath: str):
    provider_class = load_provider_class(dotpath)
    return provider_class()
