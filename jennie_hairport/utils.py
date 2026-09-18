import re
import secrets
from urllib.parse import quote

SITE = {
    "name": "Jennie_Hairport",
    "tagline": "Premium Hair, Fair Prices.",
    "description": (
        "Vietnam bone-straight hair, wigs, bundles and closures — direct sourcing, "
        "honest pricing."
    ),
    "whatsapp_number": "2349034160178",
    "whatsapp_display": "+234 903 416 0178",
    "instagram_handle": "hairportbyjennie",
    "instagram_url": "https://instagram.com/hairportbyjennie",
    "tiktok_handle": "Jennie_hairport",
    "tiktok_url": "https://www.tiktok.com/@jennie_hairport",
    "address": "38 Sadalat Street, Agodo, after Dbanj Hotel",
}


def format_naira(amount: int) -> str:
    try:
        return f"₦{int(amount):,}"
    except (TypeError, ValueError):
        return f"₦0"


def build_whatsapp_link(message: str, number: str = SITE["whatsapp_number"]) -> str:
    return f"https://wa.me/{number}?text={quote(message)}"


def product_inquiry_message(product_name: str) -> str:
    return (
        f"Hello Jennie_Hairport, I'd like to ask a question about {product_name}. "
        "Please send me more details."
    )


def general_inquiry_message() -> str:
    return "Hello Jennie_Hairport, I'd like to know more about your available hair collections."


def payment_plan_inquiry_message() -> str:
    return "Hello Jennie_Hairport, I'd like to ask about your flexible payment plan options."


def wholesale_inquiry_message() -> str:
    return (
        "Hello Jennie_Hairport, I'm interested in becoming a wholesale customer. "
        "Please send me your wholesale terms and pricing."
    )


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def generate_order_reference() -> str:
    return "JH-" + secrets.token_hex(4).upper()
