from dotenv import dotenv_values
import requests

config = dotenv_values(
    "C:/Users/eviadmin/Documents/Datawarehouse/test_schedule_scripts/From_BC/python/.env"
)


def send_email(
    subject,
    body,
    to_emails=["ntellez@evi-ind.com"],
    api_key=config["smtp2go_api_key"],
    sender=config["email_user"],
):
    """
    Sends an email via the SMTP2GO API (replaces the old Office 365
    SMTP basic-auth flow, which Microsoft now rejects with a 535 error).
    """
    url = "https://api.smtp2go.com/v3/email/send"
    headers = {
        "Content-Type": "application/json",
        "X-Smtp2go-Api-Key": api_key,
        "accept": "application/json",
    }
    payload = {
        "sender": sender,
        "to": to_emails,
        "subject": subject,
        "text_body": body,
    }

    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()  # raises an exception on 4xx/5xx
    return response.json()


if __name__ == "__main__":
    email_subject = "Test Email from Python"
    email_body = "This is a test email sent via SMTP2GO API."
    result = send_email(email_subject, email_body)
    print(result)
