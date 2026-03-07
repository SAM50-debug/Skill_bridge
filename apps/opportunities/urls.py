from django.urls import path
from .views import opportunity_detail, apply_to_opportunity

urlpatterns = [
    path("<int:pk>/", opportunity_detail, name="opportunity_detail"),
    path("<int:pk>/apply/", apply_to_opportunity, name="apply_to_opportunity"),
]