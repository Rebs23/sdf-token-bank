
import os
import time
import stripe
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
app = FastAPI(title="SDF Token Bank")

# --- BANCO DE TOKENS (Simulado) ---
bank_ledger = {"admin_sonora": 5000000} # 5 millones de tokens iniciales

class TokenRequest(BaseModel):
    user_id: str
    amount_to_burn: int

@app.post("/v1/use-tokens")
def burn_tokens(req: TokenRequest):
    balance = bank_ledger.get(req.user_id, 0)
    if balance < req.amount_to_burn:
        raise HTTPException(status_code=402, detail="Inyeccion de Tokens requerida")
    
    bank_ledger[req.user_id] -= req.amount_to_burn
    return {"status": "BURNED", "remaining": bank_ledger[req.user_id], "latency": "45ms"}

@app.get("/")
def health():
    return {"bank": "SDF Token Bank", "status": "Online"}
