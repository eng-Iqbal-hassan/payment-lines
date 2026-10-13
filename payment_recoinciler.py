from typing import Dict, List, Optional, Tuple

from alert import Alert
from statement import Statement
from utils import close_in_time, merchant_match, same_amount, same_direction, within_days


def same_payment(a: Alert, b: Alert) -> bool:
    # Amount is not checked: SMS and email may disagree (flagged later).
    return same_direction(a, b) and close_in_time(a, b) and merchant_match(a, b)


def alert_matches_line(alert: Alert, line: Statement) -> bool:
    return (same_direction(alert, line) and same_amount(alert, line)
            and within_days(alert, line) and merchant_match(alert, line))


def amounts_differ(group: List[Alert]) -> bool:
    return any(not same_amount(group[0], a) for a in group[1:])


class Reconciler:
    """Matches a list of alerts against a list of statement lines."""

    def __init__(self, alerts: List[Alert], statements: List[Statement]):
        self._alerts = alerts
        self._statements = statements

    def _group_alerts(self) -> List[List[Alert]]:
        """Step 1: put alerts that report the same payment into one group."""
        groups: List[List[Alert]] = []
        for alert in sorted(self._alerts, key=lambda a: a._occurred_at):
            for group in groups:
                if same_payment(group[0], alert):
                    group.append(alert)
                    break
            else:
                groups.append([alert])
        return groups

    def _match_groups(
        self, groups: List[List[Alert]]
    ) -> List[Tuple[List[Alert], Optional[Statement]]]:
        """Step 2: give each group the earliest unused statement line that matches.

        A group matches if any one of its alerts matches, so a flagged group
        still finds its line through the alert with the right amount.
        Each line is used once, so two equal payments get two different lines.
        """
        used = set()
        matches = []
        for group in groups:
            found = None
            for line in sorted(self._statements, key=lambda s: s._occurred_at):
                if line._id in used:
                    continue
                if any(alert_matches_line(a, line) for a in group):
                    found = line
                    used.add(line._id)
                    break
            matches.append((group, found))
        return matches

    def reconcile(self) -> Dict[str, list]:
        """Step 3: run steps 1 and 2, then sort every result into one bucket."""
        matches = self._match_groups(self._group_alerts())

        buckets: Dict[str, list] = {
            "matched": [],         # (group, line): alerts and bank agree
            "flagged": [],         # (group, line): matched, but the alerts disagree on amount
            "alert_only": [],      # group: no bank line for this payment
            "statement_only": [],  # line: bank charged, but no alert came
        }
        used = set()
        for group, line in matches:
            if line is None:
                buckets["alert_only"].append(group)
                continue
            used.add(line._id)
            if amounts_differ(group):
                buckets["flagged"].append((group, line))
            else:
                buckets["matched"].append((group, line))

        result = []
        for s in self._statements:
            if s._id not in used:
                result.append(s)
        buckets["statement_only"] = result
        return buckets

    def summary(self) -> str:
        """Step 4: the buckets as a readable report."""
        b = self.reconcile()

        def ids(group: List[Alert]) -> str:
            return "+".join(a._id for a in group)

        lines = [f"MATCHED ({len(b['matched'])})"]
        for group, line in b["matched"]:
            lines.append(f"  {ids(group):8} -> {line._id:4} {line._amount:>10.2f}  {line._merchant}")

        lines.append(f"FLAGGED: alerts disagree on amount ({len(b['flagged'])})")
        for group, line in b["flagged"]:
            said = ", ".join(f"{a._id}={a._amount:.2f}" for a in group)
            lines.append(f"  {ids(group):8} -> {line._id:4} {line._amount:>10.2f}  {line._merchant}  [{said}]")

        lines.append(f"ALERT ONLY: no bank line ({len(b['alert_only'])})")
        for group in b["alert_only"]:
            a = group[0]
            lines.append(f"  {ids(group):8}         {a._amount:>10.2f}  {a._merchant}")

        lines.append(f"STATEMENT ONLY: no alert ({len(b['statement_only'])})")
        for s in b["statement_only"]:
            lines.append(f"  {'':8}    {s._id:4} {s._amount:>10.2f}  {s._merchant}")

        return "\n".join(lines)
