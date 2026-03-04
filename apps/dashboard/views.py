from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from apps.opportunities.models import Opportunity


@login_required
def job_dashboard(request):
    items = Opportunity.objects.filter(
        category="job",
        status="published",
        deadline__gte=timezone.now(),
    ).order_by("-featured", "-created_at")

    return render(request, "dashboard/jobs.html", {"items": items})


@login_required
def internship_dashboard(request):
    items = Opportunity.objects.filter(
        category="internship",
        status="published",
        deadline__gte=timezone.now(),
    ).order_by("-featured", "-created_at")

    return render(request, "dashboard/internships.html", {"items": items})