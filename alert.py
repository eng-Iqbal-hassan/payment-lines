from datetime import datetime
from typing import Dict, Optional

from notice import Notice


class Alert(Notice):
    """An SMS or email alert, built from one row of alerts.csv."""

    def __init__(self, ref: Optional[str], **notice_fields):
        super().__init__(**notice_fields)
        self._ref = ref

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> "Alert":
        return cls(
            id=row["id"],
            source=row["source"],
            account=row["account"],
            direction=row["direction"],
            amount=float(row["amount"]),
            merchant=row["merchant"],
            occurred_at=datetime.strptime(row["received_at"], "%Y-%m-%d %H:%M"),
            raw=tuple(row.items()),
            ref=row["ref"] or None,
        )
