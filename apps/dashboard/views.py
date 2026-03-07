from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.opportunities.models import Application, Opportunity


def _with_applied_ids(user, items):
    applied_ids = set(
        Application.objects.filter(
            user=user,
            opportunity__in=items,
        ).values_list("opportunity_id", flat=True)
    )
    return applied_ids


@login_required
def dashboard_home(request):
    choice = request.user.preferred_category or request.user.interest

    if choice == "job":
        return redirect("job_dashboard")

    if choice == "internship":
        return redirect("internship_dashboard")

    if choice == "both":
        return redirect("dashboard_all")

    return redirect("signup_step4")


@login_required
def job_dashboard(request):
    items = Opportunity.objects.filter(
        category="job",
        status="published",
        deadline__gte=timezone.now(),
    ).order_by("-featured", "-created_at")

    applied_ids = _with_applied_ids(request.user, items)

    return render(
        request,
        "dashboard/jobs.html",
        {
            "items": items,
            "applied_ids": applied_ids,
        },
    )


@login_required
def internship_dashboard(request):
    items = Opportunity.objects.filter(
        category="internship",
        status="published",
        deadline__gte=timezone.now(),
    ).order_by("-featured", "-created_at")

    applied_ids = _with_applied_ids(request.user, items)

    return render(
        request,
        "dashboard/internships.html",
        {
            "items": items,
            "applied_ids": applied_ids,
        },
    )


@login_required
def dashboard_all(request):
    job_items = Opportunity.objects.filter(
        category="job",
        status="published",
        deadline__gte=timezone.now(),
    ).order_by("-featured", "-created_at")

    internship_items = Opportunity.objects.filter(
        category="internship",
        status="published",
        deadline__gte=timezone.now(),
    ).order_by("-featured", "-created_at")

    all_items = Opportunity.objects.filter(
        status="published",
        deadline__gte=timezone.now(),
    ).order_by("-featured", "-created_at")

    applied_ids = _with_applied_ids(request.user, all_items)

    return render(
        request,
        "dashboard/all.html",
        {
            "job_items": job_items,
            "internship_items": internship_items,
            "all_items": all_items,
            "applied_ids": applied_ids,
        },
    )