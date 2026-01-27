from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, LogoutView, UserProfileView, ChangePasswordView

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
]
