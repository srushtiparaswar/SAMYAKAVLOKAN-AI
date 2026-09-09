import sqlite3
from datetime import datetime
import smtplib
from email.message import EmailMessage
from twilio.rest import Client

# =========================
# EMAIL CONFIG
# =========================

EMAIL_ADDRESS = "samyakavlokan.ai@gmail.com"
EMAIL_PASSWORD = "xxxx"




# =========================
# DATABASE EVENT LOGGER
# =========================

def log_event(event_type, person_count, alert_status):

    conn = sqlite3.connect("samyakavlokan.db")
    cursor = conn.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO events
    (timestamp, event_type, person_count, alert_status)
    VALUES (?, ?, ?, ?)
    """,
    (
        current_time,
        event_type,
        person_count,
        alert_status
    ))

    conn.commit()
    conn.close()

    print("Event Saved Successfully")


# =========================
# EMAIL + SMS ALERT
# =========================

def send_alert():

    try:
        # EMAIL ALERT

        msg = EmailMessage()

        msg["Subject"] = "SAMYAKAVLOKAN ALERT"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        msg.set_content("""
HELP Gesture Detected!

Immediate Attention Required.

SAMYAKAVLOKAN AI
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("Email Alert Sent Successfully")

    except Exception as e:
        print("Email Error:", e)

    try:
        # SMS ALERT

        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages.create(
            body="HELP Gesture Detected! - SAMYAKAVLOKAN AI",
            from_=TWILIO_NUMBER,
            to=RECEIVER_NUMBER
        )

        print("SMS Sent Successfully")
        print(message.sid)

    except Exception as e:
        print("SMS Error:", e)