from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class SystemLog(models.Model):
    """系统日志模型"""
    # 日志级别
    LOG_LEVELS = (
        ('DEBUG', '调试'),
        ('INFO', '信息'),
        ('WARNING', '警告'),
        ('ERROR', '错误'),
        ('CRITICAL', '严重'),
    )
    
    # 资源类型
    RESOURCE_TYPES = (
        ('FORM', '表单'),
        ('USER', '用户'),
        ('SYSTEM', '系统'),
        ('OTHER', '其他'),
    )
    
    level = models.CharField(
        max_length=10,
        choices=LOG_LEVELS,
        default='INFO',
        verbose_name='日志级别'
    )
    message = models.TextField(verbose_name='日志消息')
    resource_type = models.CharField(
        max_length=10,
        choices=RESOURCE_TYPES,
        blank=True,
        null=True,
        verbose_name='资源类型'
    )
    resource_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='资源ID'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='操作用户'
    )
    ip_address = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='操作IP地址'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='创建时间'
    )
    
    class Meta:
        verbose_name = '系统日志'
        verbose_name_plural = '系统日志'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"[{self.level}] {self.message[:50]}"
