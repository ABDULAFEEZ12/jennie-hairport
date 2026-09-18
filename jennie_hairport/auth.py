import hmac
from functools import wraps

from flask import current_app, redirect, session, url_for


def check_admin_password(password: str) -> bool:
    expected = current_app.config["ADMIN_PASSWORD"]
    return hmac.compare_digest(password or "", expected)


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)

    return wrapped
