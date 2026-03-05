from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from apps.opportunities.models import Opportunity


@login_required
def job_dashboard(request):
    q = request.GET.get("q", "").strip()
    featured = request.GET.get("featured", "").strip()

    items = Opportunity.objects.filter(
        category="job",
        status="published",
        deadline__gte=timezone.now(),
    )

    if q:
        items = items.filter(Q(title__icontains=q) | Q(company_name__icontains=q))

    if featured == "1":
        items = items.filter(featured=True)

    items = items.order_by("-featured", "-created_at")

    return render(request, "dashboard/jobs.html", {
        "items": items,
        "q": q,
        "featured": featured,
    })


@login_required
def internship_dashboard(request):
    q = request.GET.get("q", "").strip()
    featured = request.GET.get("featured", "").strip()

    items = Opportunity.objects.filter(
        category="internship",
        status="published",
        deadline__gte=timezone.now(),
    )

    if q:
        items = items.filter(Q(title__icontains=q) | Q(company_name__icontains=q))

    if featured == "1":
        items = items.filter(featured=True)

    items = items.order_by("-featured", "-created_at")

    return render(request, "dashboard/internships.html", {
        "items": items,
        "q": q,
        "featured": featured,
    })

@login_required
def dashboard_home(request):
    user = request.user

    if user.interest == "job":
        return redirect("/dashboard/jobs/")

    if user.interest == "internship":
        return redirect("/dashboard/internships/")

    return redirect("/interest/")