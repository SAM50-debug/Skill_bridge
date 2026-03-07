from django.urls import path
from .views import (
    login_view,
    logout_view,
    interest_view,
    signup_step1_view,
    signup_step2_view,
    signup_step3_view,
    signup_step4_view,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("interest/", interest_view, name="interest"),

    path("signup/step-1/", signup_step1_view, name="signup_step1"),
    path("signup/step-2/", signup_step2_view, name="signup_step2"),
    path("signup/step-3/", signup_step3_view, name="signup_step3"),
    path("signup/step-4/", signup_step4_view, name="signup_step4"),

    # convenience route
    path("signup/", signup_step1_view, name="signup"),
]