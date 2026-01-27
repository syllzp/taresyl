from django.contrib.auth.models import User
from auth_app.models import Role, Permission, UserRole, RolePermission

# Get or create admin user
try:
    admin_user = User.objects.get(username='admin')
    print('Found admin user')
except User.DoesNotExist:
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print('Created admin user successfully')

# Create admin role
try:
    admin_role = Role.objects.get(name='Admin')
    print('Found admin role')
except Role.DoesNotExist:
    admin_role = Role.objects.create(
        name='Admin',
        description='System administrator role'
    )
    print('Created admin role successfully')

# Create basic permissions
permissions = [
    'admin_access',
    'user_manage',
    'role_manage',
    'permission_manage',
    'form_manage',
    'report_view'
]

for codename in permissions:
    perm, created = Permission.objects.get_or_create(
        codename=codename,
        name=codename.replace('_', ' ').title(),
        type='api'
    )
    if created:
        print(f'Created permission: {codename}')
    else:
        print(f'Permission already exists: {codename}')
    
    # Assign permission to admin role
    rp, created = RolePermission.objects.get_or_create(
        role=admin_role,
        permission=perm
    )
    if created:
        print(f'Assigned permission to admin role: {codename}')

# Assign admin role to admin user
ur, created = UserRole.objects.get_or_create(
    user=admin_user,
    role=admin_role
)
if created:
    print('Assigned admin role to admin user successfully')
else:
    print('Admin user already has admin role')

# Show results
print('\n=== Operation completed ===')
print(f'Admin role: {admin_role}')
print(f'Number of permissions created: {Permission.objects.count()}')
print(f'Number of roles for admin user: {admin_user.userrole_set.count()}')
print(f'Number of permissions for admin role: {admin_role.rolepermission_set.count()}')
