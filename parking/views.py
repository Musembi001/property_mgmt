from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ParkingSlot, ParkingAssignment
from .forms import ParkingAssignmentForm

@login_required
def parking_slot_list(request):
    user = request.user
    if hasattr(user, "role"):
        if user.role == "tenant":
            slots = ParkingSlot.objects.filter(parkingassignment__user=user).distinct()
        elif user.role == "landlord":
            slots = ParkingSlot.objects.filter(property__landlord=user).distinct()
        elif user.role == "agent":
            slots = ParkingSlot.objects.filter(property__agent=user).distinct()
        elif user.role == "caretaker":
            slots = ParkingSlot.objects.filter(property__caretaker=user).distinct()
        else:
            slots = ParkingSlot.objects.none()
    else:
        slots = ParkingSlot.objects.none()
    return render(request, "parking/parking_slot_list.html", {"slots": slots})

@login_required
def parking_assignment_list(request):
    user = request.user
    if hasattr(user, "role"):
        if user.role == "tenant":
            assignments = ParkingAssignment.objects.filter(user=user).select_related('slot', 'user').order_by('-assigned_at')
        elif user.role == "landlord":
            assignments = ParkingAssignment.objects.filter(slot__property__landlord=user).select_related('slot', 'user').order_by('-assigned_at')
        elif user.role == "agent":
            assignments = ParkingAssignment.objects.filter(slot__property__agent=user).select_related('slot', 'user').order_by('-assigned_at')
        elif user.role == "caretaker":
            assignments = ParkingAssignment.objects.filter(slot__property__caretaker=user).select_related('slot', 'user').order_by('-assigned_at')
        else:
            assignments = ParkingAssignment.objects.none()
    else:
        assignments = ParkingAssignment.objects.none()
    return render(request, "parking/parking_assignment_list.html", {"assignments": assignments})

@login_required
def parking_assign(request):
    if not hasattr(request.user, "role") or request.user.role not in ["landlord", "agent"]:
        return redirect('parking_assignment_list')
    if request.method == "POST":
        form = ParkingAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parking_assignment_list')
    else:
        form = ParkingAssignmentForm()
    return render(request, "parking/parking_assign.html", {"form": form})
