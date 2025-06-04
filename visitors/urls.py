from django.urls import path
from . import views

urlpatterns = [
    path('', views.visitor_list, name='visitor_list'),
    path('register/', views.visitor_register, name='visitor_register'),
    path('checkout/<int:pk>/', views.visitor_checkout, name='visitor_checkout'),
]