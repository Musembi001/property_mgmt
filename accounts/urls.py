from django.urls import path
from . import views
from .views import TenantListView, TenantDetailView, TenantUpdateView, tenant_deactivate, tenant_activate
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', TenantListView.as_view(), name='tenant_list'),
    path('users/<int:pk>/', TenantDetailView.as_view(), name='tenant_detail'),
    path('users/<int:pk>/edit/', TenantUpdateView.as_view(), name='tenant_edit'),
    path('users/<int:pk>/deactivate/', tenant_deactivate, name='tenant_deactivate'),
    path('users/<int:pk>/activate/', tenant_activate, name='tenant_activate'),
    path('profile/', views.profile_view, name='profile'),
]

urlpatterns += [
    path('settings/password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/profile/'
    ), name='password_change'),
]