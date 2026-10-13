from datetime import datetime
from typing import Dict

from notice import Notice


class Statement(Notice):
    """One line of the bank statement, built from one row of statements.csv."""

    def __init__(self, balance: float, **notice_fields):
        super().__init__(**notice_fields)
        self._balance = balance

    @classmethod
    def from_row(cls, row: Dict[str, str], account: str) -> "Statement":
        # statements.csv has no account column, so the caller passes it in.
        debit, credit = row["debit"], row["credit"]
        if bool(debit) == bool(credit):
            raise ValueError(f"{row['id']}: exactly one of debit/credit must be filled")

        return cls(
            id=row["id"],
            source="statement",
            account=account,
            direction="out" if debit else "in",
            amount=float(debit or credit),
            merchant=row["description"],
            # The statement only gives a date, so the time is midnight.
            occurred_at=datetime.strptime(row["date"], "%Y-%m-%d"),
            raw=tuple(row.items()),
            balance=float(row["balance"]),
        )
