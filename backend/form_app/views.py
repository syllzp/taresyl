from rest_framework import viewsets, permissions
from .models import FormConfig
from .serializers import FormConfigSerializer


class FormConfigViewSet(viewsets.ModelViewSet):
    queryset = FormConfig.objects.all()
    serializer_class = FormConfigSerializer
    permission_classes = [permissions.AllowAny]
