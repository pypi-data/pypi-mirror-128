# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail  # noqa: F401


def get_email_sender(api_key):
    return SendGridAPIClient(api_key)
