import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv  
load_dotenv()  # Load environment variables from .env file
app_password = os.getenv("app_password")
sender_email = os.getenv("sender_email")
def send_email(recipient_email, subject, body):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade to a secure connection
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        return {"status": "success", "message": "Email sent successfully!"}
    except Exception as e:
        return {"status": "failed", "message": f"Failed to send email: {e}"}