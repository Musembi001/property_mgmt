from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Lease
from .forms import LeaseForm

class LeaseListView(LoginRequiredMixin, ListView):
    model = Lease
    template_name = 'leases/lease_list.html'
    context_object_name = 'leases'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "role"):
            if user.role == "tenant":
                return Lease.objects.filter(tenant=user)
            elif user.role == "landlord":
                # Assumes Lease has unit__property__landlord or similar relation
                return Lease.objects.filter(unit__property__landlord=user)
            elif user.role == "agent":
                # Assumes Lease has unit__property__agent or similar relation
                return Lease.objects.filter(unit__property__agent=user)
            elif user.role == "caretaker":
                # Assumes Lease has unit__property__caretaker or similar relation
                return Lease.objects.filter(unit__property__caretaker=user)
        # Default: show nothing
        return Lease.objects.none()

class LeaseCreateView(CreateView):
    model = Lease
    form_class = LeaseForm
    template_name = 'leases/lease_form.html'
    success_url = reverse_lazy('lease_list')
