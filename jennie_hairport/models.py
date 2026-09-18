from bson.objectid import ObjectId
from bson.errors import InvalidId

CATEGORY_CHOICES = ["bone-straight", "wigs", "bundles", "closures", "frontals"]
CATEGORY_LABELS = {
    "bone-straight": "Bone Straight",
    "wigs": "Wigs",
    "bundles": "Bundles",
    "closures": "Closures",
    "frontals": "Frontals",
}
STOCK_STATUS_CHOICES = ["in-stock", "low-stock", "sold-out", "preorder"]
STOCK_STATUS_LABELS = {
    "in-stock": "In Stock",
    "low-stock": "Low Stock",
    "sold-out": "Sold Out",
    "preorder": "Pre-Order",
}
BADGE_CHOICES = ["Best Seller", "New", "Limited"]


def safe_object_id(value):
    """Convert a string to ObjectId, returning None if it isn't a valid one."""
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


class DocWrapper:
    """Thin wrapper giving a Mongo document dict-and-attribute access, so templates and
    routes can use `product.name` instead of `product['name']`."""

    def __init__(self, doc):
        self._doc = doc or {}

    def __getattr__(self, name):
        try:
            return self._doc[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def get(self, name, default=None):
        return self._doc.get(name, default)

    def to_dict(self):
        return dict(self._doc)


class ProductDoc(DocWrapper):
    @property
    def id(self):
        return str(self._doc["_id"])

    @property
    def seed(self):
        """A stable small integer derived from the id, used to pick a placeholder gradient."""
        return int(str(self._doc["_id"]), 16) % 1000

    @property
    def category_label(self):
        return CATEGORY_LABELS.get(self._doc.get("category"), self._doc.get("category"))

    @property
    def stock_status_label(self):
        return STOCK_STATUS_LABELS.get(self._doc.get("stock_status"), self._doc.get("stock_status"))

    @property
    def old_price(self):
        return self._doc.get("old_price")

    @property
    def discount_percent(self):
        old = self._doc.get("old_price")
        price = self._doc.get("price", 0)
        if old and old > price:
            return round((old - price) / old * 100)
        return None

    @property
    def images(self):
        return self._doc.get("images") or ["placeholder"]

    @property
    def primary_image(self):
        return self.images[0]

    @property
    def lengths(self):
        return self._doc.get("lengths") or []

    @property
    def specifications(self):
        return self._doc.get("specifications") or []

    @property
    def care_instructions(self):
        return self._doc.get("care_instructions") or []


class OrderItemDoc(DocWrapper):
    @property
    def line_total(self):
        return self._doc.get("price", 0) * self._doc.get("quantity", 1)


class OrderDoc(DocWrapper):
    @property
    def id(self):
        return str(self._doc["_id"])

    @property
    def items(self):
        return [OrderItemDoc(i) for i in self._doc.get("items", [])]


class MessageDoc(DocWrapper):
    @property
    def id(self):
        return str(self._doc["_id"])
