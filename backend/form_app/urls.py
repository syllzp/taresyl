from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormConfigViewSet

router = DefaultRouter()
router.register(r'form-configs', FormConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
]