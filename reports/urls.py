from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_dashboard, name='reports_dashboard'),
    path('payments/', views.payments_report, name='payments_report'),
    path('leases/', views.leases_report, name='leases_report'),
    path('properties/', views.properties_report, name='properties_report'),
]