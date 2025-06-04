from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from payments.models import Payment
from leases.models import Lease
from properties.models import Building, Unit
import pandas as pd
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io

@login_required
def reports_dashboard(request):
    return render(request, "reports/reports_dashboard.html")

@login_required
def payments_report(request):
    payments = Payment.objects.select_related('lease', 'lease__tenant').order_by('-date')
    return render(request, "reports/payments_report.html", {"payments": payments})

@login_required
def leases_report(request):
    user = request.user
    leases = Lease.objects.select_related('tenant', 'unit').all()

    # Role-based filtering
    if hasattr(user, "role"):
        if user.role == "tenant":
            leases = leases.filter(tenant=user)
        elif user.role == "landlord":
            leases = leases.filter(unit__property__landlord=user)
        elif user.role == "agent":
            leases = leases.filter(unit__property__agent=user)
        elif user.role == "caretaker":
            leases = leases.filter(unit__property__caretaker=user)

    # Filtering
    tenant = request.GET.get('tenant')
    unit = request.GET.get('unit')
    status = request.GET.get('status')
    if tenant:
        leases = leases.filter(tenant__username__icontains=tenant)
    if unit:
        leases = leases.filter(unit__unit_number__icontains=unit)
    if status == "active":
        leases = leases.filter(is_active=True)
    elif status == "ended":
        leases = leases.filter(is_active=False)

    # Count for chart (filtered by role)
    active_count = leases.filter(is_active=True).count()
    ended_count = leases.filter(is_active=False).count()

    export = request.GET.get('export')
    if export == 'excel':
        df = pd.DataFrame(list(leases.values('tenant__username', 'unit__unit_number', 'start_date', 'end_date', 'is_active')))
        df.rename(columns={'tenant__username': 'Tenant', 'unit__unit_number': 'Unit', 'start_date': 'Start Date', 'end_date': 'End Date', 'is_active': 'Active'}, inplace=True)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="leases_report.xlsx"'
        df.to_excel(response, index=False)
        return response
    elif export == 'pdf':
        html = render_to_string("reports/leases_report.html", {"leases": leases, "active_count": active_count, "ended_count": ended_count, "request": request})
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="leases_report.pdf"'
        pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=response)
        return response

    return render(request, "reports/leases_report.html", {"leases": leases, "active_count": active_count, "ended_count": ended_count})

@login_required
def properties_report(request):
    user = request.user
    buildings = Building.objects.all()

    # Role-based filtering
    if hasattr(user, "role"):
        if user.role == "landlord":
            buildings = buildings.filter(landlord=user)
        elif user.role == "agent":
            buildings = buildings.filter(agent=user)
        elif user.role == "caretaker":
            buildings = buildings.filter(caretaker=user)
        elif user.role == "tenant":
            buildings = buildings.filter(unit__lease__tenant=user).distinct()

    # Filtering
    name = request.GET.get('name')
    location = request.GET.get('location')
    if name:
        buildings = buildings.filter(name__icontains=name)
    if location:
        buildings = buildings.filter(address__icontains=location)

    # Prepare occupancy data for chart/table
    properties = []
    for building in buildings:
        total_units = Unit.objects.filter(building=building).count()
        occupied_units = Lease.objects.filter(unit__building=building, is_active=True).count()
        vacant_units = total_units - occupied_units
        properties.append({
            "name": building.name,
            "location": building.address,
            "total_units": total_units,
            "occupied_units": occupied_units,
            "vacant_units": vacant_units,
        })

    export = request.GET.get('export')
    if export == 'excel':
        df = pd.DataFrame(properties)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="properties_report.xlsx"'
        df.to_excel(response, index=False)
        return response
    elif export == 'pdf':
        html = render_to_string("reports/properties_report.html", {"properties": properties, "request": request})
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="properties_report.pdf"'
        pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=response)
        return response

    return render(request, "reports/properties_report.html", {"properties": properties})
