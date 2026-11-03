def auth_role_context(request):
    """
    Supplies the active stakeholder role and permissions to all templates
    for dynamic navigation rendering and access control feedback.
    """
    user = request.user
    if not user.is_authenticated:
        role = 'anonymous'
        role_name = 'Visitor'
    elif user.is_superuser or user.username in ['admin', 'harshit008']:
        role = 'admin'
        role_name = 'System Administrator / Owner'
    elif user.username == 'manager' or (user.is_staff and not user.is_superuser):
        role = 'manager'
        role_name = 'Operations Manager'
    elif user.username == 'guard':
        role = 'guard'
        role_name = 'Security Guard'
    elif user.username == 'customer':
        role = 'customer'
        role_name = 'Driver / Customer'
    else:
        role = 'operator'
        role_name = 'Gate Operator / Cashier'

    return {
        'current_role': role,
        'current_role_name': role_name,
        'is_admin': (role == 'admin'),
        'is_manager': (role == 'manager'),
        'is_operator': (role == 'operator'),
        'is_guard': (role == 'guard'),
        'is_customer': (role == 'customer'),
    }
