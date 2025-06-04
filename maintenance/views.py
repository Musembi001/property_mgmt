from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MaintenanceRequest
from .forms import MaintenanceRequestForm

@login_required
def maintenance_list(request):
    user = request.user
    if user.role == "caretaker":
        # Only show requests for units in buildings this caretaker manages
        requests = MaintenanceRequest.objects.filter(unit__building__caretaker=user)
    elif user.role == "tenant":
        # Only show requests submitted by this tenant
        requests = MaintenanceRequest.objects.filter(requested_by=user)
    elif user.role == "landlord":
        # Only show requests for properties owned by this landlord
        requests = MaintenanceRequest.objects.filter(unit__building__landlord=user)
    elif user.role == "agent":
        # Only show requests for properties managed by this agent
        requests = MaintenanceRequest.objects.filter(unit__building__agent=user)
    else:
        requests = MaintenanceRequest.objects.none()
    return render(request, "maintenance/maintenance_list.html", {"requests": requests})

@login_required
def maintenance_add(request):
    if request.method == "POST":
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.requested_by = request.user
            req.save()
            return redirect("maintenance_list")
    else:
        form = MaintenanceRequestForm()
    return render(request, "maintenance/maintenance_add.html", {"form": form})

@login_required
def maintenance_detail(request, pk):
    req = get_object_or_404(MaintenanceRequest, pk=pk)
    return render(request, "maintenance/maintenance_detail.html", {"request_obj": req})
