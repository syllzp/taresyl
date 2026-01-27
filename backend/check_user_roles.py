from auth_app.models import Role, Permission, UserRole
from django.contrib.auth.models import User

print('=== Checking User Roles ===')

# Get all users
users = User.objects.all()
print(f'Total users: {users.count()}')

for user in users:
    print(f'\nUser: {user.username}')
    roles = user.userrole_set.all()
    if roles:
        print('Roles:')
        for role in roles:
            print(f'  - {role.role.name}')
    else:
        print('Roles: None')

print('\n=== Check Complete ===')
