from alert import Alert
from notice import Notice
from statement import Statement

MAX_MINUTES_APART = 5  # SMS and email for one payment arrive within this many minutes
MAX_DAYS_LATE = 2      # how many days after the alert the statement line may appear


# --- Any two notices (alert <-> alert or alert <-> statement) ---

def same_direction(a: Notice, b: Notice) -> bool:
    return a._direction == b._direction


def same_amount(a: Notice, b: Notice) -> bool:
    # Compare in paisa so float rounding (e.g. 0.1 + 0.2) can't cause a miss.
    return round(a._amount * 100) == round(b._amount * 100)


def merchant_match(a: Notice, b: Notice) -> bool:
    # One name inside the other: "FOODPANDA" matches "POS FOODPANDA PK KARACHI".
    x, y = a._merchant.upper().strip(), b._merchant.upper().strip()
    return bool(x and y) and (x in y or y in x)


# --- Alert <-> alert (is it the same payment reported twice?) ---

def close_in_time(a: Alert, b: Alert) -> bool:
    gap = abs((a._occurred_at - b._occurred_at).total_seconds())
    return gap <= MAX_MINUTES_APART * 60


# --- Alert <-> statement (did the payment really happen?) ---

def within_days(alert: Alert, statement: Statement) -> bool:
    # Compare dates only: the statement has no time of day.
    days = (statement._occurred_at.date() - alert._occurred_at.date()).days
    return 0 <= days <= MAX_DAYS_LATE
