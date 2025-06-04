from django.urls import path
from .views import LeaseListView, LeaseCreateView

urlpatterns = [
    path('', LeaseListView.as_view(), name='lease_list'),
    path('add/', LeaseCreateView.as_view(), name='lease_add'),
]