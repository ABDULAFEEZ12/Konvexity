from flask import Blueprint

public_bp = Blueprint(
    "public",
    __name__,
    template_folder="templates/public",
    static_folder="static",
    url_prefix="",
)