# 🌿 Natures Slumber — Complete Website Guide

> Last updated: May 2026 | Stack: Python · FastAPI · Jinja2 · Tailwind CSS · SQLite

---

## Table of Contents
1. [Project Structure](#1-project-structure)
2. [Running the Website](#2-running-the-website)
3. [The Database](#3-the-database)
4. [Adding & Editing Products](#4-adding--editing-products)
5. [Managing Orders (Admin)](#5-managing-orders-admin)
6. [Cart & Checkout Flow](#6-cart--checkout-flow)
7. [Ratings System](#7-ratings-system)
8. [Editing the Design](#8-editing-the-design)
9. [Adding a New Page](#9-adding-a-new-page)
10. [Common Tasks Cheat Sheet](#10-common-tasks-cheat-sheet)

---

## 1. Project Structure

```
natures-slumber/
│
├── main.py              ← App entry point & page routes
├── products.py          ← ALL product data lives here
├── database.py          ← SQLite helpers (orders + ratings)
│
├── routes/
│   ├── shop.py          ← Cart/checkout/ratings API
│   └── admin.py         ← Admin dashboard routes
│
├── templates/
│   ├── base.html        ← Header + footer (edit once, applies everywhere)
│   ├── index.html       ← Home page
│   ├── mattress.html    ← Mattress landing
│   ├── mattress-category.html  ← Relax / Value Plus grid
│   ├── pillows.html     ← Pillow grid
│   ├── pillow-detail.html      ← Individual pillow page + ratings
│   ├── toppers.html     ← Toppers info page
│   ├── about.html       ← Who We Are
│   ├── contact.html     ← Contact form
│   ├── cart.html        ← Shopping cart
│   ├── checkout.html    ← Checkout form
│   ├── order-confirm.html      ← Order confirmation
│   ├── admin.html       ← Orders dashboard
│   └── admin-order.html ← Individual order detail
│
├── assets/ → symlink to "Natures Slumber_files/" (images, CSS, JS)
├── data/
│   └── store.db         ← SQLite database (auto-created on first run)
│
└── TUTORIAL.md          ← This file
```

---

## 2. Running the Website

### First time setup
```bash
cd Documents/Personal/natures-slumber
uv venv --python 3.11
uv pip install fastapi uvicorn jinja2 python-multipart
```

### Start the server
```bash
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
- `--reload` auto-restarts when you edit code (great for development)
- Open: **http://localhost:8000**
- Admin: **http://localhost:8000/admin**

### Stop the server
Press `Ctrl+C` in the terminal, or run:
```bash
kill $(lsof -ti:8000)
```

---

## 3. The Database

**Technology:** SQLite — a single file (`data/store.db`). No server, no config.
It's automatically created on first run. Free, reliable, perfect for small stores.

### Tables

| Table | What it stores |
|---|---|
| `orders` | Customer info, total, status, timestamp |
| `order_items` | Each product line within an order |
| `ratings` | Star ratings + review text per product slug |

### View the database (optional)
```bash
# Install DB browser: brew install --cask db-browser-for-sqlite
# Then open: data/store.db
```

Or query from command line:
```bash
sqlite3 data/store.db "SELECT ref, name, total, status FROM orders;"
```

---

## 4. Adding & Editing Products

**All product data lives in `products.py`.** Edit that file — changes appear everywhere automatically.

### Add a new pillow

Open `products.py` and add an entry to the `PILLOWS` list:

```python
{"slug": "travel",       # URL-safe ID — must be unique
 "name": "Travel Pillow",
 "img":  "travel-pillow.jpg",   # Put image in assets/ folder
 "price": 1500,                  # Integer rupees (no ₹ symbol)
 "old":   1875,                  # Original price (for "Sale" badge)
 "type":  "pillow",
 "desc":  "Compact latex pillow perfect for travel."},
```

The pillow will automatically appear on:
- `/pillows` grid
- The dropdown navigation
- The home page featured products (first 8)

### Add a new mattress size

Add to `RELAX_MATTRESSES` or `VALUE_PLUS_MATTRESSES`:

```python
{"slug":  "relax-super-king",
 "name":  "Relax Super King Mattress",
 "size":  "Super King (6×6.5 ft)",
 "price": 45000,
 "old":   55000,
 "type":  "mattress",
 "img":   "AdobeStock_181325350_mattress.jpg",
 "desc":  "The ultimate luxury latex mattress."},
```

### Change a price

Find the product in `products.py` and update `"price"` and/or `"old"`:
```python
"price": 2800,   # ← new sale price
"old":   3500,   # ← original price (shows as strikethrough)
```

---

## 5. Managing Orders (Admin)

### Access the dashboard
Go to: **http://localhost:8000/admin**

> ⚠️ There is no password yet. For production, add authentication before deploying.
> See `routes/admin.py` → `ADMIN_PASS = "slumber2026"` to set a password.

### What you can do
- **View all orders** with customer name, total, status, date
- **Filter by status** (pending / confirmed / shipped / delivered / cancelled)
- **Open an order** to see full details and items
- **Update order status** using the radio buttons on the order detail page

### Order statuses

| Status | Meaning |
|---|---|
| `pending` | Just placed, not yet reviewed |
| `confirmed` | You've confirmed and are preparing it |
| `shipped` | Dispatched to the customer |
| `delivered` | Customer received it |
| `cancelled` | Order was cancelled |

### Export orders to CSV (manual)
```bash
sqlite3 -csv data/store.db \
  "SELECT ref, name, email, phone, total, status, created_at FROM orders;" \
  > orders.csv
```

---

## 6. Cart & Checkout Flow

1. Customer browses → clicks **Add to Cart** on any product
2. Cart is saved to browser **localStorage** (persists across pages)
3. Cart icon in header shows live item count
4. `/cart` — shows all items with qty +/− controls and totals
5. `/checkout` — customer fills delivery details (name, email, phone, address)
6. On submit → POST to `/api/checkout` which:
   - Validates every product slug against the server catalog
   - Calculates totals server-side (can't be tampered with)
   - Saves to SQLite
   - Returns order reference
7. Customer is redirected to `/order/{ref}` confirmation page

**Payment:** Cash on Delivery only (for now). To add online payments, integrate Razorpay or PayU into `routes/shop.py`.

---

## 7. Ratings System

Each product page (`/pillows/{slug}`) has:

- **Star display** — fetched live from the API (`/api/ratings/{slug}`)
- **Interactive rating widget** — click 1–5 stars, optional review text, submit
- **Review feed** — shows last 10 reviews below the widget

### API endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/ratings/{slug}` | GET | Returns avg, count, reviews |
| `/api/ratings` | POST | Submit a new rating |

### POST body example
```json
{ "slug": "dm1", "stars": 5, "review": "Absolutely love this pillow!" }
```

---

## 8. Editing the Design

### Brand colours
Edit the Tailwind config block at the top of `templates/base.html`:
```js
tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: "#342c2a",   // Dark brown — header, text, buttons
        hover:   "#81981b",   // Olive green — hover state
        accent:  "#b0c845",   // Lime green — badges, highlights
        light:   "#f7f7f7",   // Off-white — backgrounds
      }
    }
  }
}
```

### Logo size
In `templates/base.html`, find the `<img>` tag in the header:
```html
<img src="/assets/natures-slumber-logo.png" class="h-24 object-contain" />
```
Change `h-24` to `h-28`, `h-32`, etc. (Tailwind units = 4px each, so h-24 = 96px).

### Header height
In `templates/base.html`, find:
```html
<div class="... h-28">
```
Adjust `h-28` to match the logo size.

### Hero slider images
Slider images are defined in `products.py`:
```python
BANNERS = [
    ("filename.jpg", "Caption text"),
    ...
]
```
Add an image to the `assets/` folder and add it to this list.

### Adding new images
1. Copy the image to `Documents/Personal/Natures Slumber_files/`
2. Reference it in templates as `/assets/your-image.jpg`
3. Reference it in `products.py` as just `"your-image.jpg"`

---

## 9. Adding a New Page

**Example: Adding a "Blog" page**

### Step 1 — Create the template
`templates/blog.html`:
```html
{% extends "base.html" %}
{% block title %}Blog — Natures Slumber{% endblock %}

{% block content %}
<section class="py-16 max-w-4xl mx-auto px-4">
  <h1 class="text-4xl font-bold text-primary mb-8">Our Blog</h1>
  <!-- Your content here -->
</section>
{% endblock %}
```

### Step 2 — Add the route in `main.py`
```python
@app.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    return templates.TemplateResponse(request, "blog.html", {})
```

### Step 3 — Add to navigation in `base.html`
```html
<a href="/blog" class="nav-link px-3 py-2 hover:text-accent transition-colors">Blog</a>
```

That's it! 🎉

---

## 10. Common Tasks Cheat Sheet

| Task | Where to look |
|---|---|
| Change a product price | `products.py` |
| Add a new product | `products.py` |
| View all orders | `http://localhost:8000/admin` |
| Change order status | Admin → click order → update status |
| Edit header/footer | `templates/base.html` |
| Edit home page | `templates/index.html` |
| Edit brand colours | `templates/base.html` → Tailwind config |
| Change logo | Replace `assets/natures-slumber-logo.png` |
| Add a page | `main.py` + new template |
| View the database | `sqlite3 data/store.db` or DB Browser |
| Restart after code change | `Ctrl+C` then re-run uvicorn command |
| Check server logs | `cat /tmp/natures-slumber.log` |

---

*Built with ❤️ using Python + FastAPI + Tailwind CSS + SQLite*
