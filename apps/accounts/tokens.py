from datetime import timedelta
from django.utils import timezone


def token_is_expired(token):
    expiration_time = token.created_at + timedelta(minutes=30)
    return timezone.now() > expiration_time