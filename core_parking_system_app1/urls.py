from django.urls import path
from . import views

urlpatterns = [
    # Authentication & Access Control
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    # Dashboard & Base Routes
    path('', views.dashboard, name='dashboard'),
    
    # Full CRUD Operations
    path('add/', views.add_vehicle, name='add_vehicle'),                          # Create (C)
    path('history/', views.parking_history, name='parking_history'),              # Read (R - All Records)
    path('edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),      # Update (U - Edit details)
    path('exit/<int:vehicle_id>/', views.exit_vehicle, name='exit_vehicle'),      # Update (U - Checkout & Bill)
    path('delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),# Delete (D - Cancel/Remove)

    # Q08 Features
    path('profile/', views.profile_settings, name='profile_settings'),
    path('reports/', views.sqc_reports, name='sqc_reports'),
]
