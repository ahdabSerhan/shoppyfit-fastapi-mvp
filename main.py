
import os, json
from typing import Optional, List
from fastapi import FastAPI, Query, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ShoppyFit Retail Agentic AI API", version="1.0.0")

# --- Optional API key protection (set SHOPPYFIT_API_KEY env var to enable) ---
API_KEY = os.getenv("SHOPPYFIT_API_KEY")
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

# --- CORS (safe to leave open for MVP; tighten later) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load minimal catalog ---
with open("products.json") as f:
    PRODUCTS = json.load(f)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}

@app.get("/api/products")
def search_products(
    query: str,
    max_price: float = None,
    brand: str = None,
    size: str = None,
    limit: int = 5
):
    results = []
    for p in PRODUCTS:
        if query.lower() not in p["title"].lower() and query.lower() not in p["description"].lower():
            continue
        if max_price and p["price"] > max_price:
            continue
        if brand and p["brand"].lower() != brand.lower():
            continue
        if size and size not in p.get("sizes", []):
            continue
        results.append(p)
    return results[:limit]

@app.get("/api/products/{product_id}", tags=["catalog"], dependencies=[Depends(verify_api_key)])
def get_product(product_id: str):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")
