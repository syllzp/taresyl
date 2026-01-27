from rest_framework import serializers
from .models import SystemLog
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class SystemLogSerializer(serializers.ModelSerializer):
    """系统日志序列化器"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = SystemLog
        fields = [
            'id',
            'level',
            'message',
            'resource_type',
            'resource_id',
            'user',
            'ip_address',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
