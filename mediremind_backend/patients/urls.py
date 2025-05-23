from django.urls import path
from .views import patient_dashboard, patient_profile, update_patient_profile

urlpatterns = [
    path('dashboard/', patient_dashboard, name='patient_dashboard'),
    path('profile/', patient_profile, name='patient_profile'),
    path('profile/update/', update_patient_profile, name='update_patient_profile'),
]
