from django.urls import path
from .views import (
    dashboard_home,
    dashboard_all,
    job_dashboard,
    internship_dashboard,
)

urlpatterns = [
    path("", dashboard_home, name="dashboard_home"),
    path("all/", dashboard_all, name="dashboard_all"),
    path("jobs/", job_dashboard, name="job_dashboard"),
    path("internships/", internship_dashboard, name="internship_dashboard"),
]