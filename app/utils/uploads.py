# app/utils/uploads.py
"""
Shared file-upload handling.

Deliberately built on top of the existing Media model (filename,
mime_type, file_size, url, folder, uploaded_by) rather than a new
LeadDocument/ProjectFile table, so every upload surface in the app
(lead proposals, project files, anything added later) shares one storage
path and one queryable record instead of each feature inventing its own.
"""
import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import Media


class UploadError(Exception):
    """Raised for any rejected upload; callers catch this and surface a
    form error rather than a 500."""


def _extension(filename):
    if "." not in filename:
        return None
    return filename.rsplit(".", 1)[1].lower()


def _allowed(filename):
    ext = _extension(filename)
    if not ext:
        return False
    return ext in current_app.config.get("ALLOWED_UPLOAD_EXTENSIONS", set())


def save_upload(file_storage, folder="general", uploaded_by=None):
    """
    Validates and persists an uploaded werkzeug FileStorage.

    Writes the file to UPLOAD_FOLDER/<folder>/<random-name>.<ext> and stages
    (adds, does not commit) a Media row pointing at it. Returns the Media
    instance. Caller commits as part of its own transaction, so a saved
    file always has a matching database record and vice versa.

    Raises UploadError for anything invalid: no file, disallowed extension,
    or an unusable filename.
    """
    if not file_storage or not file_storage.filename:
        raise UploadError("No file was provided.")

    if not _allowed(file_storage.filename):
        allowed = ", ".join(sorted(current_app.config.get("ALLOWED_UPLOAD_EXTENSIONS", set())))
        raise UploadError(f"That file type isn't supported. Allowed types: {allowed}.")

    original_filename = secure_filename(file_storage.filename)
    if not original_filename:
        raise UploadError("That filename isn't valid.")

    ext = _extension(original_filename)
    stored_filename = f"{uuid.uuid4().hex}.{ext}"

    target_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], folder)
    os.makedirs(target_dir, exist_ok=True)

    absolute_path = os.path.join(target_dir, stored_filename)
    file_storage.save(absolute_path)

    file_size = os.path.getsize(absolute_path)
    mime_type = file_storage.mimetype or "application/octet-stream"

    # Relative to the static folder, so templates can do
    # url_for('static', filename=media.url) directly.
    relative_url = f"uploads/{folder}/{stored_filename}"

    media = Media(
        filename=stored_filename,
        original_filename=original_filename,
        mime_type=mime_type,
        file_size=file_size,
        url=relative_url,
        folder=folder,
        uploaded_by=uploaded_by,
    )
    db.session.add(media)
    return media