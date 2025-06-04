from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import City, Building, Unit
from .forms import BuildingForm

# Optional: Only allow landlords to access certain views
class LandlordRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, "role") and self.request.user.role == "landlord"

# City Views
class CityListView(LoginRequiredMixin, ListView):
    model = City
    template_name = 'properties/city_list.html'

class CityCreateView(LoginRequiredMixin, CreateView):
    model = City
    fields = ['name']
    template_name = 'properties/city_form.html'
    success_url = reverse_lazy('city_list')

class CityUpdateView(LoginRequiredMixin, UpdateView):
    model = City
    fields = ['name']
    template_name = 'properties/city_form.html'
    success_url = reverse_lazy('city_list')

class CityDeleteView(LoginRequiredMixin, DeleteView):
    model = City
    template_name = 'properties/city_confirm_delete.html'
    success_url = reverse_lazy('city_list')

# Building Views
class BuildingListView(LoginRequiredMixin, ListView):
    model = Building
    template_name = 'properties/building_list.html'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "role"):
            if user.role == "landlord":
                return Building.objects.filter(landlord=user)
            elif user.role == "agent":
                return Building.objects.filter(agent=user)
            elif user.role == "caretaker":
                return Building.objects.filter(caretaker=user)
            # Tenants should not see all buildings; return none or filter as needed
            elif user.role == "tenant":
                return Building.objects.filter(unit__lease__tenant=user).distinct()
        return Building.objects.none()

class BuildingCreateView(LoginRequiredMixin, LandlordRequiredMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('building_list')

    def form_valid(self, form):
        form.instance.landlord = self.request.user
        return super().form_valid(form)

class BuildingUpdateView(LoginRequiredMixin, LandlordRequiredMixin, UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('building_list')

class BuildingDeleteView(LoginRequiredMixin, LandlordRequiredMixin, DeleteView):
    model = Building
    template_name = 'properties/building_confirm_delete.html'
    success_url = reverse_lazy('building_list')

# Unit Views
class UnitListView(LoginRequiredMixin, ListView):
    model = Unit
    template_name = 'properties/unit_list.html'

    def get_queryset(self):
        user = self.request.user
        building_id = self.kwargs['building_id']
        qs = Unit.objects.filter(building_id=building_id)
        if hasattr(user, "role"):
            if user.role == "landlord":
                return qs.filter(building__landlord=user)
            elif user.role == "agent":
                return qs.filter(building__agent=user)
            elif user.role == "caretaker":
                return qs.filter(building__caretaker=user)
            elif user.role == "tenant":
                return qs.filter(lease__tenant=user).distinct()
        return Unit.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building_id'] = self.kwargs['building_id']
        return context

class UnitCreateView(LoginRequiredMixin, LandlordRequiredMixin, CreateView):
    model = Unit
    fields = ['unit_number', 'floor']
    template_name = 'properties/unit_form.html'

    def form_valid(self, form):
        form.instance.building_id = self.kwargs['building_id']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building_id'] = self.kwargs['building_id']
        return context

    def get_success_url(self):
        return reverse('unit_list', args=[self.kwargs['building_id']])

class UnitUpdateView(LoginRequiredMixin, LandlordRequiredMixin, UpdateView):
    model = Unit
    fields = ['unit_number', 'floor']
    template_name = 'properties/unit_form.html'

    def get_success_url(self):
        return reverse('unit_list', args=[self.object.building_id])

class UnitDeleteView(LoginRequiredMixin, LandlordRequiredMixin, DeleteView):
    model = Unit
    template_name = 'properties/unit_confirm_delete.html'

    def get_success_url(self):
        return reverse('unit_list', args=[self.object.building_id])
