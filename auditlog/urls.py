from django.urls import path
from . import views

urlpatterns = [
    path('', views.auditlog_list, name='auditlog_list'),
]