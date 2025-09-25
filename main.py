
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

@app.get("/api/products", tags=["catalog"], dependencies=[Depends(verify_api_key)])
def search_products(
    query: str = Query(..., description="Search keyword, e.g. 'dress' or 'sneakers'"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    brand: Optional[str] = Query(None, description="Brand name filter (e.g., 'Nike', 'Adidas', 'Mayes NYC')"),
    size: Optional[str] = Query(None, description="Size filter (e.g., 'M' or '10')")
) -> List[dict]:
    results = []
    q = query.lower()
    for p in PRODUCTS:
        # text match
        if q not in p["title"].lower() and q not in p["description"].lower():
            continue
        # price
        if max_price is not None and p["price"] > max_price:
            continue
        # brand
        if brand and p["brand"].lower() != brand.lower():
            continue
        # size
        if size and size not in p.get("sizes", []):
            continue
        results.append(p)
    return results

@app.get("/api/products/{product_id}", tags=["catalog"], dependencies=[Depends(verify_api_key)])
def get_product(product_id: str):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")
