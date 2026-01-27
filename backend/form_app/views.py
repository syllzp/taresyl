from rest_framework import viewsets, permissions
from .models import FormConfig
from .serializers import FormConfigSerializer
from system_app.models import SystemLog


class FormConfigViewSet(viewsets.ModelViewSet):
    queryset = FormConfig.objects.all()
    serializer_class = FormConfigSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """创建表单配置并记录日志"""
        response = super().create(request, *args, **kwargs)
        
        # 记录创建日志
        SystemLog.objects.create(
            level='INFO',
            message=f'创建了新表单: {response.data.get("name")}',
            resource_type='FORM',
            resource_id=str(response.data.get("id")),
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response
    
    def update(self, request, *args, **kwargs):
        """更新表单配置并记录日志"""
        form_instance = self.get_object()
        old_name = form_instance.name
        
        response = super().update(request, *args, **kwargs)
        
        # 记录更新日志
        SystemLog.objects.create(
            level='INFO',
            message=f'更新了表单: {old_name} -> {response.data.get("name")}',
            resource_type='FORM',
            resource_id=str(kwargs.get("pk")),
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response
    
    def destroy(self, request, *args, **kwargs):
        """删除表单配置并记录日志"""
        form_instance = self.get_object()
        form_name = form_instance.name
        form_id = str(form_instance.id)
        
        response = super().destroy(request, *args, **kwargs)
        
        # 记录删除日志
        SystemLog.objects.create(
            level='INFO',
            message=f'删除了表单: {form_name}',
            resource_type='FORM',
            resource_id=form_id,
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response
