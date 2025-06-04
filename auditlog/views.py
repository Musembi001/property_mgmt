from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AuditLog

@login_required
def auditlog_list(request):
    user = request.user
    if user.is_superuser or user.is_staff:
        logs = AuditLog.objects.all().order_by('-timestamp')[:200]
    elif hasattr(user, "role") and user.role == "landlord":
        property_ids = user.building_set.values_list('id', flat=True)
        logs = AuditLog.objects.filter(property_id__in=property_ids).order_by('-timestamp')[:200]
    elif hasattr(user, "role") and user.role == "agent":
        property_ids = user.agent_buildings.values_list('id', flat=True)
        logs = AuditLog.objects.filter(property_id__in=property_ids).order_by('-timestamp')[:200]
    elif hasattr(user, "role") and user.role == "caretaker":
        property_ids = user.caretaker_buildings.values_list('id', flat=True)
        logs = AuditLog.objects.filter(property_id__in=property_ids).order_by('-timestamp')[:200]
    elif hasattr(user, "role") and user.role == "tenant":
        logs = AuditLog.objects.filter(user=user).order_by('-timestamp')[:200]
    else:
        logs = AuditLog.objects.filter(user=user).order_by('-timestamp')[:200]
    # Limit to the last 200 logs for performance
    if request.GET.get('q'):
        query = request.GET.get('q')
        logs = logs.filter(object_repr__icontains=query)
    return render(request, "auditlog/auditlog_list.html", {"logs": logs})

