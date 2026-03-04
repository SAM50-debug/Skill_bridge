from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Opportunity


def opportunity_detail(request, pk):
    op = get_object_or_404(Opportunity, pk=pk)

    expired = timezone.now() > op.deadline
    return render(request, "opportunities/detail.html", {"op": op, "expired": expired})