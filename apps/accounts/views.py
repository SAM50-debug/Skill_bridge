from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .forms import EmailLoginForm, SignUpForm
from .models import EmailVerificationToken, User
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

        try:
            send_verification_email(user, token_obj.token)
        except Exception:
            # Don't break signup if SMTP is temporarily down
            messages.warning(
                request,
                "Account created, but verification email could not be sent right now. Use 'Resend verification' to try again.",
            )

        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("interest")

    return render(request, "accounts/signup.html", {"form": form})


@require_http_methods(["GET", "POST"])
def resend_verification_view(request):
    """
    Public resend endpoint (no login required) to avoid deadlock:
    user can't login until verified, so resend must not require auth.
    Security: always returns a generic success message (no user enumeration).
    """
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()

        try:
            user = User.objects.get(email__iexact=email)

            if not user.is_verified:
                token_obj, _ = EmailVerificationToken.objects.update_or_create(
                    user=user,
                    defaults={"is_used": False},
                )

                try:
                    send_verification_email(user, token_obj.token)
                except Exception:
                    # swallow SMTP errors; still show generic message
                    pass

        except User.DoesNotExist:
            pass

        messages.success(
            request,
            "If the email exists, a verification link has been sent. Please check your inbox/spam.",
        )
        return redirect("resend_verification")

    return render(request, "accounts/resend_verification.html")


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
        return redirect("resend_verification")

    user = verification.user
    user.is_verified = True
    user.save(update_fields=["is_verified"])

    verification.is_used = True
    verification.save()

    messages.success(request, "Email verified. You can now log in.")
    return redirect("login")