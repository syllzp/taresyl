from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'
    
    def ready(self):
        """应用启动时自动创建内置角色"""
        from .models import Role
        from django.contrib.auth.models import User
        
        def create_builtin_roles(sender, **kwargs):
            """创建内置角色"""
            # 创建管理员角色
            admin_role, created = Role.objects.get_or_create(
                name='Admin',
                defaults={'description': 'System administrator role with full permissions'}
            )
            if created:
                print('Created builtin role: Admin')
            
            # 创建普通用户角色
            user_role, created = Role.objects.get_or_create(
                name='User',
                defaults={'description': 'Regular user role with basic permissions'}
            )
            if created:
                print('Created builtin role: User')
        
        # 注册信号处理器
        post_migrate.connect(create_builtin_roles, sender=self)
