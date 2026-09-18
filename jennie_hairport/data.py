"""Data-access layer: every MongoDB read/write for products, orders and messages lives here."""

from datetime import datetime, timezone

from .extensions import products_collection, orders_collection, messages_collection
from .models import ProductDoc, OrderDoc, MessageDoc, safe_object_id


def _utcnow():
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------

def get_all_products():
    return [ProductDoc(d) for d in products_collection().find().sort("created_at", -1)]


def get_product_by_slug(slug):
    doc = products_collection().find_one({"slug": slug})
    return ProductDoc(doc) if doc else None


def get_product_by_id(id_str):
    obj_id = safe_object_id(id_str)
    if not obj_id:
        return None
    doc = products_collection().find_one({"_id": obj_id})
    return ProductDoc(doc) if doc else None


def get_related_products(product, limit=4):
    cursor = products_collection().find(
        {"category": product.get("category"), "_id": {"$ne": safe_object_id(product.id)}}
    ).limit(limit)
    return [ProductDoc(d) for d in cursor]


def slug_exists(slug, exclude_id=None):
    query = {"slug": slug}
    if exclude_id:
        query["_id"] = {"$ne": safe_object_id(exclude_id)}
    return products_collection().find_one(query) is not None


def filter_and_sort_products(args):
    query = {}

    q = (args.get("q") or "").strip()
    if q:
        query["$or"] = [
            {"name": {"$regex": q, "$options": "i"}},
            {"category": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
        ]

    category = (args.get("category") or "").strip()
    if category == "new-arrivals":
        query["new_arrival"] = True
    elif category == "best-sellers":
        query["best_seller"] = True
    elif category == "wholesale":
        query["wholesale_available"] = True
    elif category:
        query["category"] = category

    if args.get("availability") == "in-stock":
        query["availability"] = True

    min_price = args.get("minPrice")
    max_price = args.get("maxPrice")
    if (min_price and min_price.isdigit()) or (max_price and max_price.isdigit()):
        price_filter = {}
        if min_price and min_price.isdigit():
            price_filter["$gte"] = int(min_price)
        if max_price and max_price.isdigit():
            price_filter["$lte"] = int(max_price)
        query["price"] = price_filter

    products = [ProductDoc(d) for d in products_collection().find(query)]

    length = args.get("length")
    if length and length.isdigit():
        products = [p for p in products if int(length) in p.lengths]

    sort = args.get("sort") or ""
    if sort == "price-asc":
        products.sort(key=lambda p: p.get("price", 0))
    elif sort == "price-desc":
        products.sort(key=lambda p: p.get("price", 0), reverse=True)
    elif sort == "newest":
        products.sort(key=lambda p: p.get("created_at") or _utcnow(), reverse=True)
    elif sort == "best-selling":
        products.sort(key=lambda p: bool(p.get("best_seller")), reverse=True)

    return products


def get_all_lengths():
    lengths = set()
    for doc in products_collection().find({}, {"lengths": 1}):
        lengths.update(doc.get("lengths") or [])
    return sorted(lengths)


def create_product(data: dict) -> ProductDoc:
    data = dict(data)
    data.setdefault("created_at", _utcnow())
    result = products_collection().insert_one(data)
    return ProductDoc(products_collection().find_one({"_id": result.inserted_id}))


def update_product(id_str: str, data: dict):
    obj_id = safe_object_id(id_str)
    if not obj_id:
        return None
    products_collection().update_one({"_id": obj_id}, {"$set": data})
    doc = products_collection().find_one({"_id": obj_id})
    return ProductDoc(doc) if doc else None


def delete_product(id_str: str) -> bool:
    obj_id = safe_object_id(id_str)
    if not obj_id:
        return False
    result = products_collection().delete_one({"_id": obj_id})
    return result.deleted_count > 0


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------

def create_order(data: dict) -> OrderDoc:
    data = dict(data)
    data.setdefault("created_at", _utcnow())
    data.setdefault("payment_status", "pending")
    data.setdefault("paid_at", None)
    result = orders_collection().insert_one(data)
    return OrderDoc(orders_collection().find_one({"_id": result.inserted_id}))


def reference_exists(reference: str) -> bool:
    return orders_collection().find_one({"reference": reference}) is not None


def get_order_by_reference(reference: str):
    doc = orders_collection().find_one({"reference": reference})
    return OrderDoc(doc) if doc else None


def get_orders():
    return [OrderDoc(d) for d in orders_collection().find().sort("created_at", -1)]


def update_order_status(reference: str, status: str, paid_at=None):
    update = {"payment_status": status}
    if paid_at is not None:
        update["paid_at"] = paid_at
    orders_collection().update_one({"reference": reference}, {"$set": update})


# ---------------------------------------------------------------------------
# Contact messages
# ---------------------------------------------------------------------------

def create_message(data: dict) -> MessageDoc:
    data = dict(data)
    data.setdefault("created_at", _utcnow())
    data.setdefault("read", False)
    result = messages_collection().insert_one(data)
    return MessageDoc(messages_collection().find_one({"_id": result.inserted_id}))


def get_messages():
    return [MessageDoc(d) for d in messages_collection().find().sort("created_at", -1)]


def mark_all_messages_read():
    messages_collection().update_many({"read": False}, {"$set": {"read": True}})
