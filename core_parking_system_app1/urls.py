from django.urls import path
from . import views

urlpatterns = [
    # 1. Main Landing & Stakeholder Auth Launchpad
    path('', views.landing_auth, name='landing_auth'),
    path('persona/<str:persona>/', views.quick_persona_login, name='quick_persona_login'),
    path('logout/', views.logout_view, name='logout'),

    # 2. Stakeholder Dedicated Workstations
    path('operator/', views.operator_terminal, name='operator_terminal'),
    path('dashboard/', views.operator_terminal, name='dashboard'),  # backward compatibility alias
    path('customer/', views.customer_portal, name='customer_portal'),
    path('security/', views.security_console, name='security_console'),
    path('manager/', views.manager_console, name='manager_console'),
    path('admin-console/', views.admin_console, name='admin_console'),

    # 3. Vehicle Operations & Billing
    path('add/', views.add_vehicle, name='add_vehicle'),
    path('edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('exit/<int:vehicle_id>/', views.exit_vehicle, name='exit_vehicle'),
    path('delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('receipt/<int:vehicle_id>/', views.receipt_view, name='receipt_view'),

    # 4. Security Sub-Actions
    path('security/resolve/<int:incident_id>/', views.security_resolve_incident, name='security_resolve_incident'),
    path('security/barrier/<str:barrier_type>/', views.security_toggle_barrier, name='security_toggle_barrier'),

    # 5. History, Settings & Tools
    path('history/', views.parking_history, name='parking_history'),
    path('profile/', views.profile_settings, name='profile_settings'),

    # 6. APIs
    path('api/validate-plate/', views.api_validate_plate, name='api_validate_plate'),
    path('api/reset-seed/', views.api_reset_seed, name='api_reset_seed'),
]
