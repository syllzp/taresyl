from rest_framework import serializers
from .models import FormConfig, FormData, TemplateCategory, FormTemplate

class FormConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormConfig
        fields = ['id', 'name', 'config', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class FormDataSerializer(serializers.ModelSerializer):
    """表单数据序列化器"""
    class Meta:
        model = FormData
        fields = ['id', 'form_config', 'user', 'data', 'submitted_at', 'updated_at']
        read_only_fields = ['id', 'user', 'submitted_at', 'updated_at']


class FormDataListSerializer(serializers.ModelSerializer):
    """表单数据列表序列化器，包含表单配置信息"""
    form_config_name = serializers.CharField(source='form_config.name', read_only=True)
    
    class Meta:
        model = FormData
        fields = ['id', 'form_config', 'form_config_name', 'data', 'submitted_at', 'updated_at']
        read_only_fields = ['id', 'form_config_name', 'submitted_at', 'updated_at']


class TemplateCategorySerializer(serializers.ModelSerializer):
    """模板分类序列化器"""
    class Meta:
        model = TemplateCategory
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class FormTemplateSerializer(serializers.ModelSerializer):
    """表单模板序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = FormTemplate
        fields = ['id', 'name', 'description', 'config', 'category', 'category_name', 'user', 'user_username', 'is_public', 'usage_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'user_username', 'usage_count', 'created_at', 'updated_at']


class FormTemplateListSerializer(serializers.ModelSerializer):
    """表单模板列表序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = FormTemplate
        fields = ['id', 'name', 'description', 'category', 'category_name', 'is_public', 'usage_count', 'created_at']
        read_only_fields = ['id', 'category_name', 'usage_count', 'created_at']