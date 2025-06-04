"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.db import models  # <-- Add this import
from properties.models import Property
from leases.models import Lease
from payments.models import Payment
from maintenance.models import MaintenanceRequest

def dashboard(request):
    properties_count = Property.objects.count()
    tenants_count = Lease.objects.values('tenant').distinct().count()
    leases_count = Lease.objects.count()
    payments_total = Payment.objects.filter(status='paid').aggregate(total=models.Sum('amount'))['total'] or 0
    maintenance_count = MaintenanceRequest.objects.count()
    recent_leases = Lease.objects.select_related('tenant', 'unit').order_by('-start_date')[:5]

    # Example for occupancy and revenue charts
    occupied_units = Lease.objects.filter(is_active=True).count()
    vacant_units = Property.objects.count() - occupied_units
    revenue_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    revenue_data = [120000, 135000, 128000, 140000, 150000, 160000]  # Replace with real data if needed

    context = {
        'properties_count': properties_count,
        'tenants_count': tenants_count,
        'leases_count': leases_count,
        'payments_total': payments_total,
        'maintenance_count': maintenance_count,
        'recent_leases': recent_leases,
        'occupied_units': occupied_units,
        'vacant_units': vacant_units,
        'revenue_months': revenue_months,
        'revenue_data': revenue_data,
    }
    return render(request, "dashboard.html", context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('properties/', include('properties.urls')),
    path('leases/', include('leases.urls')),
    path('payments/', include('payments.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('reports/', include('reports.urls')),
    path('notifications/', include('notifications.urls')),
    path('documents/', include('documents.urls')),
    path('auditlog/', include('auditlog.urls')),
    path('support/', include('support.urls')),
    path('feedback/', include('feedback.urls')),
    path('calendar/', include('calendarapp.urls')),
    path('expenses/', include('expenses.urls')),
    path('parking/', include('parking.urls')),
    path('visitors/', include('visitors.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('', dashboard, name='home'),  # Root URL shows dashboard
]
