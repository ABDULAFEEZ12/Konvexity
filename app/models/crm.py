# app/models/crm.py
"""
CRM foundation models (Phase 1).

Kept in its own module rather than growing app/models/__init__.py further,
so the CRM subsystem stays easy to find and touch without risking the
existing marketing-site models. Re-exported from app.models at the bottom
of app/models/__init__.py, so `from app.models import ActivityLog` works
exactly like every other model in this project.
"""
from datetime import datetime, timezone

from app.extensions import db
from app.models.base import TimestampMixin, generate_uuid

# Reuses the existing User.role column rather than introducing a separate
# Admin table. "learner" already exists as the default for the public-facing
# side of the app; "consultant" and "admin" are the two CRM-facing roles.
ROLE_LEARNER = "learner"
ROLE_CONSULTANT = "consultant"
ROLE_ADMIN = "admin"

STAFF_ROLES = (ROLE_CONSULTANT, ROLE_ADMIN)


class SoftDeleteMixin:
    """Shared soft-delete behavior for CRM records that need an "archived"
    state distinct from a hard delete (leads, projects). Records with
    deleted_at set should be excluded from default list queries by the
    view layer, not by a global query filter, so admins can still look
    up archived records explicitly."""

    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def soft_delete(self):
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.deleted_at = None


class ActivityLog(TimestampMixin, db.Model):
    """Append-only audit trail. entity_type/entity_id are kept generic
    (rather than a separate log table per entity) so logins, lead status
    changes, booking updates, and project notes all share one timeline
    that a detail page can query by (entity_type, entity_id)."""

    __tablename__ = "activity_logs"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    entity_type = db.Column(db.String(50), nullable=False, index=True)
    entity_id = db.Column(db.String(36), nullable=False, index=True)
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    meta = db.Column(db.JSON, nullable=True, default=dict)

    actor_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    actor = db.relationship("User")

    __table_args__ = (
        db.Index("ix_activity_logs_entity", "entity_type", "entity_id"),
    )

    def __repr__(self):
        return f"<ActivityLog {self.entity_type}:{self.entity_id} {self.action}>"

    @staticmethod
    def record(entity_type, entity_id, action, actor_id=None, description=None, meta=None):
        """Builds and stages (adds, does not commit) a log row. Callers
        commit it as part of the same transaction as the change it
        describes, so a log entry is never left dangling if the rest of
        the operation fails."""
        entry = ActivityLog(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            actor_id=actor_id,
            description=description,
            meta=meta or {},
        )
        db.session.add(entry)
        return entry


class IdentifierSequence(db.Model):
    """Backing counter for human-readable IDs like KVX-2026-00124 or
    KVX-MTG-2026-00031. One row per (scope, period); row-level locking in
    app/utils/identifiers.py prevents two concurrent submissions in the
    same period from ever getting the same number, which a naive
    COUNT(*) + 1 approach would not guarantee under load."""

    __tablename__ = "identifier_sequences"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    scope = db.Column(db.String(100), nullable=False, index=True)
    period = db.Column(db.String(20), nullable=False)
    last_value = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (
        db.UniqueConstraint("scope", "period", name="uq_identifier_sequences_scope_period"),
    )

    def __repr__(self):
        return f"<IdentifierSequence {self.scope}:{self.period}={self.last_value}>"


# --- "Work With Konvexity" service options ------------------------------
SERVICE_CHOICES = [
    ("ai_strategy", "AI Strategy"),
    ("digital_transformation", "Digital Transformation"),
    ("software_development", "Software Development"),
    ("web_development", "Web Development"),
    ("mobile_development", "Mobile Development"),
    ("cloud_infrastructure", "Cloud Infrastructure"),
    ("product_design", "Product Design"),
    ("branding", "Branding"),
    ("business_consulting", "Business Consulting"),
    ("startup_advisory", "Startup Advisory"),
    ("custom_solution", "Custom Solution"),
]

LEAD_STATUS_CHOICES = [
    ("new", "New"),
    ("contacted", "Contacted"),
    ("proposal_sent", "Proposal Sent"),
    ("negotiation", "Negotiation"),
    ("won", "Won"),
    ("lost", "Lost"),
    ("archived", "Archived"),
]


class Lead(TimestampMixin, SoftDeleteMixin, db.Model):
    """A "Work With Konvexity" submission. request_id is the
    human-readable KVX-2026-00124 style identifier shown to the visitor
    on submission and used by the admin team to reference it."""

    __tablename__ = "leads"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    request_id = db.Column(db.String(30), unique=True, nullable=False, index=True)

    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(300), nullable=False, index=True)
    whatsapp_number = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(300), nullable=True)
    job_title = db.Column(db.String(200), nullable=True)
    country = db.Column(db.String(100), nullable=True)

    service_interest = db.Column(db.String(50), nullable=False, index=True)
    message = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(30), nullable=False, default="new", index=True)

    assigned_consultant_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    assigned_consultant = db.relationship("User", foreign_keys=[assigned_consultant_id])

    def __repr__(self):
        return f"<Lead {self.request_id} {self.full_name}>"

    @property
    def service_label(self):
        return dict(SERVICE_CHOICES).get(self.service_interest, self.service_interest)

    @property
    def status_label(self):
        return dict(LEAD_STATUS_CHOICES).get(self.status, self.status)


# --- "Schedule a Consultation" platform options -------------------------
MEETING_PLATFORM_CHOICES = [
    ("google_meet", "Google Meet"),
    ("zoom", "Zoom"),
    ("phone", "Phone Call"),
]

BOOKING_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]


class ConsultationBooking(TimestampMixin, SoftDeleteMixin, db.Model):
    """A "Schedule a Consultation" submission. booking_id is the
    human-readable KVX-MTG-2026-00031 style identifier. preferred_date and
    preferred_time are visitor-stated preferences, not a confirmed
    slot: an admin still approves/reschedules against real availability,
    since no calendar/availability engine exists yet."""

    __tablename__ = "consultation_bookings"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    booking_id = db.Column(db.String(30), unique=True, nullable=False, index=True)

    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(300), nullable=False, index=True)
    whatsapp_number = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(300), nullable=True)

    meeting_goal = db.Column(db.Text, nullable=True)
    preferred_platform = db.Column(db.String(30), nullable=False)
    preferred_date = db.Column(db.String(50), nullable=True)
    preferred_time = db.Column(db.String(50), nullable=True)

    status = db.Column(db.String(30), nullable=False, default="pending", index=True)

    assigned_consultant_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    assigned_consultant = db.relationship("User", foreign_keys=[assigned_consultant_id])

    def __repr__(self):
        return f"<ConsultationBooking {self.booking_id} {self.full_name}>"

    @property
    def platform_label(self):
        return dict(MEETING_PLATFORM_CHOICES).get(self.preferred_platform, self.preferred_platform)

    @property
    def status_label(self):
        return dict(BOOKING_STATUS_CHOICES).get(self.status, self.status)