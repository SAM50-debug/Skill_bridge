from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook

from .models import Opportunity, Application


def export_applications_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "applications"

    headers = [
        "company_name",
        "opportunity_title",
        "category",
        "student_name",
        "student_email",
        "student_phone",
        "college",
        "course",
        "year",
        "cgpa",
        "preferred_category",
        "preferred_location",
        "application_status",
        "confirmation_email_sent",
        "applied_at",
    ]
    ws.append(headers)

    for app in queryset.select_related("user", "opportunity").order_by("id"):
        user = app.user
        opportunity = app.opportunity
        ws.append([
            opportunity.company_name,
            opportunity.title,
            opportunity.category,
            f"{user.first_name} {user.last_name}".strip(),
            user.email,
            user.phone,
            user.college,
            user.course,
            user.year,
            str(user.cgpa) if user.cgpa is not None else "",
            user.preferred_category,
            user.preferred_location,
            app.status,
            "yes" if app.confirmation_email_sent else "no",
            app.applied_at.isoformat() if app.applied_at else "",
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="applications.xlsx"'
    wb.save(response)
    return response


export_applications_to_excel.short_description = "Export selected applications to Excel (.xlsx)"


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company_name",
        "category",
        "location",
        "minimum_cgpa",
        "deadline",
        "status",
        "featured",
    )
    list_filter = ("category", "status", "featured")
    search_fields = ("title", "company_name", "location", "field_tags", "eligible_programs")
    ordering = ("-featured", "-created_at")
    list_editable = ("status", "featured")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "opportunity",
        "status",
        "confirmation_email_sent",
        "applied_at",
    )
    list_filter = (
        "status",
        "confirmation_email_sent",
        "opportunity__company_name",
        "opportunity__category",
    )
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "opportunity__title",
        "opportunity__company_name",
    )
    ordering = ("-applied_at",)
    actions = [export_applications_to_excel]