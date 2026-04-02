import pytest

from paygate.base import PaymentProvider
from paygate.factory import PaymentProviderPath, load_provider_class, select_provider


def test_enum_paths():
    """Verify that all enums correspond to valid dot-paths within the package."""
    for path in PaymentProviderPath:
        assert path.startswith("paygate.")
        assert path.endswith("Provider")


def test_load_provider_class():
    """Verify that each provider class can be dynamically loaded."""
    for path in PaymentProviderPath:
        cls = load_provider_class(path)
        assert issubclass(cls, PaymentProvider)


def test_select_provider():
    """Verify that selecting a provider via the enum returns an instance of PaymentProvider."""
    provider = select_provider(PaymentProviderPath.CINETPAY)
    assert isinstance(provider, PaymentProvider)
    assert type(provider).__name__ == "CinetPayProvider"


def test_invalid_provider():
    """Verify that an invalid dot-path raises an ImportError or AttributeError during loading."""
    with pytest.raises((ImportError, AttributeError, ValueError)):
        load_provider_class("paygate.invalid.UnknownProvider")
