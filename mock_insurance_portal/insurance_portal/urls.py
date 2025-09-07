# insurance_portal/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.eligibility_index, name='eligibility_index'),  
    path('check-eligibility/', views.check_eligibility_with_credentials, name='check_eligibility_with_credentials'),
    path('<str:patient_id>/', views.patient_eligibility, name='patient_eligibility'),
    
]
