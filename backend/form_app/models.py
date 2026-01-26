from django.db import models

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
