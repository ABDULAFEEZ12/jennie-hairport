import os
from datetime import datetime

from flask import Flask, render_template, abort, Response
from gridfs.errors import NoFile

from config import Config
from .extensions import init_mongo, get_fs_bucket
from .models import CATEGORY_CHOICES, CATEGORY_LABELS, STOCK_STATUS_CHOICES, BADGE_CHOICES, safe_object_id
from . import utils
from .seed import seed_products


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config.from_object(config_class)

    init_mongo(app)

    with app.app_context():
        seed_products()

    def find_static_image(*candidates):
        """Returns the /static URL for the first candidate filename that actually
        exists in static/images/, or None if the owner hasn't added one yet."""
        for filename in candidates:
            if os.path.exists(os.path.join(app.static_folder, "images", filename)):
                return f"/static/images/{filename}"
        return None

    logo_url = find_static_image("logo.png", "logo.svg", "logo.jpg", "logo.jpeg")

    from .blueprints.main.routes import main_bp
    from .blueprints.admin.routes import admin_bp
    from .blueprints.payments.routes import payments_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(payments_bp, url_prefix="/payments")

    @app.route("/media/<file_id>")
    def serve_media(file_id):
        """Serves a product image stored in MongoDB GridFS."""
        obj_id = safe_object_id(file_id)
        if not obj_id:
            abort(404)
        try:
            grid_out = get_fs_bucket().open_download_stream(obj_id)
        except NoFile:
            abort(404)
        content_type = (grid_out.metadata or {}).get("contentType", "application/octet-stream")
        response = Response(grid_out.read(), mimetype=content_type)
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response

    @app.context_processor
    def inject_globals():
        return {
            "SITE": utils.SITE,
            "CATEGORY_CHOICES": CATEGORY_CHOICES,
            "CATEGORY_LABELS": CATEGORY_LABELS,
            "STOCK_STATUS_CHOICES": STOCK_STATUS_CHOICES,
            "BADGE_CHOICES": BADGE_CHOICES,
            "format_naira": utils.format_naira,
            "build_whatsapp_link": utils.build_whatsapp_link,
            "general_inquiry_message": utils.general_inquiry_message,
            "payment_plan_inquiry_message": utils.payment_plan_inquiry_message,
            "wholesale_inquiry_message": utils.wholesale_inquiry_message,
            "product_inquiry_message": utils.product_inquiry_message,
            "current_year": datetime.now().year,
            "logo_url": logo_url,
        }

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(_e):
        return render_template("500.html"), 500

    @app.cli.command("seed-db")
    def seed_db_command():
        """Re-seed the products collection (only inserts products that don't already exist)."""
        created = seed_products()
        print(f"Seeded {created} product(s).")

    return app
