# app/blueprints/admin/routes.py
from datetime import datetime, timezone

from flask import abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.blueprints.admin import admin_bp
from app.blueprints.admin.forms import AdminLoginForm, ChangePasswordForm
from app.extensions import db, limiter
from app.models import (
    Application,
    ConsultationBooking,
    ContactInquiry,
    Lead,
    User,
)
from app.models.crm import (
    BOOKING_STATUS_CHOICES,
    LEAD_STATUS_CHOICES,
    STAFF_ROLES,
    ActivityLog,
)


@admin_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    if current_user.is_authenticated and current_user.role in STAFF_ROLES:
        return redirect(url_for("admin.dashboard"))

    form = AdminLoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = db.session.query(User).filter_by(email=email).first()

        valid = (
            user is not None
            and user.is_active
            and user.role in STAFF_ROLES
            and user.check_password(form.password.data)
        )

        if not valid:
            flash("Those credentials don't match an admin account.", "error")
        else:
            login_user(user, remember=form.remember.data)
            user.last_login = datetime.now(timezone.utc)
            ActivityLog.record(
                entity_type="user",
                entity_id=user.id,
                action="login",
                actor_id=user.id,
                description=f"{user.email} signed in to the admin dashboard.",
            )
            db.session.commit()

            next_url = request.args.get("next")
            return redirect(next_url or url_for("admin.dashboard"))

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
def logout():
    ActivityLog.record(
        entity_type="user",
        entity_id=current_user.id,
        action="logout",
        actor_id=current_user.id,
        description=f"{current_user.email} signed out.",
    )
    db.session.commit()
    logout_user()
    flash("You have been signed out.", "success")
    return redirect(url_for("admin.login"))


@admin_bp.before_request
def require_staff():
    """Applies to every route in this blueprint. admin.login is exempt
    (it has to be reachable while anonymous), everything else requires an
    authenticated session and a staff role. Deliberately not using the
    @login_required decorator here: stacking it directly on a
    before_request function runs it before the endpoint-name check below,
    which would redirect away from the login page itself."""
    if request.endpoint == "admin.login":
        return None
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    if current_user.role not in STAFF_ROLES:
        abort(403)


@admin_bp.route("/account", methods=["GET", "POST"])
def account():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Your current password is incorrect.", "error")
        else:
            current_user.set_password(form.new_password.data)
            ActivityLog.record(
                entity_type="user",
                entity_id=current_user.id,
                action="password_changed",
                actor_id=current_user.id,
                description=f"{current_user.email} changed their password.",
            )
            db.session.commit()
            flash("Your password has been updated.", "success")
            return redirect(url_for("admin.account"))

    return render_template("admin/account.html", form=form)


@admin_bp.route("/")
def dashboard():
    stats = {
        "total_leads": db.session.query(Lead).filter(Lead.deleted_at.is_(None)).count(),
        "new_leads": db.session.query(Lead).filter_by(status="new").filter(Lead.deleted_at.is_(None)).count(),
        "total_bookings": db.session.query(ConsultationBooking).filter(ConsultationBooking.deleted_at.is_(None)).count(),
        "pending_bookings": db.session.query(ConsultationBooking).filter_by(status="pending").filter(ConsultationBooking.deleted_at.is_(None)).count(),
        "total_inquiries": db.session.query(ContactInquiry).count(),
        "unread_inquiries": db.session.query(ContactInquiry).filter_by(is_read=False).count(),
        "total_applications": db.session.query(Application).count(),
        "pending_applications": db.session.query(Application).filter_by(status="pending").count(),
    }

    recent_activity = (
        db.session.query(ActivityLog)
        .order_by(ActivityLog.created_at.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_activity=recent_activity,
    )


# --- Leads -------------------------------------------------------------

@admin_bp.route("/leads")
def leads_list():
    query = db.session.query(Lead).filter(Lead.deleted_at.is_(None))

    search = request.args.get("q", "").strip()
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Lead.full_name.ilike(like),
                Lead.email.ilike(like),
                Lead.company.ilike(like),
                Lead.request_id.ilike(like),
            )
        )

    status_filter = request.args.get("status", "").strip()
    if status_filter:
        query = query.filter_by(status=status_filter)

    page = request.args.get("page", 1, type=int)
    pagination = query.order_by(Lead.created_at.desc()).paginate(page=page, per_page=20, error_out=False)

    return render_template(
        "admin/leads_list.html",
        pagination=pagination,
        leads=pagination.items,
        search=search,
        status_filter=status_filter,
        status_choices=LEAD_STATUS_CHOICES,
    )


@admin_bp.route("/leads/<lead_id>")
def lead_detail(lead_id):
    lead = db.session.get(Lead, lead_id)
    if lead is None:
        abort(404)

    consultants = db.session.query(User).filter(User.role.in_(STAFF_ROLES)).order_by(User.first_name).all()
    history = (
        db.session.query(ActivityLog)
        .filter_by(entity_type="lead", entity_id=lead.id)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )

    return render_template(
        "admin/lead_detail.html",
        lead=lead,
        consultants=consultants,
        history=history,
        status_choices=LEAD_STATUS_CHOICES,
    )


@admin_bp.route("/leads/<lead_id>/status", methods=["POST"])
def lead_update_status(lead_id):
    lead = db.session.get(Lead, lead_id)
    if lead is None:
        abort(404)

    new_status = request.form.get("status", "").strip()
    valid_statuses = {value for value, _ in LEAD_STATUS_CHOICES}
    if new_status not in valid_statuses:
        flash("That isn't a valid status.", "error")
        return redirect(url_for("admin.lead_detail", lead_id=lead.id))

    old_status = lead.status
    lead.status = new_status
    ActivityLog.record(
        entity_type="lead",
        entity_id=lead.id,
        action="status_changed",
        actor_id=current_user.id,
        description=f"Status changed from {old_status} to {new_status}.",
    )
    db.session.commit()
    flash("Lead status updated.", "success")
    return redirect(url_for("admin.lead_detail", lead_id=lead.id))


@admin_bp.route("/leads/<lead_id>/assign", methods=["POST"])
def lead_assign(lead_id):
    lead = db.session.get(Lead, lead_id)
    if lead is None:
        abort(404)

    consultant_id = request.form.get("consultant_id", "").strip() or None
    lead.assigned_consultant_id = consultant_id

    consultant = db.session.get(User, consultant_id) if consultant_id else None
    description = f"Assigned to {consultant.email}." if consultant else "Unassigned."
    ActivityLog.record(
        entity_type="lead",
        entity_id=lead.id,
        action="assigned",
        actor_id=current_user.id,
        description=description,
    )
    db.session.commit()
    flash("Assignment updated.", "success")
    return redirect(url_for("admin.lead_detail", lead_id=lead.id))


@admin_bp.route("/leads/<lead_id>/note", methods=["POST"])
def lead_add_note(lead_id):
    lead = db.session.get(Lead, lead_id)
    if lead is None:
        abort(404)

    note = request.form.get("note", "").strip()
    if not note:
        flash("Note can't be empty.", "error")
        return redirect(url_for("admin.lead_detail", lead_id=lead.id))

    ActivityLog.record(
        entity_type="lead",
        entity_id=lead.id,
        action="note",
        actor_id=current_user.id,
        description=note,
    )
    db.session.commit()
    flash("Note added.", "success")
    return redirect(url_for("admin.lead_detail", lead_id=lead.id))


@admin_bp.route("/leads/<lead_id>/archive", methods=["POST"])
def lead_archive(lead_id):
    lead = db.session.get(Lead, lead_id)
    if lead is None:
        abort(404)

    lead.soft_delete()
    ActivityLog.record(
        entity_type="lead",
        entity_id=lead.id,
        action="archived",
        actor_id=current_user.id,
        description="Lead archived.",
    )
    db.session.commit()
    flash("Lead archived.", "success")
    return redirect(url_for("admin.leads_list"))


# --- Consultation bookings ----------------------------------------------

@admin_bp.route("/bookings")
def bookings_list():
    query = db.session.query(ConsultationBooking).filter(ConsultationBooking.deleted_at.is_(None))

    search = request.args.get("q", "").strip()
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                ConsultationBooking.full_name.ilike(like),
                ConsultationBooking.email.ilike(like),
                ConsultationBooking.booking_id.ilike(like),
            )
        )

    status_filter = request.args.get("status", "").strip()
    if status_filter:
        query = query.filter_by(status=status_filter)

    page = request.args.get("page", 1, type=int)
    pagination = query.order_by(ConsultationBooking.created_at.desc()).paginate(page=page, per_page=20, error_out=False)

    return render_template(
        "admin/bookings_list.html",
        pagination=pagination,
        bookings=pagination.items,
        search=search,
        status_filter=status_filter,
        status_choices=BOOKING_STATUS_CHOICES,
    )


@admin_bp.route("/bookings/<booking_id>")
def booking_detail(booking_id):
    booking = db.session.get(ConsultationBooking, booking_id)
    if booking is None:
        abort(404)

    history = (
        db.session.query(ActivityLog)
        .filter_by(entity_type="consultation_booking", entity_id=booking.id)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )

    return render_template(
        "admin/booking_detail.html",
        booking=booking,
        history=history,
        status_choices=BOOKING_STATUS_CHOICES,
    )


@admin_bp.route("/bookings/<booking_id>/status", methods=["POST"])
def booking_update_status(booking_id):
    booking = db.session.get(ConsultationBooking, booking_id)
    if booking is None:
        abort(404)

    new_status = request.form.get("status", "").strip()
    valid_statuses = {value for value, _ in BOOKING_STATUS_CHOICES}
    if new_status not in valid_statuses:
        flash("That isn't a valid status.", "error")
        return redirect(url_for("admin.booking_detail", booking_id=booking.id))

    old_status = booking.status
    booking.status = new_status
    ActivityLog.record(
        entity_type="consultation_booking",
        entity_id=booking.id,
        action="status_changed",
        actor_id=current_user.id,
        description=f"Status changed from {old_status} to {new_status}.",
    )
    db.session.commit()
    flash("Booking status updated.", "success")
    return redirect(url_for("admin.booking_detail", booking_id=booking.id))
