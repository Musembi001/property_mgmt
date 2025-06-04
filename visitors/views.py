from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Visitor
from .forms import VisitorForm
from django.utils import timezone

@login_required
def visitor_list(request):
    user = request.user
    if user.is_superuser:
        visitors = Visitor.objects.all().order_by('-check_in')
    elif hasattr(user, "role"):
        if user.role == "landlord":
            visitors = Visitor.objects.filter(
                property__landlord=user
            ).order_by('-check_in')
        else:
            visitors = Visitor.objects.filter(whom_to_visit=user).order_by('-check_in')
    else:
        visitors = Visitor.objects.none()
    return render(request, "visitors/visitor_list.html", {"visitors": visitors})

@login_required
def visitor_register(request):
    if request.method == "POST":
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.registered_by = request.user
            
            visitor.save()
            return redirect('visitor_list')
    else:
        form = VisitorForm()
    return render(request, "visitors/visitor_register.html", {"form": form})

@login_required
def visitor_checkout(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    if not visitor.check_out:
        visitor.check_out = timezone.now()
        visitor.save()
    return redirect('visitor_list')
