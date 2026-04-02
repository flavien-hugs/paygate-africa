from unittest.mock import patch

import pytest

from paygate_africa.kkiapay.client import KkiapayProvider


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Provide mandatory environment variables for KkiapaySettings."""
    monkeypatch.setenv("KKIAPAY_PUBLIC_KEY", "pk_test_123")
    monkeypatch.setenv("KKIAPAY_PRIVATE_KEY", "sk_test_456")
    monkeypatch.setenv("KKIAPAY_SECRET_KEY", "secret_789")


class MockTx:
    id = "TX-002"
    amount = 5000
    currency = "XOF"
    description = "Paiement Kkiapay"
    user_name = "Kouassi Koffi"
    user_email = "koffi@test.com"
    user_phone = "+22501020304"


@pytest.mark.asyncio
async def test_kkiapay_initiate_payment():
    """Test payment initiation for Kkiapay, confirming it returns the render URL."""
    provider = KkiapayProvider()
    url = await provider.initiate_payment(MockTx())
    assert "/payment/render/TX-002" in url


@pytest.mark.asyncio
async def test_kkiapay_verify_payment_success():
    """Test verification success for Kkiapay."""
    provider = KkiapayProvider()
    mock_response = {
        "status": "SUCCESS",
        "reference": "123456",
        "amount": 5000
    }

    with patch("paygate_africa.kkiapay.client._post_json", return_value=mock_response):
        result = await provider.verify_payment("123456")
        assert result["status"] == "SUCCESS"
        assert result["raw_data"] == mock_response


@pytest.mark.asyncio
async def test_kkiapay_verify_payment_failed():
    """Test verification failure for Kkiapay."""
    provider = KkiapayProvider()
    mock_response = {
        "status": "FAILED",
        "reference": "error-ref"
    }

    with patch("paygate_africa.kkiapay.client._post_json", return_value=mock_response):
        result = await provider.verify_payment("error-ref")
        assert result["status"] == "FAILED"
