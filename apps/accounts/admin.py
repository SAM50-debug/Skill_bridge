from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook

from .models import User


def export_students_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "students"

    headers = [
        "first_name",
        "last_name",
        "dob",
        "course",
        "year",
        "department",
        "college",
        "phone",
        "email",
        "interest",
        "is_verified",
        "created_at",
    ]
    ws.append(headers)

    for u in queryset.order_by("id"):
        ws.append([
            u.first_name,
            u.last_name,
            u.dob.isoformat() if u.dob else "",
            u.course,
            u.year,
            u.department,
            u.college,
            u.phone,
            u.email,
            u.interest or "",
            "yes" if u.is_verified else "no",
            u.created_at.isoformat() if u.created_at else "",
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="students.xlsx"'
    wb.save(response)
    return response


export_students_to_excel.short_description = "Export selected students to Excel (.xlsx)"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "college",
        "course",
        "year",
        "is_verified",
        "interest",
    )
    search_fields = ("email", "first_name", "last_name", "college", "department")
    list_filter = ("year", "interest", "is_verified", "department", "college")
    actions = [export_students_to_excel]