from rest_framework import serializers
from .models import FormConfig

class FormConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormConfig
        fields = ['id', 'name', 'config', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']