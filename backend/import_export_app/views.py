from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from form_app.models import FormConfig, FormData, FormTemplate
from form_app.serializers import FormConfigSerializer, FormDataSerializer, FormTemplateSerializer
import json
import pandas as pd
from io import BytesIO
import base64


class ImportExportViewSet(viewsets.ViewSet):
    """表单导出/导入视图集"""
    permission_classes = [permissions.IsAuthenticated]
    
    def export_form_config(self, request, pk=None):
        """导出表单配置"""
        try:
            form_config = FormConfig.objects.get(id=pk)
        except FormConfig.DoesNotExist:
            return Response(
                {'error': '表单配置不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 构建导出数据
        export_data = {
            'name': form_config.name,
            'config': json.loads(form_config.config) if form_config.config else {}
        }
        
        return Response(export_data)
    
    def export_form_data(self, request, form_id=None):
        """导出表单数据"""
        try:
            form_config = FormConfig.objects.get(id=form_id)
        except FormConfig.DoesNotExist:
            return Response(
                {'error': '表单配置不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        format = request.query_params.get('format', 'json')  # json, csv, excel
        
        queryset = FormData.objects.filter(form_config_id=form_id)
        
        # 构建导出数据
        data_list = []
        for form_data in queryset:
            data_list.append({
                'id': form_data.id,
                'submitted_at': form_data.submitted_at.isoformat(),
                'data': form_data.data
            })
        
        # 根据格式导出
        if format == 'json':
            return Response({
                'form_name': form_config.name,
                'total_records': len(data_list),
                'data': data_list
            })
        elif format == 'csv':
            # 构建CSV数据
            # 先将嵌套的data字段展平
            flattened_data = []
            for item in data_list:
                flattened = {
                    'id': item['id'],
                    'submitted_at': item['submitted_at']
                }
                if isinstance(item['data'], dict):
                    for key, value in item['data'].items():
                        flattened[key] = value
                flattened_data.append(flattened)
            
            df = pd.DataFrame(flattened_data)
            output = BytesIO()
            df.to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)
            
            # 编码为base64以便返回
            csv_data = base64.b64encode(output.read()).decode('utf-8')
            
            return Response({
                'filename': f'{form_config.name}_data.csv',
                'data': csv_data,
                'format': 'csv'
            })
        elif format == 'excel':
            # 构建Excel数据
            # 先将嵌套的data字段展平
            flattened_data = []
            for item in data_list:
                flattened = {
                    'id': item['id'],
                    'submitted_at': item['submitted_at']
                }
                if isinstance(item['data'], dict):
                    for key, value in item['data'].items():
                        flattened[key] = value
                flattened_data.append(flattened)
            
            df = pd.DataFrame(flattened_data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Form Data')
            output.seek(0)
            
            # 编码为base64以便返回
            excel_data = base64.b64encode(output.read()).decode('utf-8')
            
            return Response({
                'filename': f'{form_config.name}_data.xlsx',
                'data': excel_data,
                'format': 'excel'
            })
        else:
            return Response(
                {'error': 'format参数必须是json、csv或excel'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def import_form_config(self, request):
        """导入表单配置"""
        try:
            import_data = request.data
        except Exception as e:
            return Response(
                {'error': '请求数据格式错误'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        name = import_data.get('name')
        config = import_data.get('config')
        
        if not name or not config:
            return Response(
                {'error': '必须提供name和config参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建新的表单配置
        form_config = FormConfig.objects.create(
            name=name,
            config=json.dumps(config)
        )
        
        serializer = FormConfigSerializer(form_config)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def import_form_data(self, request, form_id=None):
        """导入表单数据"""
        try:
            form_config = FormConfig.objects.get(id=form_id)
        except FormConfig.DoesNotExist:
            return Response(
                {'error': '表单配置不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            import_data = request.data.get('data', [])
        except Exception as e:
            return Response(
                {'error': '请求数据格式错误'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(import_data, list):
            return Response(
                {'error': 'data必须是列表'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 导入数据
        imported_count = 0
        for item in import_data:
            data = item.get('data')
            if data:
                FormData.objects.create(
                    form_config=form_config,
                    user=request.user,
                    data=data
                )
                imported_count += 1
        
        return Response({
            'imported_count': imported_count,
            'form_id': form_id
        })
    
    def export_templates(self, request):
        """导出模板"""
        template_ids = request.query_params.getlist('ids', [])
        
        queryset = FormTemplate.objects.all()
        
        if template_ids:
            queryset = queryset.filter(id__in=template_ids)
        
        # 构建导出数据
        templates = []
        for template in queryset:
            templates.append({
                'name': template.name,
                'description': template.description,
                'config': json.loads(template.config) if template.config else {},
                'is_public': template.is_public
            })
        
        return Response({
            'total_templates': len(templates),
            'templates': templates
        })
    
    def import_templates(self, request):
        """导入模板"""
        try:
            import_data = request.data.get('templates', [])
        except Exception as e:
            return Response(
                {'error': '请求数据格式错误'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(import_data, list):
            return Response(
                {'error': 'templates必须是列表'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 导入模板
        imported_count = 0
        for template_data in import_data:
            name = template_data.get('name')
            config = template_data.get('config')
            
            if name and config:
                FormTemplate.objects.create(
                    name=name,
                    description=template_data.get('description', ''),
                    config=json.dumps(config),
                    user=request.user,
                    is_public=template_data.get('is_public', False)
                )
                imported_count += 1
        
        return Response({
            'imported_count': imported_count
        })
