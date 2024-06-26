from core.services.send_email import send_email
from eventify.celery import app


@app.task
def send_email_task(email: str, subject: str, message: str) -> str:
    return send_email(email, subject, message)
