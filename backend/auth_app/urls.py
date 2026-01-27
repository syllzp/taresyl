from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView, LogoutView, UserProfileView, ChangePasswordView, UserViewSet,
    RoleViewSet, PermissionViewSet, UserRoleViewSet, RolePermissionViewSet,
    UserWithRolesView, UserPermissionsView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'user-roles', UserRoleViewSet, basename='user-role')
router.register(r'role-permissions', RolePermissionViewSet, basename='role-permission')

urlpatterns = [
    # 用户注册
    path('register/', RegisterView.as_view(), name='register'),
    # 用户登录
    path('login/', LoginView.as_view(), name='login'),
    # 刷新令牌
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 用户退出登录
    path('logout/', LogoutView.as_view(), name='logout'),
    # 获取和更新用户信息
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    # 修改密码
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    # 获取用户权限
    path('user-permissions/', UserPermissionsView.as_view(), name='user_permissions'),
    # 获取用户带有角色信息
    path('users-with-roles/<int:pk>/', UserWithRolesView.as_view(), name='user_with_roles'),
    # 管理路由
    path('', include(router.urls)),
]
