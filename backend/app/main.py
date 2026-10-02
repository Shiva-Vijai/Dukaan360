from datetime import datetime, timezone
import os
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import data
from .schemas import CreateSale, StockChange, ProductCreate, ContactRequest, CustomerCreate, Repayment

app = FastAPI(title="Dukaan360 API", version="0.1.0")


def cors_origins():
    configured = os.getenv("CORS_ALLOWED_ORIGINS", "*").strip()
    if not configured or configured == "*":
        return ["*"]
    return [origin.strip().rstrip("/") for origin in configured.split(",") if origin.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_methods=["*"],
    allow_headers=["*"],
)

def product_or_404(product_id: str):
    product = next((p for p in data.products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(404, "Product not found")
    return product

def status_for(product):
    if product["id"] == "biscuits": return "Slow Moving"
    if product["id"] == "oil5" and product["quantity"] >= 20: return "Overstock"
    days = product["quantity"] / product["daily_demand"] if product["daily_demand"] else 999
    if days <= 1.5: return "Critical"
    if days <= 4: return "Low Stock"
    return "Healthy"

def enrich(product):
    result = dict(product)
    result["status"] = status_for(product)
    result["days_remaining"] = round(product["quantity"] / product["daily_demand"], 1) if product["daily_demand"] else None
    return result

def customers():
    with data.con() as c: return [__import__('json').loads(x[0]) for x in c.execute("SELECT payload FROM customers").fetchall()]

def save_customer(customer):
    import json
    with data.con() as c: c.execute("INSERT OR REPLACE INTO customers VALUES (?,?)",(customer["phone"],json.dumps(customer)))

def customer_or_404(phone):
    customer=next((x for x in customers() if x["phone"]==phone),None)
    if not customer: raise HTTPException(404,"Customer not found")
    return customer

@app.get("/health")
def health(): return {"status": "ok"}

@app.get("/products")
def list_products(q: str = ""):
    return [enrich(p) for p in data.products if q.lower() in p["name"].lower()]

@app.get("/products/barcode/{barcode}")
def get_by_barcode(barcode: str):
    product = next((p for p in data.products if p["barcode"] == barcode), None)
    if not product: raise HTTPException(404, "Barcode not found")
    return enrich(product)

@app.post("/products", status_code=201)
def create_product(request: ProductCreate):
    if any(p["barcode"] == request.barcode for p in data.products):
        raise HTTPException(409, "A product with this barcode already exists")
    product = {"id": uuid4().hex[:8], **request.model_dump(exclude={"initial_stock"}), "quantity": request.initial_stock, "daily_demand": 0.5, "status": "Healthy"}
    data.products.append(product)
    data.persist_products()
    return enrich(product)

@app.post("/inventory/{product_id}/add")
def add_stock(product_id: str, change: StockChange):
    p = product_or_404(product_id); p["quantity"] += change.quantity; data.persist_products()
    return enrich(p)

@app.get("/analytics/dashboard")
def dashboard():
    today_total = sum(s["total"] for s in data.sales) + 4820
    low = [enrich(p) for p in data.products if status_for(p) in ("Low Stock", "Critical")]
    return {"today_sales": today_total, "bills": len(data.sales) + 37, "products": len(data.products), "low_stock": len(low), "insights": insights()["insights"]}

@app.get("/analytics/insights")
def insights():
    milk = product_or_404("milk"); oil = product_or_404("oil5"); biscuits = product_or_404("biscuits")
    milk_days = round(milk["quantity"] / milk["daily_demand"], 1)
    return {"insights": [
        {"type": "stockout", "title": f"{milk['name']} may run out in {milk_days} days", "detail": f"Current stock: {milk['quantity']} • Average daily demand: {milk['daily_demand']}", "action": "Recommended order: 15 units"},
        {"type": "excess", "title": "Cooking Oil 5L is overstocked", "detail": f"{oil['quantity']} tins in stock with low recent demand.", "action": "18 units above projected requirement"},
        {"type": "slow", "title": "Premium Biscuits are slow moving", "detail": f"{biscuits['quantity']} packs in stock; only 2 sold in 14 days.", "action": "₹1,200 capital may be tied up"},
    ]}

@app.get("/merchant-network/opportunities")
def opportunities():
    return [
        {"id": "opp-oil", "merchant": "Ravi Stores", "product": "Cooking Oil 5L", "needs": 10, "your_excess": 18, "distance": "1.8 km", "status": "Open"},
        {"id": "opp-milk", "merchant": "Lakshmi Mart", "product": "Milk 1L", "needs": 15, "your_excess": 0, "distance": "2.4 km", "status": "Open"},
    ]

@app.post("/merchant-network/{opportunity_id}/contact")
def contact_merchant(opportunity_id: str, request: ContactRequest):
    if opportunity_id not in {"opp-oil", "opp-milk"}: raise HTTPException(404, "Opportunity not found")
    return {"status": "sent", "opportunity_id": opportunity_id, "message": "Demo contact request recorded. No real message was sent.", "note": request.note}

@app.get("/sales")
def list_sales():
    return list(reversed(data.sales))

@app.get("/customers")
def list_customers(): return customers()

@app.post("/customers",status_code=201)
def create_customer(request: CustomerCreate):
    if any(x["phone"]==request.phone for x in customers()): raise HTTPException(409,"Customer phone number already exists")
    customer={"phone":request.phone,"name":request.name,"due":0,"created_at":datetime.now(timezone.utc).isoformat()}
    save_customer(customer);return customer

@app.post("/customers/{phone}/repay")
def repay(phone: str, request: Repayment):
    customer=customer_or_404(phone);customer["due"]=round(max(0,customer["due"]-request.amount),2);save_customer(customer)
    return {"customer":customer,"message":"Repayment recorded"}

@app.get("/customers/{phone}/recommendations")
def recommendations(phone: str):
    customer_or_404(phone)
    counts={}
    for sale in data.sales:
        if sale.get("customer_phone")==phone and sale.get("payment_status")=="completed":
            for item in sale["items"]: counts[item["name"]]=counts.get(item["name"],0)+item["quantity"]
    ranked=sorted(counts,key=counts.get,reverse=True)[:3]
    return {"customer_phone":phone,"products":ranked or ["Milk 1L","Sugar 1kg"],"message":"Demo recommendation based on purchase history."}

@app.post("/customers/{phone}/engagement")
def engagement(phone: str):
    customer=customer_or_404(phone);r=recommendations(phone)
    return {"status":"queued_demo","message":f"Buy-again reminder prepared for {customer['name']}: Your usual {r['products'][0]} is available.","disclosure":"No SMS, WhatsApp, or push notification was actually sent."}

@app.post("/customers/engagement/remind-all")
def remind_all_customers():
    audience = customers()
    return {"status":"queued_demo","customer_count":len(audience),"message":f"Prepared personalised buy-again reminders for {len(audience)} customer(s).","disclosure":"Demo only: no SMS, WhatsApp, or push notification was actually sent."}

@app.post("/sales")
def create_sale(request: CreateSale):
    items, total = [], 0
    for line in request.items:
        if not line.product_id:
            if not line.name or line.unit_price is None: raise HTTPException(400, "Manual item needs name and unit price")
            items.append({"product_id": None, "name": line.name, "quantity": line.quantity, "unit_price": line.unit_price, "manual": True})
            total += line.unit_price * line.quantity
            continue
        p = product_or_404(line.product_id)
        if p["quantity"] < line.quantity: raise HTTPException(400, f"Insufficient stock for {p['name']}")
        items.append({"product_id": p["id"], "name": p["name"], "quantity": line.quantity, "unit_price": p["price"]})
        total += p["price"] * line.quantity
    if request.customer_phone and not any(x["phone"]==request.customer_phone for x in customers()):
        if not request.customer_name: raise HTTPException(400,"New customer needs a name")
        save_customer({"phone":request.customer_phone,"name":request.customer_name,"due":0,"created_at":datetime.now(timezone.utc).isoformat()})
    sale = {"id": f"D360-{1000 + len(data.sales) + 1}", "items": items, "total": total, "payment_status": "pending", "payment_method":request.payment_method,"customer_phone":request.customer_phone}
    data.sales.append(sale)
    data.persist_sales()
    return sale

@app.post("/payments/simulate/{sale_id}")
def simulate_payment(sale_id: str):
    sale = next((s for s in data.sales if s["id"] == sale_id), None)
    if not sale: raise HTTPException(404, "Sale not found")
    if sale["payment_status"] == "completed": return sale
    for item in sale["items"]:
        if item["product_id"]: product_or_404(item["product_id"])["quantity"] -= item["quantity"]
    if sale.get("customer_phone") and sale.get("payment_method")=="credit":
        customer=customer_or_404(sale["customer_phone"]);customer["due"]=round(customer["due"]+sale["total"],2);save_customer(customer)
    sale.update({"payment_status": "completed", "transaction_id": f"D360-TXN-{uuid4().hex[:6].upper()}", "completed_at": datetime.now(timezone.utc).isoformat()})
    data.persist_products(); data.persist_sales()
    return sale

@app.post("/demo/reset")
def reset():
    data.reset_demo(); return {"message": "Demo data reset"}
