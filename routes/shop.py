"""Shop routes: cart UI, checkout POST, order confirm, ratings API."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
import database as db
from products import ALL_PRODUCTS

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


# ── Pydantic models ───────────────────────────────────────────────────────────

class CartItem(BaseModel):
    slug: str
    qty: int = 1

class CheckoutPayload(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    city: str
    pincode: str
    notes: str = ""
    items: list[CartItem]

class RatingPayload(BaseModel):
    slug: str
    stars: int
    review: str = ""


# ── Pages ─────────────────────────────────────────────────────────────────────

@router.get("/cart", response_class=HTMLResponse)
async def cart_page(request: Request):
    return templates.TemplateResponse(request, "cart.html", {})


@router.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    return templates.TemplateResponse(request, "checkout.html", {})


@router.get("/order/{ref}", response_class=HTMLResponse)
async def order_confirm(request: Request, ref: str):
    result = db.get_order(ref)
    if not result:
        return HTMLResponse("Order not found", status_code=404)
    return templates.TemplateResponse(request, "order-confirm.html", {
        "order": result["order"],
        "items": result["items"],
    })


# ── API ───────────────────────────────────────────────────────────────────────

@router.post("/api/checkout")
async def do_checkout(payload: CheckoutPayload):
    items = []
    for ci in payload.items:
        product = ALL_PRODUCTS.get(ci.slug)
        if not product:
            return JSONResponse({"error": f"Unknown product: {ci.slug}"}, status_code=400)
        items.append({
            "slug": ci.slug,
            "name": product["name"],
            "price": product["price"],
            "qty": ci.qty,
        })
    if not items:
        return JSONResponse({"error": "Cart is empty"}, status_code=400)

    ref = db.create_order(payload.model_dump(), items)
    return {"ref": ref}


@router.post("/api/ratings")
async def post_rating(payload: RatingPayload):
    if payload.stars not in range(1, 6):
        return JSONResponse({"error": "Stars must be 1–5"}, status_code=400)
    db.add_rating(payload.slug, payload.stars, payload.review)
    return db.get_ratings(payload.slug)


@router.get("/api/ratings/{slug}")
async def get_rating(slug: str):
    return db.get_ratings(slug)
