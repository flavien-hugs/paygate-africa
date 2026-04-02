from paygate.base import Transaction


class SimpleTx:
    def __init__(self, tx_id, amount, email):
        self.id = tx_id
        self.amount = amount
        self.currency = "XOF"
        self.description = "Test"
        self.user_name = "Test User"
        self.user_email = email
        self.user_phone = "+12345678"


def test_transaction_protocol():
    """Verify that a compliant object is correctly recognized as a Transaction."""
    tx = SimpleTx("1", 500.0, "test@example.com")
    assert isinstance(tx, Transaction)


def test_transaction_protocol_missing_attr():
    """Verify that an object missing attributes is not recognized."""

    class IncompleteTx:
        id = "1"
        amount = 100.0

    tx = IncompleteTx()
    assert not isinstance(tx, Transaction)
