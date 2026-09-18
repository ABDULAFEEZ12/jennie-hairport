import os

from flask import Blueprint, render_template, request, jsonify, abort, url_for, current_app

from ... import data
from ...models import CATEGORY_LABELS
from ...utils import generate_order_reference
from ...squad import initiate_transaction, SquadError

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    all_products = data.get_all_products()
    best_sellers = [p for p in all_products if p.get("best_seller")][:8]
    new_arrivals = [p for p in all_products if p.get("new_arrival")][:8]
    featured = [p for p in all_products if p.get("featured")][:8]
    categories_with_products = {p.get("category") for p in all_products}

    owner_photo_path = os.path.join(current_app.static_folder, "images", "main.jpeg")
    owner_photo_url = url_for("static", filename="images/main.jpeg") if os.path.exists(owner_photo_path) else None

    return render_template(
        "home.html",
        has_products=bool(all_products),
        best_sellers=best_sellers or featured,
        new_arrivals=new_arrivals,
        categories_with_products=categories_with_products,
        owner_photo_url=owner_photo_url,
    )


@main_bp.route("/shop")
def shop():
    products = data.filter_and_sort_products(request.args)
    all_lengths = data.get_all_lengths()

    category = (request.args.get("category") or "").strip()
    special_labels = {"new-arrivals": "New Arrivals", "best-sellers": "Best Sellers", "wholesale": "Wholesale"}

    if category in special_labels:
        heading = special_labels[category]
    elif category in CATEGORY_LABELS:
        heading = CATEGORY_LABELS[category]
    else:
        heading = "All Products"

    return render_template(
        "shop.html",
        products=products,
        heading=heading,
        all_lengths=all_lengths,
        active_category=category,
        active_sort=request.args.get("sort", ""),
        active_availability=request.args.get("availability", ""),
        active_length=request.args.get("length", ""),
        catalog_empty=not data.get_all_products(),
    )


@main_bp.route("/product/<slug>")
def product_detail(slug):
    product = data.get_product_by_slug(slug)
    if not product:
        abort(404)
    related = data.get_related_products(product)
    return render_template("product.html", product=product, related=related)


@main_bp.route("/cart")
def cart():
    return render_template("cart.html")


@main_bp.route("/payment-plans")
def payment_plans():
    return render_template("payment_plans.html")


@main_bp.route("/wholesale")
def wholesale():
    return render_template("wholesale.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        body = request.get_json(silent=True) or request.form
        name = (body.get("name") or "").strip()
        email = (body.get("email") or "").strip()
        message = (body.get("message") or "").strip()

        if not name or not email or not message:
            return jsonify({"message": "Name, email and message are required."}), 400

        data.create_message({"name": name[:200], "email": email[:200], "message": message[:2000]})
        return jsonify({"message": "Message sent successfully."})

    return render_template("contact.html")


@main_bp.route("/api/checkout", methods=["POST"])
def api_checkout():
    """
    Creates a pending Order from the client-side cart, then starts a Squad hosted-checkout
    transaction and returns its checkout_url for the browser to redirect to. The order is
    only marked paid later, in the /payments/callback route, after Squad confirms it
    server-side — never from anything the client sends here.
    """
    body = request.get_json(silent=True) or {}

    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip()
    phone = (body.get("phone") or "").strip()
    location = (body.get("location") or "").strip()
    notes = (body.get("notes") or "").strip()
    items = body.get("items") or []

    if not name or not email or not phone or not location:
        return jsonify({"message": "Name, email, phone and delivery location are required."}), 400
    if not items:
        return jsonify({"message": "Your bag is empty."}), 400
    if "@" not in email:
        return jsonify({"message": "Please enter a valid email address."}), 400

    amount = 0
    order_items = []
    for item in items:
        try:
            price = int(item["price"])
            quantity = max(1, int(item.get("quantity", 1)))
        except (KeyError, TypeError, ValueError):
            continue
        amount += price * quantity
        order_items.append(
            {
                "product_id": item.get("id"),
                "name": str(item.get("name", "Product"))[:200],
                "price": price,
                "quantity": quantity,
                "length": item.get("length"),
            }
        )

    if not order_items or amount <= 0:
        return jsonify({"message": "Your bag has no valid items."}), 400

    reference = generate_order_reference()
    while data.reference_exists(reference):
        reference = generate_order_reference()

    order = data.create_order(
        {
            "reference": reference,
            "customer_name": name[:200],
            "email": email[:200],
            "phone": phone[:40],
            "location": location[:300],
            "notes": notes[:500] or None,
            "amount": amount,
            "items": order_items,
        }
    )

    try:
        checkout_url = initiate_transaction(
            secret_key=current_app.config["SQUAD_SECRET_KEY"],
            env=current_app.config["SQUAD_ENV"],
            amount_naira=amount,
            email=email,
            transaction_ref=order.reference,
            callback_url=url_for("payments.callback", ref=order.reference, _external=True),
            customer_name=name,
        )
    except SquadError as exc:
        current_app.logger.error("Squad initiate failed for order %s: %s", order.reference, exc)
        return (
            jsonify(
                {
                    "message": (
                        "We couldn't start your payment right now. Please try again, or "
                        "message us on WhatsApp to complete your order."
                    )
                }
            ),
            502,
        )

    return jsonify({"checkout_url": checkout_url, "reference": order.reference})
