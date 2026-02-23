import os
import stripe
from dotenv import load_dotenv

# 1. Cargar Credenciales (.env)
load_dotenv()

# Configuramos la API Key de Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def generate_token_link():
    print("[*] SDF: Generando Link de $10 para Token Bank...")
    try:
        # A. Crear el Producto
        product = stripe.Product.create(
            name="SDF Token Bank: Explorer Pack",
            description="1,000,000 High-Velocity Agentic Tokens",
        )

        # B. Crear el Precio ($10.00 USD)
        price = stripe.Price.create(
            product=product.id,
            unit_amount=1000, # $10.00 USD
            currency="usd",
        )

        # C. Crear el Payment Link
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
            after_completion={"type": "redirect", "redirect": {"url": "https://sdf-token-bank.vercel.app"}},
        )

        # Formateo de salida seguro
        separador = "=" * 60
        print("\n" + separador)
        print("SUCCESS: Link de $10 Creado:")
        print(payment_link.url)
        print(separador)
        
        # D. Inyección Automática en index.html
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        # Reemplazamos el link viejo de $50 por el nuevo de $10
        new_html = html.replace('https://buy.stripe.com/6oU3cwd79cTqetQ6w80ZW00', payment_link.url)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_html)
            
        print("\n[✔] SDF: index.html actualizado con el nuevo precio.")

    except Exception as e:
        print("\n[✘] ERROR CRÍTICO: " + str(e))

if __name__ == "__main__":
    generate_token_link()
