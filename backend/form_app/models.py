from django.db import models
from django.contrib.auth.models import User

class FormConfig(models.Model):
    name = models.CharField(max_length=255, verbose_name='表单名称')
    config = models.TextField(verbose_name='表单配置JSON')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '表单配置'
        verbose_name_plural = '表单配置列表'
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.name


class FormData(models.Model):
    """表单数据存储模型"""
    form_config = models.ForeignKey(FormConfig, on_delete=models.CASCADE, related_name='form_data', verbose_name='关联表单配置')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='form_data', verbose_name='提交用户')
    data = models.JSONField(verbose_name='表单数据')
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '表单数据'
        verbose_name_plural = '表单数据列表'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f'FormData #{self.id} for {self.form_config.name}'


class TemplateCategory(models.Model):
    """模板分类模型"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '模板分类'
        verbose_name_plural = '模板分类列表'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class FormTemplate(models.Model):
    """表单模板模型"""
    name = models.CharField(max_length=255, verbose_name='模板名称')
    description = models.TextField(blank=True, verbose_name='模板描述')
    config = models.TextField(verbose_name='表单配置JSON')
    category = models.ForeignKey(TemplateCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='templates', verbose_name='模板分类')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates', verbose_name='创建用户')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    usage_count = models.IntegerField(default=0, verbose_name='使用次数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '表单模板'
        verbose_name_plural = '表单模板列表'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
