from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Role, Permission, UserRole, RolePermission
from .permissions import RBACPermission, IsAdmin, CanManageUsers, CanManageRoles, CanManagePermissions


class RBACModelTestCase(TestCase):
    def setUp(self):
        # 创建测试用户
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        
        # 创建测试角色
        self.admin_role, _ = Role.objects.get_or_create(
            name='Admin',
            defaults={'description': 'Administrator role'}
        )
        self.user_role, _ = Role.objects.get_or_create(
            name='User',
            defaults={'description': 'Regular user role'}
        )
        self.custom_role, _ = Role.objects.get_or_create(
            name='CustomRole',
            defaults={'description': 'Custom role'}
        )
        
        # 创建测试权限
        self.perm1 = Permission.objects.create(
            name='Can manage users',
            codename='can_manage_users',
            description='Permission to manage users'
        )
        self.perm2 = Permission.objects.create(
            name='Can manage roles',
            codename='can_manage_roles',
            description='Permission to manage roles'
        )
        self.perm3 = Permission.objects.create(
            name='Can view dashboard',
            codename='can_view_dashboard',
            description='Permission to view dashboard'
        )
    
    def test_role_creation(self):
        """测试角色创建"""
        role = Role.objects.create(
            name='TestRole',
            description='Test role'
        )
        self.assertEqual(role.name, 'TestRole')
        self.assertEqual(role.description, 'Test role')
    
    def test_permission_creation(self):
        """测试权限创建"""
        perm = Permission.objects.create(
            name='Test Permission',
            codename='test_permission',
            description='Test permission description'
        )
        self.assertEqual(perm.name, 'Test Permission')
        self.assertEqual(perm.codename, 'test_permission')
        self.assertEqual(perm.description, 'Test permission description')
    
    def test_user_role_assignment(self):
        """测试用户角色分配"""
        user_role = UserRole.objects.create(
            user=self.test_user,
            role=self.user_role
        )
        self.assertEqual(user_role.user, self.test_user)
        self.assertEqual(user_role.role, self.user_role)
        
        # 测试用户的角色关联
        roles = self.test_user.roles.all()
        self.assertIn(self.user_role, roles)
    
    def test_role_permission_assignment(self):
        """测试角色权限分配"""
        role_perm = RolePermission.objects.create(
            role=self.admin_role,
            permission=self.perm1
        )
        self.assertEqual(role_perm.role, self.admin_role)
        self.assertEqual(role_perm.permission, self.perm1)
        
        # 测试角色的权限关联
        permissions = self.admin_role.permissions.all()
        self.assertIn(self.perm1, permissions)
    
    def test_user_has_permission(self):
        """测试用户是否拥有特定权限"""
        # 分配角色给用户
        UserRole.objects.create(user=self.test_user, role=self.custom_role)
        
        # 分配权限给角色
        RolePermission.objects.create(role=self.custom_role, permission=self.perm3)
        
        # 测试用户是否拥有权限
        self.assertTrue(self.test_user.has_permission('can_view_dashboard'))
        self.assertFalse(self.test_user.has_permission('can_manage_users'))
    
    def test_user_has_role(self):
        """测试用户是否拥有特定角色"""
        # 分配角色给用户
        UserRole.objects.create(user=self.test_user, role=self.user_role)
        
        # 测试用户是否拥有角色
        self.assertTrue(self.test_user.has_role('User'))
        self.assertFalse(self.test_user.has_role('Admin'))
    
    def test_role_has_permission(self):
        """测试角色是否拥有特定权限"""
        # 分配权限给角色
        RolePermission.objects.create(role=self.custom_role, permission=self.perm2)
        
        # 测试角色是否拥有权限
        self.assertTrue(self.custom_role.has_permission('can_manage_roles'))
        self.assertFalse(self.custom_role.has_permission('can_manage_users'))
    
    def test_get_user_roles(self):
        """测试获取用户角色列表"""
        # 分配多个角色给用户
        UserRole.objects.create(user=self.test_user, role=self.user_role)
        UserRole.objects.create(user=self.test_user, role=self.custom_role)
        
        # 测试获取用户角色
        roles = self.test_user.get_roles()
        role_names = [role.name for role in roles]
        self.assertIn('User', role_names)
        self.assertIn('CustomRole', role_names)
        self.assertEqual(len(roles), 2)
    
    def test_get_user_permissions(self):
        """测试获取用户权限列表"""
        # 分配角色给用户
        UserRole.objects.create(user=self.test_user, role=self.custom_role)
        
        # 分配权限给角色
        RolePermission.objects.create(role=self.custom_role, permission=self.perm2)
        RolePermission.objects.create(role=self.custom_role, permission=self.perm3)
        
        # 测试获取用户权限
        permissions = self.test_user.get_permissions()
        perm_codenames = [perm.codename for perm in permissions]
        self.assertIn('can_manage_roles', perm_codenames)
        self.assertIn('can_view_dashboard', perm_codenames)
        self.assertEqual(len(permissions), 2)


class RBACModelTestCase(TestCase):
    def setUp(self):
        # 创建测试用户
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        
        # 创建测试角色
        self.admin_role, _ = Role.objects.get_or_create(
            name='Admin',
            defaults={'description': 'Administrator role'}
        )
        self.user_role, _ = Role.objects.get_or_create(
            name='User',
            defaults={'description': 'Regular user role'}
        )
        self.custom_role = Role.objects.create(
            name='CustomRole',
            description='Custom role'
        )
        
        # 创建测试权限
        self.perm1 = Permission.objects.create(
            name='Can manage users',
            codename='can_manage_users',
            description='Permission to manage users'
        )
        self.perm2 = Permission.objects.create(
            name='Can manage roles',
            codename='can_manage_roles',
            description='Permission to manage roles'
        )
        self.perm3 = Permission.objects.create(
            name='Can view dashboard',
            codename='can_view_dashboard',
            description='Permission to view dashboard'
        )
    
    def test_role_creation(self):
        """测试角色创建"""
        role = Role.objects.create(
            name='TestRole',
            description='Test role',
            is_built_in=False
        )
        self.assertEqual(role.name, 'TestRole')
        self.assertEqual(role.description, 'Test role')
        self.assertFalse(role.is_built_in)
    
    def test_permission_creation(self):
        """测试权限创建"""
        perm = Permission.objects.create(
            name='Test Permission',
            codename='test_permission',
            description='Test permission description'
        )
        self.assertEqual(perm.name, 'Test Permission')
        self.assertEqual(perm.codename, 'test_permission')
        self.assertEqual(perm.description, 'Test permission description')
    
    def test_user_role_assignment(self):
        """测试用户角色分配"""
        user_role = UserRole.objects.create(
            user=self.test_user,
            role=self.user_role
        )
        self.assertEqual(user_role.user, self.test_user)
        self.assertEqual(user_role.role, self.user_role)
        
        # 测试用户的角色关联
        roles = self.test_user.roles.all()
        self.assertIn(self.user_role, roles)
    
    def test_role_permission_assignment(self):
        """测试角色权限分配"""
        role_perm = RolePermission.objects.create(
            role=self.admin_role,
            permission=self.perm1
        )
        self.assertEqual(role_perm.role, self.admin_role)
        self.assertEqual(role_perm.permission, self.perm1)
        
        # 测试角色的权限关联
        permissions = self.admin_role.permissions.all()
        self.assertIn(self.perm1, permissions)
    
    def test_user_has_permission(self):
        """测试用户是否拥有特定权限"""
        # 分配角色给用户
        UserRole.objects.create(user=self.test_user, role=self.custom_role)
        
        # 分配权限给角色
        RolePermission.objects.create(role=self.custom_role, permission=self.perm3)
        
        # 测试用户是否拥有权限
        self.assertTrue(self.test_user.has_permission('can_view_dashboard'))
        self.assertFalse(self.test_user.has_permission('can_manage_users'))
    
    def test_user_has_role(self):
        """测试用户是否拥有特定角色"""
        # 分配角色给用户
        UserRole.objects.create(user=self.test_user, role=self.user_role)
        
        # 测试用户是否拥有角色
        self.assertTrue(self.test_user.has_role('User'))
        self.assertFalse(self.test_user.has_role('Admin'))
    
    def test_role_has_permission(self):
        """测试角色是否拥有特定权限"""
        # 分配权限给角色
        RolePermission.objects.create(role=self.custom_role, permission=self.perm2)
        
        # 测试角色是否拥有权限
        self.assertTrue(self.custom_role.has_permission('can_manage_roles'))
        self.assertFalse(self.custom_role.has_permission('can_manage_users'))
    
    def test_get_user_roles(self):
        """测试获取用户角色列表"""
        # 分配多个角色给用户
        UserRole.objects.create(user=self.test_user, role=self.user_role)
        UserRole.objects.create(user=self.test_user, role=self.custom_role)
        
        # 测试获取用户角色
        roles = self.test_user.get_roles()
        role_names = [role.name for role in roles]
        self.assertIn('User', role_names)
        self.assertIn('CustomRole', role_names)
        self.assertEqual(len(roles), 2)
    
    def test_get_user_permissions(self):
        """测试获取用户权限列表"""
        # 分配角色给用户
        UserRole.objects.create(user=self.test_user, role=self.custom_role)
        
        # 分配权限给角色
        RolePermission.objects.create(role=self.custom_role, permission=self.perm2)
        RolePermission.objects.create(role=self.custom_role, permission=self.perm3)
        
        # 测试获取用户权限
        permissions = self.test_user.get_permissions()
        perm_codenames = [perm.codename for perm in permissions]
        self.assertIn('can_manage_roles', perm_codenames)
        self.assertIn('can_view_dashboard', perm_codenames)
        self.assertEqual(len(permissions), 2)


class RBACViewTestCase(TestCase):
    def setUp(self):
        # 创建测试客户端
        self.client = APIClient()
        
        # 创建测试用户
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        
        # 创建测试角色
        self.admin_role, _ = Role.objects.get_or_create(
            name='Admin',
            defaults={'description': 'Administrator role'}
        )
        self.user_role, _ = Role.objects.get_or_create(
            name='User',
            defaults={'description': 'Regular user role'}
        )
        
        # 创建测试权限
        self.perm1 = Permission.objects.create(
            name='Can manage users',
            codename='can_manage_users',
            description='Permission to manage users'
        )
        self.perm2 = Permission.objects.create(
            name='Can manage roles',
            codename='can_manage_roles',
            description='Permission to manage roles'
        )
        
        # 分配角色给用户
        UserRole.objects.create(user=self.admin_user, role=self.admin_role)
        UserRole.objects.create(user=self.test_user, role=self.user_role)
        
        # 分配权限给角色
        RolePermission.objects.create(role=self.admin_role, permission=self.perm1)
        RolePermission.objects.create(role=self.admin_role, permission=self.perm2)
        
        # 获取JWT token
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.user_token = str(RefreshToken.for_user(self.test_user).access_token)
    
    def test_role_list_view(self):
        """测试角色列表API"""
        # 管理员访问
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        url = reverse('role-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 普通用户访问（应该失败）
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_role_create_view(self):
        """测试角色创建API"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        url = reverse('role-list')
        data = {
            'name': 'TestRole',
            'description': 'Test role'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'TestRole')
    
    def test_role_update_view(self):
        """测试角色更新API"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        url = reverse('role-detail', args=[self.user_role.id])
        data = {
            'description': 'Updated user role description'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Updated user role description')
    
    def test_role_delete_view(self):
        """测试角色删除API"""
        # 创建可删除的角色
        test_role = Role.objects.create(
            name='TestRole',
            description='Test role'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        url = reverse('role-detail', args=[test_role.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_permission_list_view(self):
        """测试权限列表API"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        url = reverse('permission-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_role_assignment(self):
        """测试用户角色分配API"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        url = reverse('userrole-list')
        data = {
            'user': self.test_user.id,
            'role': self.admin_role.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_role_permission_assignment(self):
        """测试角色权限分配API"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        url = reverse('rolepermission-list')
        data = {
            'role': self.user_role.id,
            'permission': self.perm2.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RBACPermissionTestCase(TestCase):
    def setUp(self):
        # 创建测试用户
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        
        # 创建测试角色
        self.admin_role, _ = Role.objects.get_or_create(
            name='Admin',
            defaults={'description': 'Administrator role'}
        )
        self.user_role, _ = Role.objects.get_or_create(
            name='User',
            defaults={'description': 'Regular user role'}
        )
        
        # 创建测试权限
        self.manage_users_perm = Permission.objects.create(
            name='Can manage users',
            codename='can_manage_users',
            description='Permission to manage users'
        )
        self.manage_roles_perm = Permission.objects.create(
            name='Can manage roles',
            codename='can_manage_roles',
            description='Permission to manage roles'
        )
        self.manage_permissions_perm = Permission.objects.create(
            name='Can manage permissions',
            codename='can_manage_permissions',
            description='Permission to manage permissions'
        )
        
        # 分配角色给用户
        UserRole.objects.create(user=self.admin_user, role=self.admin_role)
        UserRole.objects.create(user=self.test_user, role=self.user_role)
        
        # 分配权限给角色
        RolePermission.objects.create(role=self.admin_role, permission=self.manage_users_perm)
        RolePermission.objects.create(role=self.admin_role, permission=self.manage_roles_perm)
        RolePermission.objects.create(role=self.admin_role, permission=self.manage_permissions_perm)
    
    def test_is_admin_permission(self):
        """测试IsAdmin权限类"""
        permission = IsAdmin()
        
        # 模拟请求对象
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        # 管理员用户应该有权限
        admin_request = MockRequest(self.admin_user)
        self.assertTrue(permission.has_permission(admin_request, None))
        
        # 普通用户不应该有权限
        user_request = MockRequest(self.test_user)
        self.assertFalse(permission.has_permission(user_request, None))
    
    def test_can_manage_users_permission(self):
        """测试CanManageUsers权限类"""
        permission = CanManageUsers()
        
        # 模拟请求对象
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        # 管理员用户应该有权限
        admin_request = MockRequest(self.admin_user)
        self.assertTrue(permission.has_permission(admin_request, None))
        
        # 普通用户不应该有权限
        user_request = MockRequest(self.test_user)
        self.assertFalse(permission.has_permission(user_request, None))
    
    def test_can_manage_roles_permission(self):
        """测试CanManageRoles权限类"""
        permission = CanManageRoles()
        
        # 模拟请求对象
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        # 管理员用户应该有权限
        admin_request = MockRequest(self.admin_user)
        self.assertTrue(permission.has_permission(admin_request, None))
        
        # 普通用户不应该有权限
        user_request = MockRequest(self.test_user)
        self.assertFalse(permission.has_permission(user_request, None))
    
    def test_can_manage_permissions_permission(self):
        """测试CanManagePermissions权限类"""
        permission = CanManagePermissions()
        
        # 模拟请求对象
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        # 管理员用户应该有权限
        admin_request = MockRequest(self.admin_user)
        self.assertTrue(permission.has_permission(admin_request, None))
        
        # 普通用户不应该有权限
        user_request = MockRequest(self.test_user)
        self.assertFalse(permission.has_permission(user_request, None))
    
    def test_rbac_permission(self):
        """测试RBACPermission权限类"""
        # 测试需要can_manage_users权限的情况
        permission = RBACPermission('can_manage_users')
        
        # 模拟请求对象
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        # 管理员用户应该有权限
        admin_request = MockRequest(self.admin_user)
        self.assertTrue(permission.has_permission(admin_request, None))
        
        # 普通用户不应该有权限
        user_request = MockRequest(self.test_user)
        self.assertFalse(permission.has_permission(user_request, None))


if __name__ == '__main__':
    import unittest
    unittest.main()
