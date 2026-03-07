from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from .models import User

from .forms import (
    EmailLoginForm,
    SignUpStep1Form,
    SignUpStep2Form,
    SignUpStep3Form,
    SignUpStep4Form,
)


SIGNUP_SESSION_KEY = "signup_data"


def _get_signup_data(request):
    return request.session.get(SIGNUP_SESSION_KEY, {})


def _update_signup_data(request, step_data):
    data = _get_signup_data(request)
    data.update(step_data)
    request.session[SIGNUP_SESSION_KEY] = data
    request.session.modified = True


def _clear_signup_data(request):
    if SIGNUP_SESSION_KEY in request.session:
        del request.session[SIGNUP_SESSION_KEY]
        request.session.modified = True


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    form = EmailLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        login(request, user)
        return redirect("dashboard_home")

    return render(request, "accounts/login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def signup_step1_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    form = SignUpStep1Form(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data.copy()

        profile_picture = request.FILES.get("profile_picture")
        if profile_picture:
            data["profile_picture_name"] = profile_picture.name
            request.session["signup_profile_picture_temp"] = profile_picture.name

        _update_signup_data(
            request,
            {
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "dob": str(data["dob"]),
                "phone": data["phone"],
                "email": data["email"],
            },
        )

        # keep uploaded file temporarily in request.FILES flow for now
        if profile_picture:
            request.session["signup_has_profile_picture"] = True

        return redirect("signup_step2")

    return render(request, "accounts/signup_step1.html", {"form": form, "step": 1})


@require_http_methods(["GET", "POST"])
def signup_step2_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if "email" not in _get_signup_data(request):
        return redirect("signup_step1")

    form = SignUpStep2Form(request.POST or None)

    if request.method == "POST" and form.is_valid():
        _update_signup_data(
            request,
            {
                "college": form.cleaned_data["college"],
                "course": form.cleaned_data["course"],
                "year": form.cleaned_data["year"],
                "cgpa": str(form.cleaned_data["cgpa"]),
            },
        )
        return redirect("signup_step3")

    return render(request, "accounts/signup_step2.html", {"form": form, "step": 2})


@require_http_methods(["GET", "POST"])
def signup_step3_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if "college" not in _get_signup_data(request):
        return redirect("signup_step2")

    form = SignUpStep3Form(request.POST or None)

    if request.method == "POST" and form.is_valid():
        _update_signup_data(
            request,
            {
                "password1": form.cleaned_data["password1"],
                "password2": form.cleaned_data["password2"],
            },
        )
        return redirect("signup_step4")

    return render(request, "accounts/signup_step3.html", {"form": form, "step": 3})


@require_http_methods(["GET", "POST"])
def signup_step4_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    signup_data = _get_signup_data(request)
    if "password1" not in signup_data:
        return redirect("signup_step3")

    form = SignUpStep4Form(request.POST or None)

    if request.method == "POST" and form.is_valid():
        _update_signup_data(
            request,
            {
                "preferred_category": form.cleaned_data["preferred_category"],
                "interested_fields": form.cleaned_data["interested_fields"],
                "preferred_location": form.cleaned_data["preferred_location"],
                "skills": form.cleaned_data["skills"],
            },
        )

        final_data = _get_signup_data(request)

        try:
            user = User.objects.create_user(
                username=final_data["email"].lower(),
                email=final_data["email"].lower(),
                password=final_data["password1"],
                first_name=final_data["first_name"],
                last_name=final_data["last_name"],
                dob=final_data["dob"],
                phone=final_data["phone"],
                college=final_data["college"],
                course=final_data["course"],
                year=final_data["year"],
                department="",
                cgpa=final_data["cgpa"],
                preferred_category=final_data["preferred_category"],
                interested_fields=final_data.get("interested_fields", ""),
                preferred_location=final_data["preferred_location"],
                skills=final_data.get("skills", ""),
                is_active=True,
                is_verified=False,
            )

            # legacy compatibility only
            if final_data["preferred_category"] == "job":
                user.interest = "job"
            elif final_data["preferred_category"] == "internship":
                user.interest = "internship"
            else:
                user.interest = None

            user.save()
            login(request, user)
            _clear_signup_data(request)

            messages.success(request, "Account created successfully.")
            return redirect("dashboard_home")

        except Exception:
            messages.error(request, f"Something went wrong while creating your account: {e}")
            return redirect("signup_step1")

    return render(request, "accounts/signup_step4.html", {"form": form, "step": 4})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def interest_view(request):
    if request.user.interest == "job":
        return redirect("/dashboard/jobs/")
    if request.user.interest == "internship":
        return redirect("/dashboard/internships/")

    if request.method == "POST":
        interest = request.POST.get("interest")

        if interest in ["job", "internship"]:
            request.user.interest = interest
            request.user.save(update_fields=["interest"])

            if interest == "job":
                return redirect("/dashboard/jobs/")
            if interest == "internship":
                return redirect("/dashboard/internships/")

    return render(request, "accounts/interest.html")