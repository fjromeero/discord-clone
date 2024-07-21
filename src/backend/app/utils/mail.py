from dataclasses import dataclass
from datetime import datetime, timedelta
import emails
import logging
from pathlib import Path
from typing import Any

from jinja2 import Template
import resend

from app.core.config import settings


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent.parent / "email-templates" / "build" / template_name
    ).read_text()

    html_content = Template(template_str).render(context)
    return html_content


def generate_reset_password_email(email_to: str, username: str, token: str) -> EmailData:
    project_name= settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {username}"
    link = f"{settings.server_host}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": project_name,
            "username": username,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,        
        },
    )

    return EmailData(html_content=html_content, subject=subject)


def send_email(
    *,
    email_to: str,
    subject: str,
    html_content: str,
) -> None:
    
    params: resend.Emails.SendParams = {
        "from": f"Discord Clone Support <{settings.SMTP_SENDER}>",
        "to": [email_to],
        "subject": subject,
        "html": html_content,
    }

    email: resend.Email = resend.Emails.send(params)
    logging.info(f"sent email result: {email}")