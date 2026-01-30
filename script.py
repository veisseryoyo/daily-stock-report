import requests
import smtplib
import os
from email.message import EmailMessage

# 1. הגדרות - נתונים שנמשכים מה-Secrets של GitHub
FINNHUB_API_KEY = os.environ.get('FINNHUB_KEY')
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
TARGET_SYMBOL = "TSLA"  # שנה כאן לכל מניה שתרצה, למשל AAPL או NVDA

def get_stock_data(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    # c = Current Price, dp = Percent Change
    return data.get('c'), data.get('dp')

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # שולח לעצמך

    # חיבור לשרת של גוגל
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def main():
    try:
        price, change = get_stock_data(TARGET_SYMBOL)
        
        if price:
            status = "עליה" if change > 0 else "ירידה"
            message = f"דוח מניית {TARGET_SYMBOL}:\n\nמחיר נוכחי: ${price}\nשינוי יומי: {change}%\nמגמה: {status}"
            subject = f"דוח יומי: {TARGET_SYMBOL} ({change}%)"
            
            send_email(subject, message)
            print(f"Success! Report sent for {TARGET_SYMBOL}")
        else:
            print("Could not fetch data from Finnhub.")
            
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
