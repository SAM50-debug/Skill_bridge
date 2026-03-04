from django.urls import path
from .views import opportunity_detail

urlpatterns = [
    path("<int:pk>/", opportunity_detail, name="opportunity_detail"),
]