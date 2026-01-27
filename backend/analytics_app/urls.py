from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsViewSet

urlpatterns = [
    # 提交量统计
    path('submission-count/', AnalyticsViewSet.as_view({'get': 'submission_count'}), name='analytics-submission-count'),
    # 字段数据分布
    path('field-distribution/', AnalyticsViewSet.as_view({'get': 'field_distribution'}), name='analytics-field-distribution'),
    # 数据趋势分析
    path('trend/', AnalyticsViewSet.as_view({'get': 'trend'}), name='analytics-trend'),
    # 导出统计报告
    path('export/', AnalyticsViewSet.as_view({'get': 'export'}), name='analytics-export'),
    # 自定义统计查询
    path('custom/', AnalyticsViewSet.as_view({'post': 'custom'}), name='analytics-custom'),
]
