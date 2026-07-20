# app/blueprints/public/__init__.py

from flask import Blueprint

public_bp = Blueprint(
    "public",
    __name__,
    template_folder=None,
    static_folder=None,
    url_prefix="",
)