from unittest.mock import patch

import pytest

from paygate.cinetpay.client import CinetPayProvider


# Mock settings before importing Provider if necessary
@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Provide mandatory environment variables for CinetPaySettings."""
    monkeypatch.setenv("CINETPAY_API_KEY", "dummy_key")
    monkeypatch.setenv("CINETPAY_SITE_ID", "123456")
    monkeypatch.setenv("CINETPAY_SECRET_KEY", "dummy_secret")
    monkeypatch.setenv("CINETPAY_BASE_URL", "https://api-checkout.cinetpay.com/v2/")


class MockTx:
    id = "TX-001"
    amount = 5000
    currency = "XOF"
    description = "Test transaction"
    user_name = "Test User"
    user_email = "test@example.com"
    user_phone = "+22501020304"


@pytest.mark.asyncio
async def test_cinetpay_initiate_payment():
    """Test payment initiation by mocking the urllib response."""
    provider = CinetPayProvider()
    mock_response = {
        "code": "201",
        "data": {"payment_url": "https://secure.cinetpay.com/pay/123"}
    }

    # Mock the internal _post_json call
    with patch("paygate.cinetpay.client._post_json", return_value=mock_response):
        url = await provider.initiate_payment(MockTx())
        assert url == "https://secure.cinetpay.com/pay/123"


@pytest.mark.asyncio
async def test_cinetpay_verify_payment_success():
    """Test verification with a success response."""
    provider = CinetPayProvider()
    mock_response = {
        "code": "00",
        "data": {"status": "ACCEPTED", "amount": 5000}
    }

    with patch("paygate.cinetpay.client._post_json", return_value=mock_response):
        result = await provider.verify_payment("TX-001")
        assert result["status"] == "SUCCESS"
        assert result["raw_data"] == mock_response


@pytest.mark.asyncio
async def test_cinetpay_verify_payment_failed():
    """Test verification with a failure response."""
    provider = CinetPayProvider()
    mock_response = {
        "code": "802",
        "data": {"status": "REFUSED"}
    }

    with patch("paygate.cinetpay.client._post_json", return_value=mock_response):
        result = await provider.verify_payment("TX-001")
        assert result["status"] == "FAILED"
