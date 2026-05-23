"""Admin routes — order dashboard at /admin."""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import database as db

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

ADMIN_PASS = "slumber2026"   # ← change this before going live!
STATUSES   = ["pending", "confirmed", "shipped", "delivered", "cancelled"]


@router.get("", response_class=HTMLResponse)
async def admin_dashboard(request: Request, status: str = ""):
    orders = db.list_orders(status or None)
    return templates.TemplateResponse(request, "admin.html", {
        "orders": orders,
        "statuses": STATUSES,
        "current_status": status,
    })


@router.get("/{ref}", response_class=HTMLResponse)
async def admin_order(request: Request, ref: str):
    result = db.get_order(ref)
    if not result:
        return HTMLResponse("Order not found", status_code=404)
    return templates.TemplateResponse(request, "admin-order.html", {
        "order": result["order"],
        "items": result["items"],
        "statuses": STATUSES,
    })


@router.post("/{ref}/status")
async def update_status(ref: str, status: str = Form(...)):
    db.update_order_status(ref, status)
    return RedirectResponse(f"/admin/{ref}", status_code=303)
