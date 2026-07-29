# app/utils/decorators.py
from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def role_required(*roles):
    """
    Gate a view to specific User.role values, e.g.
    @role_required(ROLE_ADMIN, ROLE_CONSULTANT).

    Wraps login_required internally so an anonymous request is redirected
    to the login page (Flask-Login's normal behavior) rather than getting
    a bare 403 with no way forward; an authenticated user with the wrong
    role gets the 403.
    """

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator