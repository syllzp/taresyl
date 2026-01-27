from rest_framework import serializers
from .models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    """文件上传序列化器"""
    file_url = serializers.CharField(source='file_url', read_only=True)
    
    class Meta:
        model = FileUpload
        fields = ['id', 'file', 'filename', 'file_size', 'content_type', 'uploaded_at', 'is_public', 'file_url']
        read_only_fields = ['id', 'file_size', 'content_type', 'uploaded_at', 'file_url']


class FileUploadListSerializer(serializers.ModelSerializer):
    """文件上传列表序列化器"""
    file_url = serializers.CharField(source='file_url', read_only=True)
    
    class Meta:
        model = FileUpload
        fields = ['id', 'filename', 'file_size', 'content_type', 'uploaded_at', 'is_public', 'file_url']
        read_only_fields = ['id', 'file_size', 'content_type', 'uploaded_at', 'file_url']
