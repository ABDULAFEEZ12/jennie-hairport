"""
No demo/sample products ship with this project — the catalogue starts empty and the
business owner adds real products through the admin panel (/admin/products/new).

PRODUCTS is intentionally empty. It exists only so a future migration or bulk-import
script has an obvious, documented place to insert real product dicts if that's ever
useful — it is NOT a place to add placeholder or example data.
"""

from .extensions import products_collection
from .utils import slugify

PRODUCTS = []


def seed_products(force: bool = False) -> int:
    """Populate the products collection from PRODUCTS if it's empty (or always, if force=True).

    With PRODUCTS empty by default, this is a no-op — the catalogue stays exactly as
    the owner has built it through the admin panel.
    """
    collection = products_collection()

    if not PRODUCTS:
        return 0

    if not force and collection.find_one() is not None:
        return 0

    if force:
        collection.delete_many({})

    created = 0
    for data in PRODUCTS:
        slug = slugify(data["name"])
        if collection.find_one({"slug": slug}):
            continue
        doc = dict(data)
        doc["slug"] = slug
        collection.insert_one(doc)
        created += 1

    return created
