from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.conf import settings


class User(AbstractUser):
    YEAR_CHOICES = [
        ("7", "7"),
        ("8", "8"),
        ("passed", "Passed"),
    ]

    INTEREST_CHOICES = [
        ("job", "Job"),
        ("internship", "Internship"),
    ]

    PREFERRED_CATEGORY_CHOICES = [
        ("job", "Job"),
        ("internship", "Internship"),
        ("both", "Both"),
    ]

    PREFERRED_LOCATION_CHOICES = [
        ("remote", "Remote"),
        ("onsite", "On-site"),
        ("hybrid", "Hybrid"),
        ("any", "Any"),
    ]

    email = models.EmailField(unique=True)

    dob = models.DateField(null=True, blank=True)
    course = models.CharField(max_length=150)
    year = models.CharField(max_length=10, choices=YEAR_CHOICES)
    department = models.CharField(max_length=150, blank=True, default="")
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

    profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)

    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    preferred_category = models.CharField(
        max_length=20,
        choices=PREFERRED_CATEGORY_CHOICES,
        default="both",
        blank=True,
    )

    interested_fields = models.TextField(blank=True)
    preferred_location = models.CharField(
        max_length=20,
        choices=PREFERRED_LOCATION_CHOICES,
        default="any",
        blank=True,
    )
    skills = models.TextField(blank=True)

    def __str__(self):
        return self.email


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