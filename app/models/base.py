# app/models/base.py
"""
Shared model primitives (UUID PK helper, timestamp mixin).

Split out of app/models/__init__.py so new CRM models (app/models/crm.py)
can import these without creating a circular import: __init__.py imports
from crm.py, so crm.py cannot import back from __init__.py.
"""
import uuid
from datetime import datetime, timezone

from app.extensions import db


def generate_uuid():
    return str(uuid.uuid4())


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )