from django.urls import path
from . import views

urlpatterns = [
    path('', views.support_list, name='support_list'),
    path('add/', views.support_create, name='support_create'),  # change 'new/' to 'add/'
    path('<int:pk>/', views.support_detail, name='support_detail'),
]