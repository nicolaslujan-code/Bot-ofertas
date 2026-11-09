import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
QUERY_ENV = os.environ.get("QUERY", "ofertas, gaming, electronica, ps5, bazar, muebles, zapatillas adidas")
PRECIO_MAX = float(os.environ.get("PRECIO_MAX", "999999999"))

vistos = set()

def enviar_alerta(titulo, precio, link, porcentaje):
    mensaje = f"🚨 **¡OFERTA ENCONTRADA ({int(porcentaje)}% OFF)!** 🚨\n\n📌 {titulo}\n💰 Precio: ${precio:,.2f}\n🔗 {link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

def buscar():
    categorias = [cat.strip() for cat in QUERY_ENV.split(",")]
    
    for termino in categorias:
        url = f"https://api.mercadolibre.com/sites/MLA/search?q={termino}&sort=price_asc"
        try:
            resp = requests.get(url).json()
            items = resp.get("results", [])
            
            for item in items[:15]:
                item_id = item.get("id")
                precio = item.get("price")
                titulo = item.get("title")
                link = item.get("permalink")
                precio_original = item.get("original_price")
                
                if item_id not in vistos:
                    if precio_original and precio and precio <= PRECIO_MAX:
                        descuento = ((precio_original - precio) / precio_original) * 100
                        if descuento >= 35:
                            enviar_alerta(titulo, precio, link, descuento)
                            vistos.add(item_id)
        except Exception as e:
            print(f"Error buscando {termino}: {e}")

if __name__ == "__main__":
    buscar()
