from django.conf import settings
from django.core.mail import send_mail, get_connection


def send_verification_email(user, token):
    verification_link = f"{settings.SITE_URL}/verify-email/{token}/"

    subject = "Verify your SkillBridge account"
    message = f"""Hello {user.first_name},

Please verify your email by clicking the link below:

{verification_link}

This link will expire in 30 minutes.

SkillBridge Team
"""

    # timeout prevents hanging forever
    connection = get_connection(timeout=15)

    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
        connection=connection,
    )