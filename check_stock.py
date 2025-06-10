import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

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
        soup = BeautifulSoup(response.text, "html.parser")
        buttons = soup.find_all("button")
        sold_out = any("sold out" in btn.get_text(strip=True).lower() for btn in buttons)
        return not sold_out
    except Exception as e:
        print(f"[ERROR] Failed to check stock: {e}")
        return False

def send_email():
    sender_email = os.environ["EMAIL_SENDER"]
    receiver_email = os.environ["EMAIL_RECEIVER"]
    password = os.environ["EMAIL_PASSWORD"]

    subject = "Sayaka 100g is BACK IN STOCK!"
    body = "💚 Sayaka 100g Matcha is available now: https://ippodotea.com/collections/matcha/products/sayaka-100g"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

if True:
    send_email()
else:
    print("Still sold out.")
