import requests
import smtplib
import os
from email.message import EmailMessage

def send_email(subject, body):
    email_user = os.environ.get('EMAIL_USER')
    email_pass = os.environ.get('EMAIL_PASS')
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = email_user

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)

def main():
    print("Starting script...")
    symbol = "TSLA"
    api_key = os.environ.get('FINNHUB_KEY')
    
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        price = data.get('c', 0)
        
        # גם אם המחיר הוא 0 (כי השוק סגור), נשלח מייל לבדיקה
        subject = f"בדיקת מערכת: {symbol}"
        body = f"הסקריפט רץ בהצלחה!\nמחיר נוכחי שנמצא: ${price}"
        
        send_email(subject, body)
        print("Email sent!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
