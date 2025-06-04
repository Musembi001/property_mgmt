from django.urls import path
from . import views

urlpatterns = [
    # City
    path('cities/', views.CityListView.as_view(), name='city_list'),
    path('cities/add/', views.CityCreateView.as_view(), name='city_add'),
    path('cities/<int:pk>/edit/', views.CityUpdateView.as_view(), name='city_edit'),
    path('cities/<int:pk>/delete/', views.CityDeleteView.as_view(), name='city_delete'),

    # Building
    path('', views.BuildingListView.as_view(), name='building_list'),
    path('add/', views.BuildingCreateView.as_view(), name='building_add'),
    path('<int:pk>/edit/', views.BuildingUpdateView.as_view(), name='building_edit'),
    path('<int:pk>/delete/', views.BuildingDeleteView.as_view(), name='building_delete'),

    # Unit
    path('<int:building_id>/units/', views.UnitListView.as_view(), name='unit_list'),
    path('<int:building_id>/units/add/', views.UnitCreateView.as_view(), name='unit_add'),
    path('units/<int:pk>/edit/', views.UnitUpdateView.as_view(), name='unit_edit'),
    path('units/<int:pk>/delete/', views.UnitDeleteView.as_view(), name='unit_delete'),
]