import smtplib
from email.mime.text import MIMEText

def send_email():
    sender_email = os.environ["EMAIL_SENDER"]
    receiver_email = os.environ["EMAIL_RECEIVER"]
    password = os.environ["EMAIL_PASSWORD"]

    subject = "Sayaka 100g is BACK IN STOCK!"
    body = "💚 https://ippodotea.com/collections/matcha/products/sayaka-100g"

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
        print(f"Email failed: {e}")
