from django.urls import path
from . import views

urlpatterns = [
    path('', views.parking_slot_list, name='parking_home'),  # Add this line
    path('slots/', views.parking_slot_list, name='parking_slot_list'),
    path('assignments/', views.parking_assignment_list, name='parking_assignment_list'),
    path('assign/', views.parking_assign, name='parking_assign'),
]