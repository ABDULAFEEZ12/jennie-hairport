import io

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from PIL import Image, ImageOps

from ... import data
from ...extensions import get_fs_bucket
from ...models import safe_object_id
from ...utils import slugify
from ...auth import check_admin_password, admin_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@admin_required
def index():
    return redirect(url_for("admin.products"))


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if check_admin_password(password):
            session["is_admin"] = True
            return redirect(url_for("admin.products"))
        flash("Incorrect password.")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/products")
@admin_required
def products():
    return render_template("admin/products.html", products=data.get_all_products())


def _allowed_image(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def _upload_image_to_gridfs(file_storage) -> str:
    """
    Compresses an uploaded image and stores it in MongoDB GridFS, returning the
    /media/<file_id> URL path the site should use to display it.
    """
    raw_bytes = file_storage.read()
    content_type = file_storage.mimetype or "application/octet-stream"

    try:
        image = Image.open(io.BytesIO(raw_bytes))
        image = ImageOps.exif_transpose(image)
        max_dim = 1400
        if image.width > max_dim or image.height > max_dim:
            image.thumbnail((max_dim, max_dim), Image.LANCZOS)

        buffer = io.BytesIO()
        if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
            image.convert("RGBA").save(buffer, format="PNG", optimize=True)
            content_type = "image/png"
        else:
            image.convert("RGB").save(buffer, format="JPEG", quality=82, optimize=True)
            content_type = "image/jpeg"
        data_bytes = buffer.getvalue()
    except Exception:
        data_bytes = raw_bytes

    file_id = get_fs_bucket().upload_from_stream(
        file_storage.filename, io.BytesIO(data_bytes), metadata={"contentType": content_type}
    )
    return url_for("serve_media", file_id=str(file_id))


def _delete_gridfs_image(image_path):
    if not image_path or not image_path.startswith("/media/"):
        return
    file_id = safe_object_id(image_path.rsplit("/", 1)[-1])
    if file_id:
        try:
            get_fs_bucket().delete(file_id)
        except Exception:
            pass


def _product_from_form(form, files):
    def as_bool(name):
        return form.get(name) == "on"

    def as_list(name):
        raw = form.get(name, "")
        return [line.strip() for line in raw.splitlines() if line.strip()]

    def as_lengths(name):
        raw = form.get(name, "")
        return [int(part.strip()) for part in raw.split(",") if part.strip().isdigit()]

    badge = form.get("badge") or None
    if badge == "none":
        badge = None

    result = dict(
        name=form.get("name", "").strip(),
        category=form.get("category"),
        description=form.get("description", "").strip(),
        specifications=as_list("specifications"),
        care_instructions=as_list("care_instructions"),
        price=int(form.get("price") or 0),
        old_price=int(form["old_price"]) if form.get("old_price") else None,
        lengths=as_lengths("lengths"),
        availability=as_bool("availability"),
        stock_status=form.get("stock_status", "in-stock"),
        featured=as_bool("featured"),
        best_seller=as_bool("best_seller"),
        new_arrival=as_bool("new_arrival"),
        wholesale_available=as_bool("wholesale_available"),
        badge=badge,
    )

    uploaded = files.getlist("images") if files else []
    image_paths = [
        _upload_image_to_gridfs(f) for f in uploaded if f and f.filename and _allowed_image(f.filename)
    ]
    if image_paths:
        result["images"] = image_paths

    return result


@admin_bp.route("/products/new", methods=["GET", "POST"])
@admin_required
def new_product():
    if request.method == "POST":
        product_data = _product_from_form(request.form, request.files)
        if not product_data["name"] or not product_data["category"] or product_data["price"] <= 0:
            flash("Name, category and a valid price are required.")
            return render_template("admin/product_form.html", product=None)

        product_data.setdefault("images", ["placeholder"])
        base_slug = slugify(product_data["name"])
        slug = base_slug
        counter = 1
        while data.slug_exists(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1
        product_data["slug"] = slug

        data.create_product(product_data)
        flash("Product created.")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_form.html", product=None)


@admin_bp.route("/products/<product_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = data.get_product_by_id(product_id)
    if not product:
        flash("Product not found.")
        return redirect(url_for("admin.products"))

    if request.method == "POST":
        product_data = _product_from_form(request.form, request.files)
        if not product_data["name"] or not product_data["category"] or product_data["price"] <= 0:
            flash("Name, category and a valid price are required.")
            return render_template("admin/product_form.html", product=product)

        if "images" in product_data:
            for old_image in product.images:
                _delete_gridfs_image(old_image)

        data.update_product(product_id, product_data)
        flash("Product updated.")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_form.html", product=product)


@admin_bp.route("/products/<product_id>/delete", methods=["POST"])
@admin_required
def delete_product(product_id):
    product = data.get_product_by_id(product_id)
    if product:
        for image in product.images:
            _delete_gridfs_image(image)
    if data.delete_product(product_id):
        flash("Product deleted.")
    else:
        flash("Product not found.")
    return redirect(url_for("admin.products"))


@admin_bp.route("/orders")
@admin_required
def orders():
    return render_template("admin/orders.html", orders=data.get_orders())


@admin_bp.route("/messages")
@admin_required
def messages():
    all_messages = data.get_messages()
    data.mark_all_messages_read()
    return render_template("admin/messages.html", messages=all_messages)
