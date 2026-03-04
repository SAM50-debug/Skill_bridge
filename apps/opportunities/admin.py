from django.contrib import admin
from .models import Opportunity


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company_name",
        "category",
        "location",
        "deadline",
        "status",
        "featured",
    )
    list_filter = ("category", "status", "featured")
    search_fields = ("title", "company_name", "location")
    ordering = ("-featured", "-created_at")