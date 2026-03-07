from django.conf import settings
from django.core.mail import get_connection, send_mail


def send_application_confirmation_email(user, opportunity):
    subject = f"Application received - {opportunity.title}"
    message = f"""Hello {user.first_name or user.email},

Your application has been recorded successfully.

Opportunity: {opportunity.title}
Company: {opportunity.company_name}
Category: {opportunity.category.title()}
Location: {opportunity.location}

Thank you,
SkillBridge Team
"""

    connection = get_connection(timeout=10)

    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        connection=connection,
    )