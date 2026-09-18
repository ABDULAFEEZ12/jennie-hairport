"""
Thin client for Squad's hosted checkout (Standard Checkout / "Payment Modal") API.

This deliberately uses Squad's *hosted redirect* flow only — we send the customer to
squad's own payment page (`checkout_url`) rather than collecting card numbers on this
server. That keeps this codebase out of PCI-DSS card-data scope entirely, which matters
far more than saving the user a redirect hop.

Endpoints/fields below are taken from Squad's current public docs (docs.squadco.com,
"Direct API Integration" / hosted checkout section) as of this writing. Payment provider
APIs do change — if a real transaction ever comes back with an unexpected shape, check
https://docs.squadco.com before assuming this client is wrong.
"""

import requests

SANDBOX_BASE_URL = "https://sandbox-api-d.squadco.com"
LIVE_BASE_URL = "https://api-d.squadco.com"


class SquadError(Exception):
    """Raised when Squad's API returns an error or an unexpected response shape."""


def _base_url(env: str) -> str:
    return LIVE_BASE_URL if env == "live" else SANDBOX_BASE_URL


def _headers(secret_key: str) -> dict:
    return {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }


def initiate_transaction(
    *,
    secret_key: str,
    env: str,
    amount_naira: int,
    email: str,
    transaction_ref: str,
    callback_url: str,
    customer_name: str = "",
    timeout: int = 15,
) -> str:
    """
    Starts a Squad hosted-checkout transaction and returns the checkout_url to redirect
    the customer to. Raises SquadError on any failure (network, bad keys, bad response).
    """
    url = f"{_base_url(env)}/transaction/initiate"
    payload = {
        "amount": int(round(amount_naira)) * 100,  # Squad expects kobo
        "email": email,
        "currency": "NGN",
        "initiate_type": "inline",
        "transaction_ref": transaction_ref,
        "callback_url": callback_url,
        "customer_name": customer_name,
    }

    try:
        response = requests.post(url, json=payload, headers=_headers(secret_key), timeout=timeout)
    except requests.RequestException as exc:
        raise SquadError(f"Could not reach Squad: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise SquadError(f"Squad returned a non-JSON response (status {response.status_code})") from exc

    if response.status_code >= 400 or not data.get("success"):
        message = data.get("message", "Unknown error from Squad")
        raise SquadError(f"Squad rejected the transaction: {message}")

    checkout_url = (data.get("data") or {}).get("checkout_url")
    if not checkout_url:
        raise SquadError("Squad's response did not include a checkout_url")

    return checkout_url


def verify_transaction(*, secret_key: str, env: str, transaction_ref: str, timeout: int = 15) -> dict:
    """
    Confirms the real, final status of a transaction directly with Squad — never trust a
    browser redirect's query string alone as proof of payment; always re-check server-side.

    Returns a dict with at least: status ("success" | "failed" | "abandoned" | "pending"),
    amount_kobo, raw (the full Squad response) for logging/debugging.
    """
    url = f"{_base_url(env)}/transaction/verify/{transaction_ref}"

    try:
        response = requests.get(url, headers=_headers(secret_key), timeout=timeout)
    except requests.RequestException as exc:
        raise SquadError(f"Could not reach Squad: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise SquadError(f"Squad returned a non-JSON response (status {response.status_code})") from exc

    if response.status_code >= 400 or not data.get("success"):
        message = data.get("message", "Unknown error from Squad")
        raise SquadError(f"Could not verify transaction: {message}")

    inner = data.get("data") or {}
    squad_status = (inner.get("transaction_status") or "").strip().lower()
    status_map = {
        "success": "success",
        "failed": "failed",
        "abandoned": "abandoned",
        "pending": "pending",
    }

    return {
        "status": status_map.get(squad_status, "pending"),
        "amount_kobo": inner.get("transaction_amount"),
        "raw": data,
    }
