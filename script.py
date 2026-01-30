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
    api_key = os.environ.get('FINNHUB_KEY', '').strip()
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('c'), data.get('d'), data.get('dp')
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None, None

def send_daily_report(price, dollar_change, percent_change):
    # ניקוי משתנים מרווחים וירידות שורה
    email_user = os.environ.get('EMAIL_USER', '').strip()
    email_pass = os.environ.get('EMAIL_PASS', '').strip()
    dest_email = os.environ.get('PERSONAL_EMAIL', '').strip()
    
    # בדיקה שהכתובות לא ריקות
    if not email_user or not dest_email:
        print(f"ERROR: Missing email addresses. User: '{email_user}', Dest: '{dest_email}'")
        return

    today_date = datetime.now().strftime("%d/%m/%Y")
    msg = EmailMessage()
    
    if price and price != 0:
        total_value = price * MY_SHARES_COUNT
        p_change_dollars = (dollar_change or 0) * MY_SHARES_COUNT
        status = "עליה 🟢" if (percent_change or 0) > 0 else "ירידה 🔴"
        
        subject = f"דוח {MY_STOCK_SYMBOL} ליום {today_date} | {percent_change}%"
        body = f"שלום יואל,\n\nנתוני {MY_STOCK_SYMBOL} ל-{today_date}:\n\nמחיר: ${price}\nשינוי: {percent_change}% ({status})\n\nשווי תיק: ${total_value:,.2f}\nשינוי דולרי: ${p_change_dollars:,.2f}"
    else:
        subject = f"תקלה בנתוני {MY_STOCK_SYMBOL}"
        body = "לא התקבלו נתונים מ-Finnhub."

    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = dest_email

    print(f"Sending email to {dest_email}...")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
        print("Success: Email sent!")
    except Exception as e:
        print(f"SMTP Error: {e}")

def main():
    price, d_change, p_change = get_stock_data(MY_STOCK_SYMBOL)
    send_daily_report(price, d_change, p_change)

if __name__ == "__main__":
    main()
