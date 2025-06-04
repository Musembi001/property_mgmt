from django.shortcuts import render
from properties.models import Property, Unit
from accounts.models import User
from leases.models import Lease
from payments.models import Payment
from maintenance.models import MaintenanceRequest
from django.db import models
from django.db.models.functions import TruncMonth
from django.utils import timezone
import calendar
from dateutil.relativedelta import relativedelta  # <-- Add this import
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Core metrics
    properties_count = Property.objects.count()
    tenants_count = User.objects.filter(role="tenant").count()
    leases_count = Lease.objects.count()
    payments_total = Payment.objects.filter(status='paid').aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
    maintenance_count = MaintenanceRequest.objects.count()

    # Occupancy
    occupied_units = Unit.objects.filter(is_occupied=True).count()
    vacant_units = Unit.objects.filter(is_occupied=False).count()

    # Revenue trends (real aggregation by month)
    today = timezone.now().date().replace(day=1)
    months = []
    month_labels = []
    for i in range(5, -1, -1):
        month = today - relativedelta(months=i)
        months.append(month)
        month_labels.append(month.strftime('%b'))

    # Aggregate revenue per month
    revenue_qs = (
        Payment.objects.filter(status='paid', date__isnull=False, date__gte=months[0])
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=models.Sum('amount'))
        .order_by('month')
    )
    # Prepare data for chart
    month_map = {r['month'].strftime('%b'): float(r['total']) for r in revenue_qs if r['month']}
    revenue_data = [month_map.get(label, 0) for label in month_labels]

    # Debug prints
    print("Revenue months:", month_labels)
    print("Revenue data:", revenue_data)

    # Recent leases
    recent_leases = Lease.objects.select_related('unit', 'tenant').order_by('-start_date')[:5]

    context = {
        "properties_count": properties_count,
        "tenants_count": tenants_count,
        "leases_count": leases_count,
        "payments_total": payments_total,
        "maintenance_count": maintenance_count,
        "occupied_units": occupied_units,
        "vacant_units": vacant_units,
        "revenue_months": month_labels,
        "revenue_data": revenue_data,
        "recent_leases": recent_leases,
    }
    return render(request, 'dashboard.html', context)