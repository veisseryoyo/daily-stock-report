import requests
import os
from datetime import datetime

def get_stock_data(symbol):
    api_key = os.environ.get('FINNHUB_KEY', '').strip()
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('c'), data.get('d'), data.get('dp')
    except:
        return None, None, None

def send_via_brevo(price, dollar_change, percent_change):
    api_key = os.environ.get('BREVO_API_KEY', '').strip()
    dest_email = os.environ.get('PERSONAL_EMAIL', '').strip()
    
    today = datetime.now().strftime("%d/%m/%Y")
    total_value = price * 24
    status = "עליה 🟢" if percent_change > 0 else "ירידה 🔴"

    url = "https://api.brevo.com/v3/smtp/email"
    
    payload = {
        "sender": {"name": "Yoyo Stocks", "email": "yoyo.stocks.market@gmail.com"},
        "to": [{"email": dest_email}],
        "subject": f"דוח AT&T ליום {today} | {percent_change}%",
        "textContent": (
            f"שלום יואל,\n\n"
            f"נתוני AT&T (סימול: T) ליום {today}:\n"
            f"מחיר מניה: ${price}\n"
            f"שינוי יומי: {percent_change}% ({status})\n\n"
            f"התיק שלך (24 מניות):\n"
            f"שינוי בשווי: ${dollar_change * 24:,.2f}\n"
            f"שווי כולל: ${total_value:,.2f}"
        )
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Success! Email sent via Brevo API.")
    else:
        print(f"Failed: {response.status_code}, {response.text}")

def main():
    price, d_change, p_change = get_stock_data("T")
    if price:
        send_via_brevo(price, d_change, p_change)

if __name__ == "__main__":
    main()
