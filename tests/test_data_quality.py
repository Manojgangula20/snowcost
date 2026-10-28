
from decimal import Decimal


VALID_STATUSES = {"SETTLED", "DECLINED"}


def validate_transaction(transaction: dict) -> list[str]:
    """Return data-quality violations for a transaction."""
    errors = []

    if not transaction.get("transaction_id"):
        errors.append("missing_transaction_id")

    if not transaction.get("customer_id"):
        errors.append("missing_customer_id")

    if transaction.get("transaction_ts") is None:
        errors.append("missing_transaction_ts")

    amount = transaction.get("amount")
    if amount is None or Decimal(str(amount)) < 0:
        errors.append("invalid_amount")

    status = transaction.get("status")
    normalized_status = status.strip().upper() if isinstance(status, str) else ""

    if normalized_status not in VALID_STATUSES:
        errors.append("invalid_status")

    return errors


def test_valid_transaction_passes():
    transaction = {
        "transaction_id": "TXN-001",
        "customer_id": "C00001",
        "transaction_ts": "2026-10-28T10:00:00",
        "amount": "125.50",
        "status": "SETTLED",
    }

    assert validate_transaction(transaction) == []


def test_missing_transaction_id_is_detected():
    transaction = {
        "customer_id": "C00001",
        "transaction_ts": "2026-10-28T10:00:00",
        "amount": "125.50",
        "status": "SETTLED",
    }

    assert "missing_transaction_id" in validate_transaction(transaction)


def test_negative_amount_is_detected():
    transaction = {
        "transaction_id": "TXN-002",
        "customer_id": "C00002",
        "transaction_ts": "2026-10-28T10:00:00",
        "amount": "-10.00",
        "status": "SETTLED",
    }

    assert "invalid_amount" in validate_transaction(transaction)


def test_status_is_normalized():
    transaction = {
        "transaction_id": "TXN-003",
        "customer_id": "C00003",
        "transaction_ts": "2026-10-28T10:00:00",
        "amount": "50",
        "status": " declined ",
    }

    assert validate_transaction(transaction) == []


def test_invalid_status_is_detected():
    transaction = {
        "transaction_id": "TXN-004",
        "customer_id": "C00004",
        "transaction_ts": "2026-10-28T10:00:00",
        "amount": "50",
        "status": "PENDING",
    }

    assert "invalid_status" in validate_transaction(transaction)
