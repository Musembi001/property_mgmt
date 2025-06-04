from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView
from django.db import models
from django.urls import reverse
from django.contrib.auth.decorators import login_required

User = get_user_model()

class TenantListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/tenant_list.html'
    context_object_name = 'tenants'
    paginate_by = 10

    def get_queryset(self):
        qs = User.objects.filter(role='tenant')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                models.Q(first_name__icontains=q) |
                models.Q(last_name__icontains=q) |
                models.Q(email__icontains=q)
            )
        return qs.order_by('-date_joined')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)  # Session expires on browser close
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

class TenantDetailView(DetailView):
    model = User
    template_name = 'accounts/tenant_detail.html'
    context_object_name = 'tenant'

class TenantUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number']  # adjust as needed
    template_name = 'accounts/tenant_form.html'

    def get_success_url(self):
        return reverse('tenant_detail', args=[self.object.pk])

def tenant_deactivate(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = False
    user.save()
    return redirect('tenant_list')

def tenant_activate(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = True
    user.save()
    return redirect('tenant_list')

@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})
