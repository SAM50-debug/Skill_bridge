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

    # add index
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)

    location = models.CharField(max_length=255, default="Not specified")

    description = models.TextField()
    apply_link = models.URLField()

    # add index
    deadline = models.DateTimeField(db_index=True)

    # add index
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        db_index=True,
    )

    # add index
    featured = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.deadline

    def __str__(self):
        return f"{self.title} @ {self.company_name}"