from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImportExportViewSet

urlpatterns = [
    # 导出表单配置
    path('form/<int:pk>/export/', ImportExportViewSet.as_view({'get': 'export_form_config'}), name='import-export-form-export'),
    # 导出表单数据
    path('form/<int:form_id>/data/export/', ImportExportViewSet.as_view({'get': 'export_form_data'}), name='import-export-form-data-export'),
    # 导入表单配置
    path('form/import/', ImportExportViewSet.as_view({'post': 'import_form_config'}), name='import-export-form-import'),
    # 导入表单数据
    path('form/<int:form_id>/data/import/', ImportExportViewSet.as_view({'post': 'import_form_data'}), name='import-export-form-data-import'),
    # 导出模板
    path('templates/export/', ImportExportViewSet.as_view({'get': 'export_templates'}), name='import-export-templates-export'),
    # 导入模板
    path('templates/import/', ImportExportViewSet.as_view({'post': 'import_templates'}), name='import-export-templates-import'),
]
