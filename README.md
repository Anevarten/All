# 🌿 Natures Slumber

A full-featured organic latex bedding e-commerce website built with **FastAPI + Jinja2 + Tailwind CSS + SQLite**.

## Features
- 🛒 Shopping cart (localStorage) with qty controls
- 💳 Checkout & order management (SQLite)
- ⭐ Dynamic product ratings & reviews
- 📦 Admin dashboard at `/admin`
- 🌿 Full product catalogue: Mattresses, Pillows, Toppers

## Quick Start

```bash
# 1. Create virtual environment
uv venv --python 3.11
uv pip install fastapi uvicorn jinja2 python-multipart

# 2. Run the server
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 3. Open in browser
open http://localhost:8000
```

## Pages
| URL | Page |
|---|---|
| `/` | Home |
| `/mattress` | Mattress catalogue |
| `/pillows` | Pillow catalogue |
| `/pillows/{slug}` | Pillow detail + ratings |
| `/cart` | Shopping cart |
| `/checkout` | Checkout |
| `/admin` | Order dashboard |

## Editing Products
All product data lives in **`products.py`**. Edit prices, names, descriptions there.

## Full documentation → [`TUTORIAL.md`](./TUTORIAL.md)
