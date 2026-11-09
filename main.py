import os
import requests
import time

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
QUERY = os.environ.get("QUERY", "RTX 4060")
PRECIO_MAX = float(os.environ.get("PRECIO_MAX", "450000"))

vistos = set()

def enviar_alerta(titulo, precio, link):
    mensaje = f"🚨 **¡OFERTA ENCONTRADA!** 🚨\n\n📌 {titulo}\n💰 Precio: ${precio:,.2f}\n🔗 {link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

def buscar():
    url = f"https://api.mercadolibre.com/sites/MLA/search?q={QUERY}&sort=price_asc"
    resp = requests.get(url).json()
    items = resp.get("results", [])
    
    for item in items[:15]:
        item_id = item.get("id")
        precio = item.get("price")
        titulo = item.get("title")
        link = item.get("permalink")
        
        if item_id not in vistos:
            if precio and precio <= PRECIO_MAX:
                enviar_alerta(titulo, precio, link)
                vistos.add(item_id)

if __name__ == "__main__":
    print("Bot iniciado correctamente...")
    while True:
        try:
            buscar()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(300)
