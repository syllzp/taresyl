from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    RoleSerializer, PermissionSerializer, UserRoleSerializer, RolePermissionSerializer,
    UserWithRolesSerializer
)
from .models import Role, Permission, UserRole, RolePermission, get_user_roles, get_user_permissions, has_permission
from .permissions import IsAdmin, CanManageUsers, CanManageRoles, CanManagePermissions
from system_app.models import SystemLog


class RegisterView(generics.CreateAPIView):
    """用户注册视图"""
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    """用户登录视图"""
    serializer_class = LoginSerializer


class LogoutView(generics.GenericAPIView):
    """用户退出登录视图"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """获取和更新用户信息视图"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """修改密码视图"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response(
                {"error": "请提供旧密码和新密码"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {"error": "旧密码错误"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "密码修改成功"},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 使用 RBAC 权限检查
    permission_classes = [CanManageUsers]
    
    def create(self, request, *args, **kwargs):
        """创建用户并记录日志"""
        response = super().create(request, *args, **kwargs)
        
        # 记录创建日志
        SystemLog.objects.create(
            level='INFO',
            message=f'创建了新用户: {response.data.get("username")}',
            resource_type='USER',
            resource_id=str(response.data.get("id")),
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response
    
    def update(self, request, *args, **kwargs):
        """更新用户并记录日志"""
        user_instance = self.get_object()
        old_username = user_instance.username
        
        response = super().update(request, *args, **kwargs)
        
        # 记录更新日志
        SystemLog.objects.create(
            level='INFO',
            message=f'更新了用户: {old_username} -> {response.data.get("username")}',
            resource_type='USER',
            resource_id=str(kwargs.get("pk")),
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response
    
    def destroy(self, request, *args, **kwargs):
        """删除用户并记录日志"""
        user_instance = self.get_object()
        username = user_instance.username
        user_id = str(user_instance.id)
        
        response = super().destroy(request, *args, **kwargs)
        
        # 记录删除日志
        SystemLog.objects.create(
            level='INFO',
            message=f'删除了用户: {username}',
            resource_type='USER',
            resource_id=user_id,
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response


class RoleViewSet(viewsets.ModelViewSet):
    """角色管理视图集"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [CanManageRoles]

    def create(self, request, *args, **kwargs):
        """创建角色并记录日志"""
        response = super().create(request, *args, **kwargs)
        
        # 记录创建日志
        SystemLog.objects.create(
            level='INFO',
            message=f'创建了新角色: {response.data.get("name")}',
            resource_type='ROLE',
            resource_id=str(response.data.get("id")),
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response

    def update(self, request, *args, **kwargs):
        """更新角色并记录日志"""
        role_instance = self.get_object()
        old_name = role_instance.name
        
        response = super().update(request, *args, **kwargs)
        
        # 记录更新日志
        SystemLog.objects.create(
            level='INFO',
            message=f'更新了角色: {old_name} -> {response.data.get("name")}',
            resource_type='ROLE',
            resource_id=str(kwargs.get("pk")),
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response

    def destroy(self, request, *args, **kwargs):
        """删除角色并记录日志"""
        role_instance = self.get_object()
        role_name = role_instance.name
        role_id = str(role_instance.id)
        
        # 阻止删除内置角色
        if role_name in ['Admin', 'User']:
            from rest_framework.response import Response
            from rest_framework import status
            return Response(
                {'error': f'内置角色 {role_name} 不能删除'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response = super().destroy(request, *args, **kwargs)
        
        # 记录删除日志
        SystemLog.objects.create(
            level='INFO',
            message=f'删除了角色: {role_name}',
            resource_type='ROLE',
            resource_id=role_id,
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response


class PermissionViewSet(viewsets.ModelViewSet):
    """权限管理视图集"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [CanManagePermissions]

    def create(self, request, *args, **kwargs):
        """创建权限并记录日志"""
        response = super().create(request, *args, **kwargs)
        
        # 记录创建日志
        SystemLog.objects.create(
            level='INFO',
            message=f'创建了新权限: {response.data.get("name")}',
            resource_type='PERMISSION',
            resource_id=str(response.data.get("id")),
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response

    def update(self, request, *args, **kwargs):
        """更新权限并记录日志"""
        permission_instance = self.get_object()
        old_name = permission_instance.name
        
        response = super().update(request, *args, **kwargs)
        
        # 记录更新日志
        SystemLog.objects.create(
            level='INFO',
            message=f'更新了权限: {old_name} -> {response.data.get("name")}',
            resource_type='PERMISSION',
            resource_id=str(kwargs.get("pk")),
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response

    def destroy(self, request, *args, **kwargs):
        """删除权限并记录日志"""
        permission_instance = self.get_object()
        permission_name = permission_instance.name
        permission_id = str(permission_instance.id)
        
        response = super().destroy(request, *args, **kwargs)
        
        # 记录删除日志
        SystemLog.objects.create(
            level='INFO',
            message=f'删除了权限: {permission_name}',
            resource_type='PERMISSION',
            resource_id=permission_id,
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response


class UserRoleViewSet(viewsets.ModelViewSet):
    """用户角色关联管理视图集"""
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [CanManageRoles]

    def create(self, request, *args, **kwargs):
        """创建用户角色关联并记录日志"""
        response = super().create(request, *args, **kwargs)
        
        # 记录创建日志
        SystemLog.objects.create(
            level='INFO',
            message=f'为用户分配了角色',
            resource_type='USER_ROLE',
            resource_id=str(response.data.get("id")),
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response

    def destroy(self, request, *args, **kwargs):
        """删除用户角色关联并记录日志"""
        user_role_instance = self.get_object()
        user_role_id = str(user_role_instance.id)
        
        response = super().destroy(request, *args, **kwargs)
        
        # 记录删除日志
        SystemLog.objects.create(
            level='INFO',
            message=f'移除了用户的角色关联',
            resource_type='USER_ROLE',
            resource_id=user_role_id,
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response


class RolePermissionViewSet(viewsets.ModelViewSet):
    """角色权限关联管理视图集"""
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [CanManagePermissions]

    def create(self, request, *args, **kwargs):
        """创建角色权限关联并记录日志"""
        response = super().create(request, *args, **kwargs)
        
        # 记录创建日志
        SystemLog.objects.create(
            level='INFO',
            message=f'为角色分配了权限',
            resource_type='ROLE_PERMISSION',
            resource_id=str(response.data.get("id")),
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response

    def destroy(self, request, *args, **kwargs):
        """删除角色权限关联并记录日志"""
        role_permission_instance = self.get_object()
        role_permission_id = str(role_permission_instance.id)
        
        response = super().destroy(request, *args, **kwargs)
        
        # 记录删除日志
        SystemLog.objects.create(
            level='INFO',
            message=f'移除了角色的权限关联',
            resource_type='ROLE_PERMISSION',
            resource_id=role_permission_id,
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response


class UserWithRolesView(generics.RetrieveAPIView):
    """获取带有角色信息的用户详情视图"""
    queryset = User.objects.all()
    serializer_class = UserWithRolesSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserPermissionsView(generics.RetrieveAPIView):
    """获取用户权限视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        permissions = get_user_permissions(user)
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)
