from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('add/', views.add_vehicle, name='add_vehicle'),
    path('exit/<int:vehicle_id>/', views.exit_vehicle, name='exit_vehicle'),
    path('profile/', views.profile_settings, name='profile_settings'),
]

