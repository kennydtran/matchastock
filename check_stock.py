import requests
from bs4 import BeautifulSoup
import os
from twilio.rest import Client

URL = "https://ippodotea.com/collections/matcha/products/sayaka-100g"

def check_stock():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        buttons = soup.find_all("button")
        sold_out = any("sold out" in btn.get_text(strip=True).lower() for btn in buttons)
        return not sold_out
    except Exception as e:
        print(f"[ERROR] Failed to check stock: {e}")
        return False

def send_sms():
    try:
        client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_AUTH"])
        message = client.messages.create(
            body="📦 Sayaka 100g Matcha is BACK IN STOCK! Order here: https://ippodotea.com/collections/matcha/products/sayaka-100g",
            from_=os.environ["TWILIO_FROM"],
            to=os.environ["MY_PHONE"]
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"[ERROR] Failed to send SMS: {e}")

if check_stock():
    send_sms()
else:
    print("Still sold out.")
