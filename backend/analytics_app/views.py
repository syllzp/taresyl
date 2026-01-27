from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Count, Sum, DateTimeField
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.utils import timezone
from form_app.models import FormConfig, FormData
import json
import pandas as pd
from io import BytesIO
import base64


class AnalyticsViewSet(viewsets.ViewSet):
    """表单统计分析视图集"""
    permission_classes = [permissions.IsAuthenticated]
    
    def submission_count(self, request):
        """提交量统计"""
        form_id = request.query_params.get('form_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = FormData.objects.all()
        
        if form_id:
            queryset = queryset.filter(form_config_id=form_id)
        
        if start_date:
            queryset = queryset.filter(submitted_at__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(submitted_at__lte=end_date)
        
        total_count = queryset.count()
        
        # 按日期分组统计
        daily_counts = queryset.annotate(
            date=TruncDay('submitted_at', output_field=DateTimeField())
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        return Response({
            'total_count': total_count,
            'daily_counts': list(daily_counts)
        })
    
    def field_distribution(self, request):
        """字段数据分布"""
        form_id = request.query_params.get('form_id')
        field_key = request.query_params.get('field_key')
        
        if not form_id or not field_key:
            return Response(
                {'error': '必须提供form_id和field_key参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = FormData.objects.filter(form_config_id=form_id)
        
        # 统计字段值分布
        distribution = {}
        for form_data in queryset:
            data = form_data.data
            if isinstance(data, dict) and field_key in data:
                value = data[field_key]
                if value:
                    if isinstance(value, list):
                        # 处理多选字段
                        for v in value:
                            distribution[str(v)] = distribution.get(str(v), 0) + 1
                    else:
                        distribution[str(value)] = distribution.get(str(value), 0) + 1
        
        # 按数量排序
        sorted_distribution = dict(sorted(
            distribution.items(),
            key=lambda item: item[1],
            reverse=True
        ))
        
        return Response({
            'field_key': field_key,
            'distribution': sorted_distribution,
            'total_count': len(queryset)
        })
    
    def trend(self, request):
        """数据趋势分析"""
        form_id = request.query_params.get('form_id')
        interval = request.query_params.get('interval', 'day')  # day, week, month
        
        queryset = FormData.objects.all()
        
        if form_id:
            queryset = queryset.filter(form_config_id=form_id)
        
        # 根据间隔分组
        if interval == 'day':
            annotated_queryset = queryset.annotate(
                period=TruncDay('submitted_at', output_field=DateTimeField())
            )
        elif interval == 'week':
            annotated_queryset = queryset.annotate(
                period=TruncWeek('submitted_at', output_field=DateTimeField())
            )
        elif interval == 'month':
            annotated_queryset = queryset.annotate(
                period=TruncMonth('submitted_at', output_field=DateTimeField())
            )
        else:
            return Response(
                {'error': 'interval参数必须是day、week或month'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 统计每个时间段的提交量
        trend_data = annotated_queryset.values('period').annotate(
            count=Count('id')
        ).order_by('period')
        
        return Response({
            'interval': interval,
            'trend_data': list(trend_data)
        })
    
    def export(self, request):
        """导出统计报告"""
        form_id = request.query_params.get('form_id')
        format = request.query_params.get('format', 'json')  # json, csv, excel
        
        if not form_id:
            return Response(
                {'error': '必须提供form_id参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            form_config = FormConfig.objects.get(id=form_id)
        except FormConfig.DoesNotExist:
            return Response(
                {'error': '表单不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        queryset = FormData.objects.filter(form_config_id=form_id)
        
        # 构建报告数据
        report_data = {
            'form_name': form_config.name,
            'total_submissions': queryset.count(),
            'generated_at': timezone.now().isoformat(),
            'data': []
        }
        
        for form_data in queryset:
            report_data['data'].append({
                'id': form_data.id,
                'submitted_at': form_data.submitted_at.isoformat(),
                'data': form_data.data
            })
        
        # 根据格式导出
        if format == 'json':
            return Response(report_data)
        elif format == 'csv':
            # 构建CSV数据
            df = pd.DataFrame(report_data['data'])
            output = BytesIO()
            df.to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)
            
            # 编码为base64以便返回
            csv_data = base64.b64encode(output.read()).decode('utf-8')
            
            return Response({
                'filename': f'{form_config.name}_report.csv',
                'data': csv_data,
                'format': 'csv'
            })
        elif format == 'excel':
            # 构建Excel数据
            df = pd.DataFrame(report_data['data'])
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Form Data')
            output.seek(0)
            
            # 编码为base64以便返回
            excel_data = base64.b64encode(output.read()).decode('utf-8')
            
            return Response({
                'filename': f'{form_config.name}_report.xlsx',
                'data': excel_data,
                'format': 'excel'
            })
        else:
            return Response(
                {'error': 'format参数必须是json、csv或excel'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def custom(self, request):
        """自定义统计查询"""
        try:
            query_params = request.data
        except Exception as e:
            return Response(
                {'error': '请求数据格式错误'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        form_id = query_params.get('form_id')
        aggregations = query_params.get('aggregations', [])
        group_by = query_params.get('group_by')
        
        if not form_id:
            return Response(
                {'error': '必须提供form_id参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = FormData.objects.filter(form_config_id=form_id)
        
        # 执行自定义聚合
        results = []
        
        # 这里实现简单的自定义聚合逻辑
        # 实际应用中可能需要更复杂的处理
        
        return Response({
            'results': results,
            'total_count': queryset.count()
        })
