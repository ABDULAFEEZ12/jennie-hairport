# Jennie_Hairport (Python / Flask)

Premium hair e-commerce site for Jennie_Hairport, built with **Flask + MongoDB**, styled by
hand (no build step), with a **Squad**-powered checkout and a built-in admin panel.

Product data, orders and contact messages are stored in **MongoDB Atlas**; product photos
are stored in **MongoDB GridFS** (same pattern as the original Kikkyhairs reference site).
WhatsApp is used only for inquiries/payment-plan/wholesale conversations — the cart
checkout charges customers directly through **Squad** (squadco.com).

## Getting Started

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
copy .env.example .env          # then edit .env with your real values
python run.py
```

Visit [http://localhost:5000](http://localhost:5000). The catalogue starts **empty** — no
demo or sample products ship with this project. Add your real products through
`/admin/products/new` (see [Managing Products](#managing-products) below). The homepage and
shop show a clean "coming soon" state until you do.

## MongoDB Setup (required — the app will not start without this)

1. Go to [cloud.mongodb.com](https://cloud.mongodb.com) and open your cluster (a free M0
   cluster is enough to run this site).
2. Click **Connect** on your cluster → **Drivers** → copy the connection string. It looks
   like:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
3. If you don't already have a database user, create one under **Database Access** and use
   its username/password in the string above (not your Atlas login password — a separate
   database user).
4. Under **Network Access**, make sure your server's IP (or `0.0.0.0/0` for
   quick testing — restrict this before going live) is allowed to connect.
5. Paste the finished string into `.env`:
   ```
   MONGO_URI=mongodb+srv://realuser:realpassword@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   MONGO_DB_NAME=jennie_hairport
   ```
6. Run `python run.py` — it will create the `jennie_hairport` database, its collections,
   and the starter products automatically.

**Never commit `.env`** — it's already in `.gitignore`. Treat your connection string as a
password: anyone with it has full read/write access to your database.

## Squad Payment Setup

This site uses Squad's **hosted checkout** (redirect flow) — the customer is sent to
Squad's own payment page, so this codebase never touches card numbers.

1. Create a Squad merchant account at [dashboard.squadco.com](https://dashboard.squadco.com).
2. Copy your **Secret Key** and **Public Key** (start with sandbox keys for testing).
3. Put them in `.env`:
   ```
   SQUAD_SECRET_KEY=sandbox_sk_...
   SQUAD_PUBLIC_KEY=sandbox_pk_...
   SQUAD_ENV=sandbox
   SITE_BASE_URL=https://your-real-domain.com   # used to build Squad's callback URL
   ```
4. Switch `SQUAD_ENV=live` and use your live keys when you're ready to accept real payments.
5. **Before accepting real money**, do a full test purchase in sandbox mode and confirm the
   order shows as paid in `/admin/orders`. Squad's API can change — the integration in
   [jennie_hairport/squad.py](jennie_hairport/squad.py) is built from their current public
   docs (docs.squadco.com) as of this writing; if a real transaction ever behaves
   unexpectedly, check Squad's docs before assuming this code is at fault.
6. For extra robustness in production, consider also configuring a **webhook** in your
   Squad dashboard pointing at a new endpoint you add — this build only does browser-redirect
   verification (`/payments/callback`), which is correct and safe, but a webhook adds a
   second, independent confirmation path in case a customer closes their browser mid-payment.

Payments are never trusted from the browser alone: `/payments/callback` always re-confirms
the real status directly with Squad's server before marking an order paid.

## Managing Products

Go to `/admin/login` and sign in with the password in `.env` (`ADMIN_PASSWORD`, default
`jennie-admin-2026` — **change this before going live**). From there you can add, edit and
delete products, including uploading images — they're compressed with Pillow and stored in
MongoDB GridFS, then served back at `/media/<id>`.

Changes are immediate — no rebuild or redeploy needed, since pages are rendered straight
from MongoDB on every request.

> **Note on testing this build**: everything except image upload was verified against a
> real MongoDB-shaped data layer (via `mongomock`) during development — every page, filter,
> the full checkout flow, and admin CRUD. Image upload specifically needs GridFS, which
> can only be tested against a real MongoDB connection, so **do one test upload through the
> admin panel once your real `MONGO_URI` is in place** to confirm it in your environment.

## Adding Your Logo and Brand Photo

No code changes needed — just drop the file in and reload the page.

| File you add | Where it appears |
|---|---|
| `static/images/logo.png` (or `.svg` / `.jpg` / `.jpeg`) | Header, mobile menu, footer, and browser favicon — automatically, everywhere at once |
| `static/images/main.jpeg` | The "Meet Jennie_Hairport" section on the homepage |

Until you add `logo.png`, the header shows a simple "J" monogram instead. Until you add
`main.jpeg`, the homepage brand-story section shows a tasteful neutral placeholder instead
of a broken image — nothing looks unfinished either way.

Recommended `main.jpeg` size: at least 1000×1250px (a 4:5 portrait crop), so it fills its
frame sharply on large screens.

## Brand & Contact Details

Brand constants (WhatsApp number, Instagram, TikTok, address) live in
[jennie_hairport/utils.py](jennie_hairport/utils.py) (the `SITE` dict) — update them there
and they update everywhere on the site automatically.

## Orders & Messages

- Every checkout attempt creates an order document (`pending` until Squad confirms it),
  viewable at `/admin/orders` along with its real-time payment status.
- The Contact page form saves submissions to the `messages` collection, viewable at
  `/admin/messages`.

## What You Still Need to Add

- Real logo, product photos (upload through the admin panel), and real testimonials — all
  currently shown as clearly marked, tasteful placeholders.
- Your real MongoDB Atlas connection string and Squad API keys (see above).
- Exact delivery fees/coverage areas — currently a placeholder note on the Contact page.
- A production `SECRET_KEY` — set a long random string in `.env` before deploying.

## Tech Stack

- Flask 3 (Blueprints: `main`, `admin`, `payments`)
- MongoDB Atlas via PyMongo — products, orders and contact messages as documents
- MongoDB GridFS — product image storage (compressed with Pillow on upload)
- Hand-written CSS (`static/css/style.css`) — no Tailwind/Node build step
- Vanilla JS for the cart (`static/js/cart.js`, localStorage-based) and UI interactions
  (`static/js/main.js`)
- Squad (squadco.com) for payment — hosted checkout only, no card data touches this server
- WhatsApp deep links for inquiries, payment-plan and wholesale conversations

## Production

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

(`gunicorn` is Unix-only — this won't run on Windows directly; deploy it to a Linux host.)

Put this behind a reverse proxy (Nginx/Caddy) with HTTPS, and set a strong `SECRET_KEY`,
your live Squad keys, your production `MONGO_URI`, and the site's real `SITE_BASE_URL` in
the production environment. Because product images live in MongoDB GridFS rather than on
local disk, this app can run on either a persistent server or most serverless/ephemeral
platforms — the only genuinely stateful dependency is MongoDB itself.
