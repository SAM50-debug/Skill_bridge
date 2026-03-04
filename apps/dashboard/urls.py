from django.urls import path
from .views import job_dashboard, internship_dashboard

urlpatterns = [
    path("jobs/", job_dashboard),
    path("internships/", internship_dashboard),
]