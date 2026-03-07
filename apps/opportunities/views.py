from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Opportunity, Application
from .utils import send_application_confirmation_email


@login_required
def opportunity_detail(request, pk):
    op = get_object_or_404(Opportunity, pk=pk)

    expired = timezone.now() > op.deadline
    already_applied = Application.objects.filter(
        user=request.user,
        opportunity=op,
    ).exists()

    return render(
        request,
        "opportunities/detail.html",
        {
            "op": op,
            "expired": expired,
            "already_applied": already_applied,
        },
    )


@login_required
def apply_to_opportunity(request, pk):
    if request.method != "POST":
        return redirect("opportunity_detail", pk=pk)

    op = get_object_or_404(Opportunity, pk=pk)

    if op.status != "published":
        messages.error(request, "This opportunity is not available for applications.")
        return redirect("opportunity_detail", pk=pk)

    if timezone.now() > op.deadline:
        messages.error(request, "This opportunity has expired.")
        return redirect("opportunity_detail", pk=pk)

    application, created = Application.objects.get_or_create(
        user=request.user,
        opportunity=op,
        defaults={
            "status": "applied",
            "confirmation_email_sent": False,
        },
    )

    if not created:
        messages.info(request, "You have already applied to this opportunity.")
        return redirect("opportunity_detail", pk=pk)

    try:
        send_application_confirmation_email(request.user, op)
        application.confirmation_email_sent = True
        application.save(update_fields=["confirmation_email_sent"])
    except Exception:
        messages.warning(
            request,
            "Application saved, but confirmation email could not be sent right now.",
        )

    messages.success(request, "Application submitted successfully.")
    return redirect("opportunity_detail", pk=pk)