from django.conf import settings
from django.db import models
from django.utils import timezone


class Opportunity(models.Model):
    CATEGORY_CHOICES = [
        ("job", "Job"),
        ("internship", "Internship"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)

    company_logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    attachment = models.FileField(upload_to="attachments/", null=True, blank=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    location = models.CharField(max_length=255, default="Not specified")

    description = models.TextField()
    apply_link = models.URLField(blank=True)

    deadline = models.DateTimeField(db_index=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        db_index=True,
    )
    featured = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # New recommendation / eligibility fields
    minimum_requirements_text = models.TextField(blank=True)
    minimum_cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    eligible_years = models.CharField(max_length=100, blank=True)
    eligible_programs = models.CharField(max_length=255, blank=True)
    field_tags = models.CharField(max_length=255, blank=True)

    def is_expired(self):
        return timezone.now() > self.deadline

    def __str__(self):
        return f"{self.title} @ {self.company_name}"


class Application(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("reviewed", "Reviewed"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    confirmation_email_sent = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "opportunity"],
                name="unique_user_opportunity_application",
            )
        ]
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.user.email} -> {self.opportunity.title}"