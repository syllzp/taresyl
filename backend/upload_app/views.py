from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.conf import settings
from .models import FileUpload
from .serializers import FileUploadSerializer, FileUploadListSerializer
import os


class FileUploadViewSet(viewsets.ModelViewSet):
    """文件上传管理视图集"""
    queryset = FileUpload.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FileUploadListSerializer
        return FileUploadSerializer
    
    def get_queryset(self):
        # 只返回当前用户的文件
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # 自动关联当前用户
        file = self.request.FILES.get('file')
        if file:
            serializer.save(
                user=self.request.user,
                filename=file.name,
                file_size=file.size,
                content_type=file.content_type
            )


class FileUploadSingleView(viewsets.ViewSet):
    """单文件上传视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request):
        """上传单个文件"""
        file = request.FILES.get('file')
        if not file:
            return Response({'error': '请选择要上传的文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查文件大小
        if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            return Response({'error': f'文件大小不能超过{settings.FILE_UPLOAD_MAX_MEMORY_SIZE / 1024 / 1024:.1f}MB'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建文件上传记录
        file_upload = FileUpload.objects.create(
            user=request.user,
            file=file,
            filename=file.name,
            file_size=file.size,
            content_type=file.content_type
        )
        
        serializer = FileUploadSerializer(file_upload)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FileUploadMultipleView(viewsets.ViewSet):
    """多文件上传视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request):
        """上传多个文件"""
        files = request.FILES.getlist('files')
        if not files:
            return Response({'error': '请选择要上传的文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_files = []
        for file in files:
            # 检查文件大小
            if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                return Response({'error': f'文件 {file.name} 大小不能超过{settings.FILE_UPLOAD_MAX_MEMORY_SIZE / 1024 / 1024:.1f}MB'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 创建文件上传记录
            file_upload = FileUpload.objects.create(
                user=request.user,
                file=file,
                filename=file.name,
                file_size=file.size,
                content_type=file.content_type
            )
            uploaded_files.append(FileUploadSerializer(file_upload).data)
        
        return Response({'files': uploaded_files}, status=status.HTTP_201_CREATED)


class FileUploadConfigView(viewsets.ViewSet):
    """文件上传配置视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """获取上传配置"""
        config = {
            'max_file_size': settings.FILE_UPLOAD_MAX_MEMORY_SIZE,
            'max_file_size_mb': settings.FILE_UPLOAD_MAX_MEMORY_SIZE / 1024 / 1024,
            'allowed_extensions': ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'],
            'media_url': settings.MEDIA_URL
        }
        return Response(config)


class FileUploadPreviewView(viewsets.ViewSet):
    """文件预览视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request, pk=None):
        """获取文件预览信息"""
        try:
            file_upload = FileUpload.objects.get(id=pk, user=request.user)
            return Response({
                'id': file_upload.id,
                'filename': file_upload.filename,
                'file_size': file_upload.file_size,
                'content_type': file_upload.content_type,
                'file_url': file_upload.file_url
            })
        except FileUpload.DoesNotExist:
            return Response({'error': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)
