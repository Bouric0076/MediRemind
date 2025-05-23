from django.urls import path
from .views import staff_dashboard

urlpatterns = [
    path("dashboard/", staff_dashboard),
]
