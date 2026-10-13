from datetime import datetime
from typing import Tuple

DIRECTIONS = ("in", "out")


class Notice:
    """One message from one source, exactly as received.

    Read-only by convention: every field is stored in an underscore
    attribute (e.g. notice._id) that is read directly but never assigned
    after __init__ (ground rule 1).
    Alert and Statement both inherit from this, so every notice has the
    same fields, whichever file it came from.
    """

    def __init__(
        self,
        id: str,
        source: str,             # 'sms', 'email' or 'statement'
        account: str,
        direction: str,          # 'in' or 'out'
        amount: float,
        merchant: str,           # alert's merchant / statement's description
        occurred_at: datetime,   # when the source says it happened
        raw: Tuple[Tuple[str, str], ...],  # original CSV row, unchanged
    ):
        if direction not in DIRECTIONS:
            raise ValueError(f"{id}: direction must be 'in' or 'out', got {direction!r}")
        if amount <= 0:
            raise ValueError(f"{id}: amount must be positive, got {amount}")

        self._id = id
        self._source = source
        self._account = account
        self._direction = direction
        self._amount = amount
        self._merchant = merchant
        self._occurred_at = occurred_at
        self._raw = raw

