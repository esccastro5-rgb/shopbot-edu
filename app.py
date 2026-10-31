from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time, hashlib, hmac, requests, uvicorn, os

app = FastAPI(title="Shopbot Shopee Affiliate API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

APP_ID = os.getenv("SHOPEE_APP_ID", "18345391314")
SECRET = os.getenv("SHOPEE_SECRET", "6725SZ3YRZPDP52Q6KKEMAOSYTJHX5AD")
GRAPHQL_URL = "https://open-api.affiliate.shopee.com.br/graphql"

def generate_signature(app_id, secret, timestamp):
    payload = f"{app_id}{timestamp}"
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return sig

@app.get("/")
def home():
    return {"status": "Shopbot API Online", "app_id": APP_ID}

@app.get("/api/products")
def get_products(limit: int = 20):
    timestamp = int(time.time())
    sig = generate_signature(APP_ID, SECRET, timestamp)
    headers = {"Content-Type": "application/json", "Authorization": f"SHA256 Credential={APP_ID}, Timestamp={timestamp}, Signature={sig}"}
    query = f"query {{ productOfferV2(listType: 0, sortType: 2, limit: {limit}) {{ nodes {{ productName imageUrl priceMin commissionRate offerLink }} }} }}"
    try:
        resp = requests.post(GRAPHQL_URL, json={"query": query}, headers=headers, timeout=15)
        return {"success": True, "shopee_response": resp.json(), "link": "https://s.shopee.com.br/9KjDHIgdYK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
