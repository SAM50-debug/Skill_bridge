from django.urls import path
from .views import login_view, signup_view, logout_view, interest_view, verify_email

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("interest/", interest_view, name="interest"),
    path("verify-email/<uuid:token>/", verify_email, name="verify_email"),
]