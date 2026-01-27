from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FileUploadViewSet, 
    FileUploadSingleView, 
    FileUploadMultipleView, 
    FileUploadConfigView, 
    FileUploadPreviewView
)

router = DefaultRouter()
router.register(r'files', FileUploadViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # 单文件上传
    path('single/', FileUploadSingleView.as_view({'post': 'create'}), name='upload-single'),
    # 多文件上传
    path('multiple/', FileUploadMultipleView.as_view({'post': 'create'}), name='upload-multiple'),
    # 获取上传配置
    path('config/', FileUploadConfigView.as_view({'get': 'list'}), name='upload-config'),
    # 文件预览
    path('preview/<int:pk>/', FileUploadPreviewView.as_view({'get': 'retrieve'}), name='upload-preview'),
]
