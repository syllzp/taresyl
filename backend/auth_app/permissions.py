from rest_framework.permissions import BasePermission
from .models import has_permission


class RBACPermission(BasePermission):
    """基于 RBAC 模型的权限检查类"""
    
    def __init__(self, required_permissions=None):
        """初始化权限类
        
        Args:
            required_permissions (list): 需要的权限代码列表
        """
        self.required_permissions = required_permissions or []
    
    def has_permission(self, request, view):
        """检查用户是否拥有所需权限
        
        Args:
            request: 请求对象
            view: 视图对象
            
        Returns:
            bool: 用户是否拥有所需权限
        """
        # 首先检查用户是否已认证
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 如果没有指定所需权限，则默认允许访问
        if not self.required_permissions:
            return True
        
        # 检查用户是否拥有所有所需权限
        for permission_codename in self.required_permissions:
            if not has_permission(request.user, permission_codename):
                return False
        
        return True


# 常用权限检查类
class IsAdmin(RBACPermission):
    """管理员权限检查"""
    def __init__(self):
        super().__init__(['admin_access'])


class CanManageUsers(RBACPermission):
    """用户管理权限检查"""
    def __init__(self):
        super().__init__(['user_manage'])


class CanManageRoles(RBACPermission):
    """角色管理权限检查"""
    def __init__(self):
        super().__init__(['role_manage'])


class CanManagePermissions(RBACPermission):
    """权限管理权限检查"""
    def __init__(self):
        super().__init__(['permission_manage'])


class CanManageForms(RBACPermission):
    """表单管理权限检查"""
    def __init__(self):
        super().__init__(['form_manage'])


class CanViewReports(RBACPermission):
    """报表查看权限检查"""
    def __init__(self):
        super().__init__(['report_view'])
