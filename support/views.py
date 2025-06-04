from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SupportTicket
from django import forms

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message']

@login_required
def support_list(request):
    user = request.user
    if hasattr(user, "role") and user.role in ["landlord", "agent", "caretaker"]:
        # Show all tickets for properties managed/owned by this user if needed
        # Example: tickets = SupportTicket.objects.filter(property__landlord=user)
        # Adjust as per your model relationships
        tickets = SupportTicket.objects.all().order_by('-created_at')
    else:
        # Tenants and others see only their own tickets
        tickets = SupportTicket.objects.filter(user=user).order_by('-created_at')
    return render(request, "support/support_list.html", {"tickets": tickets})

@login_required
def support_create(request):
    if request.method == "POST":
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('support_list')
    else:
        form = SupportTicketForm()
    return render(request, "support/support_create.html", {"form": form})

@login_required
def support_detail(request, pk):
    user = request.user
    # Only allow access if user owns the ticket or is staff
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if ticket.user != user and not user.is_staff:
        return redirect('support_list')
    return render(request, "support/support_detail.html", {"ticket": ticket})
