import requests
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime

# --- הגדרות התיק שלך ---
MY_STOCK_SYMBOL = "T"      # AT&T
MY_SHARES_COUNT = 24       # כמות מניות
# ---------------------

def get_stock_data(symbol):
    api_key = os.environ.get('FINNHUB_KEY')
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        # c = מחיר נוכחי, d = שינוי דולרי למניה אחת, dp = אחוז שינוי
        return data.get('c'), data.get('d'), data.get('dp')
    except:
        return None, None, None

def send_daily_report(price, dollar_change, percent_change):
    email_user = os.environ.get('EMAIL_USER')
    email_pass = os.environ.get('EMAIL_PASS')
    dest_email = os.environ.get('PERSONAL_EMAIL')
    
    # תאריך של היום
    today_date = datetime.now().strftime("%d/%m/%Y")
    
    if price and price != 0:
        total_value = price * MY_SHARES_COUNT
        # חישוב בכמה השווי הכולל עלה או ירד היום (שינוי למניה * כמות מניות)
        portfolio_change_dollars = dollar_change * MY_SHARES_COUNT
        
        status = "עליה 🟢" if percent_change > 0 else "ירידה 🔴"
        
        subject = f"דוח {MY_STOCK_SYMBOL} ליום {today_date} | {percent_change}%"
        body = f"""
שלום יואל,

להלן סיכום הנתונים למניית {MY_STOCK_SYMBOL} לתאריך {today_date}:

📈 נתוני שוק:
מחיר מניה: ${price}
שינוי יומי: {percent_change}% ({status})

💰 נתוני התיק שלך (אחזקה של {MY_SHARES_COUNT} מניות):
שינוי בשווי התיק היום: ${portfolio_change_dollars:,.2f}
שווי כולל של הפוזיציה: ${total_value:,.2f}

בברכה,
מערכת Yoyo Stocks Market
        """
    else:
        subject = f"תקלה בנתוני {MY_STOCK_SYMBOL} - {today_date}"
        body = "לא הצלחנו למשוך נתונים עדכניים. וודא שחיבור ה-API תקין."

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = f"Yoyo Stocks <{email_user}>"
    msg['To'] = dest_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)

def main():
    price, dollar_change, percent_change = get_stock_data(MY_STOCK_SYMBOL)
    send_daily_report(price, dollar_change, percent_change)
    print(f"Report sent for {today_date}")

if __name__ == "__main__":
    main()
