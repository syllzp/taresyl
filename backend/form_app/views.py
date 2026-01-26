from rest_framework import viewsets
from .models import FormConfig
from .serializers import FormConfigSerializer

class FormConfigViewSet(viewsets.ModelViewSet):
    queryset = FormConfig.objects.all()
    serializer_class = FormConfigSerializer
