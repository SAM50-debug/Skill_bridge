from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.conf import settings


class User(AbstractUser):

    email = models.EmailField(unique=True)

    YEAR_CHOICES = [
        ("7", "7"),
        ("8", "8"),
        ("passed", "Passed"),
    ]

    INTEREST_CHOICES = [
        ("job", "Job"),
        ("internship", "Internship"),
    ]

    dob = models.DateField(null=True, blank=True)

    course = models.CharField(max_length=150)

    year = models.CharField(
        max_length=10,
        choices=YEAR_CHOICES
    )

    department = models.CharField(max_length=150)

    college = models.CharField(max_length=255)

    phone = models.CharField(max_length=20)

    interest = models.CharField(
        max_length=20,
        choices=INTEREST_CHOICES,
        null=True,
        blank=True
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

#Email verification
class EmailVerificationToken(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification_token"
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Verification token for {self.user.email}"