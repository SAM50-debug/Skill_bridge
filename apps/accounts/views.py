from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .forms import EmailLoginForm, SignUpForm
from .models import EmailVerificationToken
from .tokens import token_is_expired
from .utils import send_verification_email


@require_http_methods(["GET", "POST"])
def login_view(request):
    # If already logged in, go where they should be
    if request.user.is_authenticated:
        if request.user.interest == "job":
            return redirect("/dashboard/jobs/")
        if request.user.interest == "internship":
            return redirect("/dashboard/internships/")
        return redirect("interest")

    form = EmailLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        login(request, user)

        # If interest already chosen, skip interest page
        if user.interest == "job":
            return redirect("/dashboard/jobs/")
        if user.interest == "internship":
            return redirect("/dashboard/internships/")

        return redirect("interest")

    return render(request, "accounts/login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.user.is_authenticated:
        if request.user.interest == "job":
            return redirect("/dashboard/jobs/")
        if request.user.interest == "internship":
            return redirect("/dashboard/internships/")
        return redirect("interest")

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()

        token_obj, _ = EmailVerificationToken.objects.update_or_create(
            user=user,
            defaults={"is_used": False},
        )

        send_verification_email(user, token_obj.token)

        return render(request, "accounts/verify_pending.html", {"email": user.email})

    return render(request, "accounts/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def interest_view(request):
    # If already chosen, skip
    if request.user.interest == "job":
        return redirect("/dashboard/jobs/")
    if request.user.interest == "internship":
        return redirect("/dashboard/internships/")

    if request.method == "POST":
        interest = request.POST.get("interest")

        if interest in ["job", "internship"]:
            request.user.interest = interest
            request.user.save()

            if interest == "job":
                return redirect("/dashboard/jobs/")
            if interest == "internship":
                return redirect("/dashboard/internships/")

    return render(request, "accounts/interest.html")


def verify_email(request, token):
    verification = get_object_or_404(EmailVerificationToken, token=token)

    if verification.is_used:
        messages.error(request, "Verification link already used.")
        return redirect("login")

    if token_is_expired(verification):
        messages.error(request, "Verification link expired. Please request a new one.")
        return redirect("login")  # we'll add resend page next

    user = verification.user
    user.is_active = True
    user.is_verified = True
    user.save()

    verification.is_used = True
    verification.save()

    messages.success(request, "Email verified. You can now log in.")
    return redirect("login")