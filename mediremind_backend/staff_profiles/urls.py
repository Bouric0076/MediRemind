from django.urls import path
from .views import staff_dashboard, staff_profile, update_staff_profile

urlpatterns = [
    path('dashboard/', staff_dashboard, name='staff_dashboard'),
    path('profile/', staff_profile, name='staff_profile'),
    path('profile/update/', update_staff_profile, name='update_staff_profile'),
]
