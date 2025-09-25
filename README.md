
# ShoppyFit FastAPI MVP (Retail Agentic AI)

Minimal API to power a Custom GPT action that returns product cards (with images + try-on links).

## 1) Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (optional) protect with an API key
export SHOPPYFIT_API_KEY=mysecret   # Windows PowerShell: $env:SHOPPYFIT_API_KEY="mysecret"

uvicorn main:app --reload --port 8000
```

Test:
- Health: http://localhost:8000/
- Search: http://localhost:8000/api/products?query=dress&max_price=300

If you set an API key, call with header: `X-API-Key: mysecret`

## 2) Deploy to Render (recommended MVP)

1. Push this folder to a new GitHub repo.
2. Go to https://dashboard.render.com -> New -> Web Service -> Connect your repo.
3. Environment: **Python**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. (Optional) In "Environment" set env var `SHOPPYFIT_API_KEY` to protect your API.
5. Deploy. Copy your live URL, e.g. `https://shoppyfit-mvp.onrender.com`

## 3) Update the OpenAPI Schema

Edit `openapi.yaml` and replace:
```yaml
servers:
  - url: https://REPLACE-WITH-YOUR-RENDER-URL
```
with your live Render URL (e.g., `https://shoppyfit-mvp.onrender.com`), then save.

## 4) Connect to ChatGPT (Custom GPT)

1. In ChatGPT, go to **Explore GPTs** → **Create**.
2. Give it a name & instructions, e.g.:
   ```
   When showing products, format as a shopping card:
   - Title in bold
   - Price in bold with 💲
   - Fit recommendation
   - Inline image from `image_url`
   - "👉 Try it on your avatar" link from `tryon_url`
   ```
3. Open the **Actions** tab → **Add Action** → **Import from OpenAPI schema** → upload `openapi.yaml`.
4. If you set an API key on Render, configure **Authentication**:
   - Type: **API Key**
   - Header name: `X-API-Key`
   - Value: your key (e.g., `mysecret`)
5. Save your GPT.

## 5) Test in ChatGPT

Ask:
- "Find me a red dress under $300"
- "Show Nike sneakers under $150 in size 9"
- "Adidas sneakers under $120?"

The GPT will call your `/api/products` endpoint and render cards with images and try-on links.

## Notes
- This MVP serves static `products.json`. Replace it later with a database or live connectors.
- CORS is open for convenience; restrict it for production.
- Optional: add `/api/products/{id}` for details (already included).
