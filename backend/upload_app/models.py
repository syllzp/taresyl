from django.db import models
from django.contrib.auth.models import User
import os


def upload_to(instance, filename):
    """生成文件上传路径"""
    import uuid
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', str(instance.user.id), filename)


class FileUpload(models.Model):
    """文件上传模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_uploads', verbose_name='上传用户')
    file = models.FileField(upload_to=upload_to, verbose_name='上传文件')
    filename = models.CharField(max_length=255, verbose_name='原始文件名')
    file_size = models.IntegerField(verbose_name='文件大小（字节）')
    content_type = models.CharField(max_length=100, verbose_name='文件类型')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    
    class Meta:
        verbose_name = '文件上传'
        verbose_name_plural = '文件上传列表'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.filename
    
    @property
    def file_url(self):
        """获取文件URL"""
        if self.file:
            return self.file.url
        return None
