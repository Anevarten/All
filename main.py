from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

import database as db
from products import (
    PILLOWS, RELAX_MATTRESSES, VALUE_PLUS_MATTRESSES,
    CERTIFICATIONS, BANNERS, PILLOW_INDEX, fmt,
)
from routes.shop  import router as shop_router
from routes.admin import router as admin_router

app = FastAPI(title="Natures Slumber")
db.init_db()

BASE = Path(__file__).parent
app.mount("/assets", StaticFiles(directory=BASE / "assets"), name="assets")
templates = Jinja2Templates(directory=BASE / "templates")

app.include_router(shop_router)
app.include_router(admin_router)


# ── Page routes ───────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {
        "banners": BANNERS,
        "certifications": CERTIFICATIONS,
        "featured_pillows": PILLOWS[:8],
        "fmt": fmt,
    })


@app.get("/mattress", response_class=HTMLResponse)
async def mattress(request: Request):
    return templates.TemplateResponse(request, "mattress.html", {})


@app.get("/mattress/relax", response_class=HTMLResponse)
async def relax_mattress(request: Request):
    return templates.TemplateResponse(request, "mattress-category.html", {
        "category": "Relax Mattress",
        "description": "Premium organic latex mattresses designed for deep, restorative sleep.",
        "img": "AdobeStock_181325350_mattress.jpg",
        "products": RELAX_MATTRESSES,
        "fmt": fmt,
    })


@app.get("/mattress/value-plus", response_class=HTMLResponse)
async def value_plus_mattress(request: Request):
    return templates.TemplateResponse(request, "mattress-category.html", {
        "category": "Value Plus Mattress",
        "description": "All the benefits of organic latex at an exceptional price point.",
        "img": "AdobeStock_181325350_mattress.jpg",
        "products": VALUE_PLUS_MATTRESSES,
        "fmt": fmt,
    })


@app.get("/pillows", response_class=HTMLResponse)
async def pillows(request: Request):
    return templates.TemplateResponse(request, "pillows.html", {
        "pillows": PILLOWS,
        "fmt": fmt,
    })


@app.get("/pillows/{slug}", response_class=HTMLResponse)
async def pillow_detail(request: Request, slug: str):
    pillow = PILLOW_INDEX.get(slug)
    if not pillow:
        return HTMLResponse("Product not found", status_code=404)
    related = [p for p in PILLOWS if p["slug"] != slug][:4]
    return templates.TemplateResponse(request, "pillow-detail.html", {
        "pillow": pillow,
        "related": related,
        "fmt": fmt,
    })


@app.get("/toppers", response_class=HTMLResponse)
async def toppers(request: Request):
    return templates.TemplateResponse(request, "toppers.html", {})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(request, "about.html", {})


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(request, "contact.html", {})
