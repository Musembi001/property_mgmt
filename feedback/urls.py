from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('add/', views.feedback_submit, name='feedback_submit'),  # change 'submit/' to 'add/'
]