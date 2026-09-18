from datetime import datetime, timezone

from flask import Blueprint, current_app, render_template, request

from ... import data
from ...squad import verify_transaction, SquadError

payments_bp = Blueprint("payments", __name__)


@payments_bp.route("/callback")
def callback():
    """
    Squad redirects the customer's browser here after a payment attempt. We ignore
    whatever query params Squad itself appends and instead rely on `ref`, which we baked
    into the callback_url ourselves when initiating — it's guaranteed to be our own order
    reference. The actual payment result is never trusted from the URL; it's always
    re-confirmed with Squad's server-to-server verify endpoint below.
    """
    reference = request.args.get("ref") or request.args.get("transaction_ref") or request.args.get("reference")
    order = data.get_order_by_reference(reference) if reference else None

    if not order:
        return render_template("payment_result.html", order=None, status="not_found"), 404

    try:
        result = verify_transaction(
            secret_key=current_app.config["SQUAD_SECRET_KEY"],
            env=current_app.config["SQUAD_ENV"],
            transaction_ref=order.reference,
        )
        status = result["status"]
    except SquadError as exc:
        current_app.logger.error("Squad verify failed for order %s: %s", order.reference, exc)
        status = "pending"

    if status == "success" and order.get("payment_status") != "success":
        data.update_order_status(order.reference, "success", paid_at=datetime.now(timezone.utc))
        order = data.get_order_by_reference(order.reference)
    elif status in ("failed", "abandoned"):
        data.update_order_status(order.reference, status)
        order = data.get_order_by_reference(order.reference)

    return render_template("payment_result.html", order=order, status=order.get("payment_status"))
