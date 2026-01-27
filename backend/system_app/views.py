from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SystemLog
from .serializers import SystemLogSerializer

class SystemLogViewSet(viewsets.ModelViewSet):
    """系统日志视图集"""
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    # 暂时允许所有请求，实际生产环境应该设置权限
    # permission_classes = [IsAuthenticated]
    
    # 自定义列表查询，支持过滤和排序
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 过滤参数
        level = self.request.query_params.get('level')
        resource_type = self.request.query_params.get('resource_type')
        user_id = self.request.query_params.get('user_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if level:
            queryset = queryset.filter(level=level)
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset

