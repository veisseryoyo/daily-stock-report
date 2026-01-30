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

def send_to_discord(message):
    webhook_url = os.environ.get('DISCORD_WEBHOOK', '').strip()
    payload = {"content": message}
    requests.post(webhook_url, json=payload)

def main():
    symbol = "T" # AT&T
    shares = 24
    price, d_change, p_change = get_stock_data(symbol)
    
    if price:
        today = datetime.now().strftime("%d/%m/%Y")
        total_value = price * shares
        portfolio_change = d_change * shares
        
        status_icon = "🚀" if p_change > 0 else "🔻"
        color_line = "------------------------------------"
        
        msg = (
            f"**{status_icon} דוח יומי: {symbol} ({today})**\n"
            f"{color_line}\n"
            f"💰 **מחיר מניה:** `${price}`\n"
            f"📈 **שינוי יומי:** `{p_change}%`\n"
            f"{color_line}\n"
            f"💼 **התיק של יהונתן (24 מניות):**\n"
            f"💵 **שווי כולל:** `${total_value:,.2f}`\n"
            f"💸 **רווח/הפסד יומי:** `${portfolio_change:,.2f}`\n"
            f"{color_line}"
        )
        
        send_to_discord(msg)
        print("המייל נשלח לדיסקורד בהצלחה!")
    else:
        print("שגיאה במשיכת הנתונים.")

if __name__ == "__main__":
    main()
