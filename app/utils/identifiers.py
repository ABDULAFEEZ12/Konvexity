# app/utils/identifiers.py
"""
Human-readable identifier generation for leads, bookings, and any future
scope that needs one (e.g. "KVX-2026-00124").

Backed by IdentifierSequence with SELECT ... FOR UPDATE, so two concurrent
submissions in the same period can never receive the same number. A naive
"COUNT(*) + 1" approach looks correct in testing and then collides under
real concurrent traffic, which is the exact kind of bug this avoids.

Note: SQLite (the local dev default in config.py) does not support row-level
locking the way Postgres does; SQLAlchemy's SQLite dialect treats
with_for_update() as a no-op rather than raising, and SQLite's own
file-level write lock serializes writes anyway, so this is still correct in
development. In production (Postgres, per config.py), the row lock is real.
"""
from datetime import datetime, timezone

from app.extensions import db
from app.models import IdentifierSequence


def _current_period():
    return str(datetime.now(timezone.utc).year)


def next_identifier(scope, prefix, pad=5, period=None):
    """
    Returns e.g. "KVX-2026-00124" for scope="lead", prefix="KVX", pad=5.
    Caller controls the surrounding transaction; this only flushes (not
    commits), so the identifier and the record it belongs to succeed or
    fail together.
    """
    period = period or _current_period()

    row = (
        db.session.query(IdentifierSequence)
        .filter_by(scope=scope, period=period)
        .with_for_update()
        .first()
    )

    if row is None:
        row = IdentifierSequence(scope=scope, period=period, last_value=0)
        db.session.add(row)
        db.session.flush()
        row = (
            db.session.query(IdentifierSequence)
            .filter_by(scope=scope, period=period)
            .with_for_update()
            .first()
        )

    row.last_value += 1
    db.session.flush()

    return f"{prefix}-{period}-{str(row.last_value).zfill(pad)}"