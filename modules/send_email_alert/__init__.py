from dotenv import dotenv_values
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config = dotenv_values(
    "C:/Users/eviadmin/Documents/Datawarehouse/test_schedule_scripts/From_BC/python/.env")

# Replace these with your Office 365 email credentials


def send_email(subject, body, to_emails=["ntellez@evi-ind.com"], email_user=config["email_user"], email_pass=config["email_pass"]):
    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = email_user
    message["To"] = ", ".join(to_emails)
    message["Subject"] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server for Office 365
    smtp_server = "smtp.office365.com"
    port = 587  # StartTLS port

    context = ssl.create_default_context()

    # Create an SMTP session
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(email_user, email_pass)
        server.sendmail(email_user, to_emails, message.as_string())


if __name__ == "__main__":
    # Replace these with your Office 365 email credentials
    email_user = config["email_user"]
    email_pass = config["email_pass"]

    email_subject = "Test Email from Python"
    email_body = "This is a test email sent from Python using Office 365."

    send_email(email_subject, email_body)
