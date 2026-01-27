from auth_app.models import Role

# 检查并创建管理员角色
try:
    admin_role = Role.objects.get(name='Admin')
    print('管理员角色已存在')
except Role.DoesNotExist:
    admin_role = Role.objects.create(name='Admin', description='System administrator role with full permissions')
    print('创建管理员角色成功')

# 检查并创建普通用户角色
try:
    user_role = Role.objects.get(name='User')
    print('普通用户角色已存在')
except Role.DoesNotExist:
    user_role = Role.objects.create(name='User', description='Regular user role with basic permissions')
    print('创建普通用户角色成功')

# 打印所有角色
print('\n现有角色:')
for role in Role.objects.all():
    print(f'{role.id}: {role.name} - {role.description}')
