from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    """角色模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    description = models.TextField(blank=True, verbose_name='角色描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色管理'

    def __str__(self):
        return self.name


class Permission(models.Model):
    """权限模型"""
    # 权限类型
    PERMISSION_TYPES = (
        ('model', '模型权限'),
        ('object', '对象权限'),
        ('menu', '菜单权限'),
        ('api', 'API权限'),
    )

    codename = models.CharField(max_length=100, unique=True, verbose_name='权限代码')
    name = models.CharField(max_length=100, verbose_name='权限名称')
    type = models.CharField(max_length=20, choices=PERMISSION_TYPES, default='model', verbose_name='权限类型')
    content_type = models.CharField(max_length=100, blank=True, verbose_name='关联类型')
    object_id = models.IntegerField(null=True, blank=True, verbose_name='关联对象ID')
    description = models.TextField(blank=True, verbose_name='权限描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = '权限管理'

    def __str__(self):
        return f'{self.name} ({self.codename})'


class UserRole(models.Model):
    """用户-角色关联模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户角色关联'
        verbose_name_plural = '用户角色管理'
        unique_together = ('user', 'role')

    def __str__(self):
        return f'{self.user.username} - {self.role.name}'


class RolePermission(models.Model):
    """角色-权限关联模型"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '角色权限关联'
        verbose_name_plural = '角色权限管理'
        unique_together = ('role', 'permission')

    def __str__(self):
        return f'{self.role.name} - {self.permission.name}'


# 为 User 模型添加角色相关的方法
def get_user_roles(user):
    """获取用户的所有角色"""
    return Role.objects.filter(userrole__user=user)


def get_user_permissions(user):
    """获取用户的所有权限"""
    roles = get_user_roles(user)
    return Permission.objects.filter(rolepermission__role__in=roles)


def has_permission(user, codename):
    """检查用户是否拥有指定权限"""
    permissions = get_user_permissions(user)
    return permissions.filter(codename=codename).exists()
