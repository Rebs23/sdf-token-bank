
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
bank_ledger = {"admin_sonora": 100000000} # 100 millones de tokens iniciales para el Comandante

LOW_FUEL_THRESHOLD = 500000 # Alerta cuando queden menos de 500k tokens

def send_admin_alert(user_id, remaining):
    """Simula el envío de una alerta al Comandante."""
    msg = f"⚠️ ALERTA DE COMBUSTIBLE: Al usuario '{user_id}' solo le quedan {remaining} tokens."
    print(f"\n[NOTIFICACIÓN ENVIADA AL ADMIN] {msg}")
    # Aquí podrías añadir una llamada a Telegram, Discord o Email API

class TokenRequest(BaseModel):
    user_id: str
    amount_to_burn: int

@app.post("/v1/use-tokens")
def burn_tokens(req: TokenRequest):
    balance = bank_ledger.get(req.user_id, 0)
    
    if balance < req.amount_to_burn:
        raise HTTPException(status_code=402, detail="Inyeccion de Tokens requerida")
    
    bank_ledger[req.user_id] -= req.amount_to_burn
    new_balance = bank_ledger[req.user_id]

    # Disparar alerta si el combustible es bajo
    if new_balance < LOW_FUEL_THRESHOLD:
        send_admin_alert(req.user_id, new_balance)

    return {"status": "BURNED", "remaining": new_balance, "latency": "45ms"}

@app.get("/")
def health():
    return {"bank": "SDF Token Bank", "status": "Online"}
