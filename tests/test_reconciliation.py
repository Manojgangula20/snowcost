
def reconcile_counts(core_count: int, mart_count: int) -> bool:
    """Return whether a mart's transaction count matches the core count."""
    return core_count == mart_count


def test_matching_counts_pass():
    assert reconcile_counts(10_000, 10_000) is True


def test_mismatched_counts_fail():
    assert reconcile_counts(10_000, 9_999) is False


def test_empty_counts_match():
    assert reconcile_counts(0, 0) is True


def test_mart_with_extra_rows_fails():
    assert reconcile_counts(10_000, 10_001) is False
