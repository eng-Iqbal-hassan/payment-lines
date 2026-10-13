import csv
from typing import List

from alert import Alert
from payment_recoinciler import Reconciler
from statement import Statement

ACCOUNT = "4521"  # statements.csv has no account column


def load_alerts(path: str) -> List[Alert]:
    with open(path, newline="") as f:
        return [Alert.from_row(row) for row in csv.DictReader(f)]


def load_statements(path: str, account: str) -> List[Statement]:
    with open(path, newline="") as f:
        return [Statement.from_row(row, account) for row in csv.DictReader(f)]


if __name__ == "__main__":
    alerts = load_alerts("alerts.csv")
    statements = load_statements("statements.csv", ACCOUNT)

    print(Reconciler(alerts, statements).summary())
