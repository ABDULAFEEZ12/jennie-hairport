from datetime import datetime, timezone

from .extensions import products_collection
from .utils import slugify

PRODUCTS = [
    dict(
        name="Vietnamese Bone Straight Bundle",
        category="bone-straight",
        description=(
            "Our signature bone straight bundle — sleek, silky, and naturally full from root "
            "to tip. Sourced directly from single donors in Vietnam and processed to keep the "
            "cuticle intact, so it holds a silk-straight finish wash after wash without turning "
            "brittle or shedding."
        ),
        specifications=[
            "100% Vietnamese human hair, single donor",
            "Cuticle aligned, double-machine wefted",
            "Natural black (can be toned/dyed by a professional)",
            "Minimal shedding and tangling with proper care",
        ],
        care_instructions=[
            "Detangle gently from tip to root before washing",
            "Wash with sulphate-free shampoo in lukewarm water",
            "Air dry or blow dry on low heat with a heat protectant",
            "Store on a silk/satin wrap or bonnet when not in use",
        ],
        price=65000,
        old_price=None,
        images=["placeholder"],
        lengths=[12, 14, 16, 18, 20, 22, 24, 26],
        availability=True,
        stock_status="in-stock",
        featured=True,
        best_seller=True,
        new_arrival=False,
        wholesale_available=True,
        badge="Best Seller",
        created_at=datetime(2026, 1, 14, tzinfo=timezone.utc),
    ),
    dict(
        name="Bone Straight 3-Bundle Deal",
        category="bone-straight",
        description=(
            "A full, install-ready set of three bone straight bundles cut from the same donor "
            "for a seamless colour and texture match. Built for fuller sew-ins, closures, and "
            "frontal installs that need real volume without extra bundles."
        ),
        specifications=[
            "3 matching bundles, same donor batch",
            "100% Vietnamese human hair",
            "Consistent density across all three bundles",
            "Recommended with a closure or frontal for a full unit",
        ],
        care_instructions=[
            "Detangle each bundle separately before installing",
            "Deep condition every 2-3 weeks",
            "Avoid high heat on a daily basis",
            "Sleep with hair protected in a bonnet or wrap",
        ],
        price=175000,
        old_price=195000,
        images=["placeholder"],
        lengths=[14, 16, 18, 20, 22, 24, 26, 28],
        availability=True,
        stock_status="in-stock",
        featured=True,
        best_seller=True,
        new_arrival=False,
        wholesale_available=True,
        badge="Best Seller",
        created_at=datetime(2026, 1, 20, tzinfo=timezone.utc),
    ),
    dict(
        name="Bone Straight Bundle + Closure Set",
        category="bone-straight",
        description=(
            "Two bone straight bundles paired with a matching lace closure for a complete, "
            "natural-looking install straight out of the pack. A favourite for customers who "
            "want a full head without sourcing pieces separately."
        ),
        specifications=[
            "2 bundles + 1 matching 4x4 lace closure",
            "100% Vietnamese human hair",
            "Free-parting closure, bleached knots",
            "Colour and texture matched across the set",
        ],
        care_instructions=[
            "Detangle closure lace with extra care",
            "Use a leave-in conditioner before styling",
            "Low heat setting only on the closure",
            "Store flat or on a mannequin head when not in use",
        ],
        price=145000,
        old_price=None,
        images=["placeholder"],
        lengths=[14, 16, 18, 20, 22, 24],
        availability=True,
        stock_status="low-stock",
        featured=False,
        best_seller=False,
        new_arrival=True,
        wholesale_available=True,
        badge="New",
        created_at=datetime(2026, 8, 2, tzinfo=timezone.utc),
    ),
    dict(
        name="Bone Straight HD Lace Front Wig",
        category="wigs",
        description=(
            "A pre-plucked, glueless-ready HD lace front wig in our signature bone straight "
            "texture. The lace melts naturally into most skin tones, giving a seamless "
            "hairline without heavy makeup or powder."
        ),
        specifications=[
            "13x4 HD transparent lace frontal wig",
            "150% density, pre-plucked hairline",
            "Adjustable straps and combs for a secure fit",
            "Baby hairs included for natural styling",
        ],
        care_instructions=[
            "Use lace-safe adhesive or apply glueless with the elastic band",
            "Wash the lace gently with a soft brush",
            "Avoid sleeping in the wig without protection",
            "Store on a wig stand to keep its shape",
        ],
        price=135000,
        old_price=155000,
        images=["placeholder"],
        lengths=[16, 18, 20, 22, 24, 26],
        availability=True,
        stock_status="in-stock",
        featured=True,
        best_seller=True,
        new_arrival=False,
        wholesale_available=True,
        badge="Best Seller",
        created_at=datetime(2026, 2, 10, tzinfo=timezone.utc),
    ),
    dict(
        name="Glueless Bone Straight Bob Wig",
        category="wigs",
        description=(
            "A chic, chin-to-shoulder length bob wig designed for effortless everyday wear. "
            "No glue, no gel — just a snug, glueless cap construction that goes on and comes "
            "off in minutes."
        ),
        specifications=[
            "Glueless wear-and-go cap construction",
            "13x4 lace front, bone straight texture",
            "130% density for a natural, blended finish",
            "Pre-cut and styled bob, ready to wear",
        ],
        care_instructions=[
            "Detangle with a wide-tooth comb only",
            "Wash sparingly to preserve the pre-styled cut",
            "Avoid excessive heat styling",
            "Store on a wig stand or in its original packaging",
        ],
        price=85000,
        old_price=None,
        images=["placeholder"],
        lengths=[10, 12, 14],
        availability=True,
        stock_status="in-stock",
        featured=False,
        best_seller=True,
        new_arrival=False,
        wholesale_available=True,
        badge="Best Seller",
        created_at=datetime(2026, 3, 5, tzinfo=timezone.utc),
    ),
    dict(
        name="Body Wave Lace Front Wig",
        category="wigs",
        description=(
            "Soft, bouncy body wave curls that fall naturally with movement. A versatile "
            "everyday wig that holds its wave pattern through multiple wears with the right "
            "care."
        ),
        specifications=[
            "13x4 lace front, body wave texture",
            "180% density for a fuller look",
            "Pre-plucked hairline with baby hairs",
            "Natural black, dyeable by a professional",
        ],
        care_instructions=[
            "Finger detangle to protect the curl pattern",
            "Air dry to maintain the wave definition",
            "Use a curl-defining leave-in when refreshing",
            "Avoid brushing when dry",
        ],
        price=150000,
        old_price=None,
        images=["placeholder"],
        lengths=[18, 20, 22, 24],
        availability=True,
        stock_status="in-stock",
        featured=False,
        best_seller=False,
        new_arrival=True,
        wholesale_available=True,
        badge="New",
        created_at=datetime(2026, 7, 18, tzinfo=timezone.utc),
    ),
    dict(
        name="U-Part Wig — Bone Straight",
        category="wigs",
        description=(
            "A quick, low-manipulation install that blends with your leave-out for a natural "
            "part. Ideal for anyone who wants length and volume without a full lace "
            "application."
        ),
        specifications=[
            "U-part cap construction, no lace needed",
            "Bone straight texture, 130% density",
            "Adjustable combs and straps",
            "Blends easily with relaxed or textured leave-out",
        ],
        care_instructions=[
            "Blend leave-out with matching products",
            "Detangle before and after each wear",
            "Store on a stand between uses",
            "Avoid excessive tension at the part",
        ],
        price=70000,
        old_price=None,
        images=["placeholder"],
        lengths=[14, 16, 18, 20],
        availability=True,
        stock_status="in-stock",
        featured=False,
        best_seller=False,
        new_arrival=False,
        wholesale_available=True,
        badge=None,
        created_at=datetime(2026, 1, 28, tzinfo=timezone.utc),
    ),
    dict(
        name="Deep Wave Bundle",
        category="bundles",
        description=(
            "Defined, springy deep wave curls with a full, healthy bounce. A textured "
            "alternative to our bone straight line for customers who want more volume and "
            "movement."
        ),
        specifications=[
            "100% Vietnamese human hair",
            "Deep wave texture, double wefted",
            "Holds curl pattern through multiple washes",
            "Can be worn straight with heat and reverts with water",
        ],
        care_instructions=[
            "Finger detangle from ends to roots",
            "Use a curl cream to refresh between washes",
            "Deep condition regularly to maintain elasticity",
            "Air dry or diffuse on low heat",
        ],
        price=72000,
        old_price=None,
        images=["placeholder"],
        lengths=[14, 16, 18, 20, 22, 24],
        availability=True,
        stock_status="in-stock",
        featured=False,
        best_seller=False,
        new_arrival=False,
        wholesale_available=True,
        badge=None,
        created_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
    ),
    dict(
        name="Curly Bundle Deal (3 Bundles)",
        category="bundles",
        description=(
            "Three matching curly bundles for a full, textured install with real bounce and "
            "body. Cut from the same batch for a consistent curl pattern from root to tip."
        ),
        specifications=[
            "3 matching bundles, same donor batch",
            "Kinky curly texture, minimal shedding",
            "Best paired with a curly closure or frontal",
            "Holds definition with proper moisture routine",
        ],
        care_instructions=[
            "Use the LOC method (liquid, oil, cream) between washes",
            "Detangle in sections while wet with conditioner",
            "Avoid brushes — use fingers or a wide-tooth comb",
            "Pineapple at night to preserve curls",
        ],
        price=168000,
        old_price=190000,
        images=["placeholder"],
        lengths=[14, 16, 18, 20, 22],
        availability=False,
        stock_status="sold-out",
        featured=False,
        best_seller=False,
        new_arrival=False,
        wholesale_available=True,
        badge="Limited",
        created_at=datetime(2025, 12, 10, tzinfo=timezone.utc),
    ),
    dict(
        name="4x4 Lace Closure — Bone Straight",
        category="closures",
        description=(
            "A versatile 4x4 lace closure that gives a natural-looking part and clean finish "
            "to any bundle install. Bleached knots and a soft, pre-plucked hairline included."
        ),
        specifications=[
            "4x4 lace closure, free part",
            "Bone straight texture to match bundles",
            "Bleached knots for a natural scalp look",
            "Medium brown lace, blends with most skin tones",
        ],
        care_instructions=[
            "Handle lace gently when detangling",
            "Use a lace-safe adhesive if laying flat",
            "Avoid heavy oils directly on the lace",
            "Store flat to preserve the parting space",
        ],
        price=45000,
        old_price=None,
        images=["placeholder"],
        lengths=[12, 14, 16, 18, 20],
        availability=True,
        stock_status="in-stock",
        featured=False,
        best_seller=False,
        new_arrival=False,
        wholesale_available=True,
        badge=None,
        created_at=datetime(2026, 1, 5, tzinfo=timezone.utc),
    ),
    dict(
        name="5x5 Lace Closure — Body Wave",
        category="closures",
        description=(
            "A wider 5x5 closure for extra versatility in parting and styling, finished in a "
            "soft body wave texture that blends seamlessly with our body wave bundles."
        ),
        specifications=[
            "5x5 lace closure, multi-directional part",
            "Body wave texture",
            "Bleached knots, pre-plucked hairline",
            "HD lace option available on request",
        ],
        care_instructions=[
            "Finger detangle to preserve the wave pattern",
            "Air dry after washing",
            "Use light, water-based products on the lace",
            "Store on a mannequin head between uses",
        ],
        price=52000,
        old_price=None,
        images=["placeholder"],
        lengths=[14, 16, 18, 20],
        availability=True,
        stock_status="in-stock",
        featured=False,
        best_seller=False,
        new_arrival=True,
        wholesale_available=True,
        badge="New",
        created_at=datetime(2026, 6, 30, tzinfo=timezone.utc),
    ),
    dict(
        name="13x4 Transparent Frontal — Bone Straight",
        category="frontals",
        description=(
            "An ear-to-ear frontal that opens up styling options from a middle part to a "
            "sleek high ponytail. Transparent lace for an undetectable finish across a range "
            "of skin tones."
        ),
        specifications=[
            "13x4 transparent lace frontal",
            "Bone straight texture, pre-plucked",
            "Bleached knots with baby hairs",
            "Ear-to-ear coverage for versatile parting",
        ],
        care_instructions=[
            "Detangle gently, starting from the ends",
            "Use minimal adhesive directly on the lace",
            "Cleanse lace with a soft brush and gentle shampoo",
            "Store flat or on a stand to protect the shape",
        ],
        price=78000,
        old_price=89000,
        images=["placeholder"],
        lengths=[14, 16, 18, 20, 22],
        availability=True,
        stock_status="in-stock",
        featured=True,
        best_seller=False,
        new_arrival=False,
        wholesale_available=True,
        badge=None,
        created_at=datetime(2026, 2, 14, tzinfo=timezone.utc),
    ),
    dict(
        name="13x6 HD Frontal — Body Wave",
        category="frontals",
        description=(
            "A deeper 13x6 HD frontal for maximum styling flexibility, including sleek-backs "
            "and side parts. HD lace disappears into the skin for a natural, "
            "glue-free-looking hairline."
        ),
        specifications=[
            "13x6 HD lace frontal",
            "Body wave texture",
            "Deeper parting space for versatile styles",
            "Pre-plucked with baby hairs",
        ],
        care_instructions=[
            "Handle HD lace with extra care — it is delicate",
            "Use gentle, sulphate-free products only",
            "Air dry away from direct heat",
            "Avoid excessive tension when styling",
        ],
        price=98000,
        old_price=None,
        images=["placeholder"],
        lengths=[16, 18, 20, 22, 24],
        availability=True,
        stock_status="low-stock",
        featured=False,
        best_seller=False,
        new_arrival=False,
        wholesale_available=True,
        badge=None,
        created_at=datetime(2026, 3, 22, tzinfo=timezone.utc),
    ),
    dict(
        name="Wholesale Bone Straight Carton (10 Bundles)",
        category="bone-straight",
        description=(
            "A bulk carton of ten bone straight bundles for vendors, salons, and resellers. "
            "Priced for volume buyers — reach out on WhatsApp for current wholesale terms and "
            "minimum order details."
        ),
        specifications=[
            "10 bundles per carton, mixed or fixed lengths on request",
            "100% Vietnamese human hair",
            "Consistent quality across the batch",
            "Wholesale pricing available on request via WhatsApp",
        ],
        care_instructions=[
            "Store in a cool, dry place away from direct sunlight",
            "Keep bundles in their original packaging until sale",
            "Handle wefts gently to avoid shedding in transit",
        ],
        price=520000,
        old_price=None,
        images=["placeholder"],
        lengths=[16, 18, 20, 22, 24],
        availability=True,
        stock_status="in-stock",
        featured=False,
        best_seller=False,
        new_arrival=False,
        wholesale_available=True,
        badge=None,
        created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
    ),
]


def seed_products(force: bool = False) -> int:
    """Populate the products collection from PRODUCTS if it's empty (or always, if force=True)."""
    collection = products_collection()

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
