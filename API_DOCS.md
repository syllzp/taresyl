# API文档

本文档详细说明低代码表单项目的后端API接口，包括接口端点、请求格式、响应格式和使用示例。

## 技术栈

- **框架**: Django 5.2 + Django REST Framework
- **API文档**: drf-spectacular (自动生成OpenAPI文档)
- **数据格式**: JSON
- **认证**: 暂未实现（可根据需要添加）

## 基础信息

- **API基础URL**: `http://localhost:8000/api`
- **内容类型**: `application/json`
- **响应格式**: 标准RESTful JSON格式

## 自动生成的API文档

项目使用drf-spectacular自动生成OpenAPI文档，提供两种UI风格：

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **Redoc**: `http://localhost:8000/api/redoc/`

## 端点列表

### 1. 表单配置管理

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/form-configs/` | 获取所有表单配置 |
| POST | `/api/form-configs/` | 创建新的表单配置 |
| GET | `/api/form-configs/{id}/` | 获取单个表单配置 |
| PUT | `/api/form-configs/{id}/` | 更新表单配置 |
| PATCH | `/api/form-configs/{id}/` | 部分更新表单配置 |
| DELETE | `/api/form-configs/{id}/` | 删除表单配置 |

### 2. API文档

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/schema/` | 获取OpenAPI schema |
| GET | `/api/docs/` | Swagger UI文档 |
| GET | `/api/redoc/` | Redoc文档 |

## 数据模型

### FormConfig

```json
{
  "id": 1,
  "name": "用户注册表单",
  "config": "{\"components\": [...], \"settings\": {...}}",
  "created_at": "2026-01-26T12:00:00Z",
  "updated_at": "2026-01-26T12:30:00Z"
}
```

- **id**: 表单配置ID (只读)
- **name**: 表单名称 (必填)
- **config**: 表单配置JSON字符串 (必填)
- **created_at**: 创建时间 (只读)
- **updated_at**: 更新时间 (只读)

## 请求和响应示例

### 1. 获取所有表单配置

**请求**:
```bash
GET /api/form-configs/
```

**响应** (200 OK):
```json
[
  {
    "id": 1,
    "name": "用户注册表单",
    "config": "{\"components\": [{\"type\": \"text\", \"label\": \"用户名\", \"key\": \"username\"}], \"settings\": {}}",
    "created_at": "2026-01-26T12:00:00Z",
    "updated_at": "2026-01-26T12:00:00Z"
  },
  {
    "id": 2,
    "name": "联系我们表单",
    "config": "{\"components\": [{\"type\": \"text\", \"label\": \"姓名\", \"key\": \"name\"}, {\"type\": \"email\", \"label\": \"邮箱\", \"key\": \"email\"}], \"settings\": {}}",
    "created_at": "2026-01-25T10:00:00Z",
    "updated_at": "2026-01-25T10:00:00Z"
  }
]
```

### 2. 创建新的表单配置

**请求**:
```bash
POST /api/form-configs/
Content-Type: application/json

{
  "name": "登录表单",
  "config": "{\"components\": [{\"type\": \"text\", \"label\": \"用户名\", \"key\": \"username\"}, {\"type\": \"password\", \"label\": \"密码\", \"key\": \"password\"}], \"settings\": {}}",
}
```

**响应** (201 Created):
```json
{
  "id": 3,
  "name": "登录表单",
  "config": "{\"components\": [{\"type\": \"text\", \"label\": \"用户名\", \"key\": \"username\"}, {\"type\": \"password\", \"label\": \"密码\", \"key\": \"password\"}], \"settings\": {}}",
  "created_at": "2026-01-26T13:00:00Z",
  "updated_at": "2026-01-26T13:00:00Z"
}
```

### 3. 获取单个表单配置

**请求**:
```bash
GET /api/form-configs/1/
```

**响应** (200 OK):
```json
{
  "id": 1,
  "name": "用户注册表单",
  "config": "{\"components\": [{\"type\": \"text\", \"label\": \"用户名\", \"key\": \"username\"}], \"settings\": {}}",
  "created_at": "2026-01-26T12:00:00Z",
  "updated_at": "2026-01-26T12:00:00Z"
}
```

### 4. 更新表单配置

**请求**:
```bash
PUT /api/form-configs/1/
Content-Type: application/json

{
  "name": "用户注册表单（更新版）",
  "config": "{\"components\": [{\"type\": \"text\", \"label\": \"用户名\", \"key\": \"username\"}, {\"type\": \"email\", \"label\": \"邮箱\", \"key\": \"email\"}], \"settings\": {}}",
}
```

**响应** (200 OK):
```json
{
  "id": 1,
  "name": "用户注册表单（更新版）",
  "config": "{\"components\": [{\"type\": \"text\", \"label\": \"用户名\", \"key\": \"username\"}, {\"type\": \"email\", \"label\": \"邮箱\", \"key\": \"email\"}], \"settings\": {}}",
  "created_at": "2026-01-26T12:00:00Z",
  "updated_at": "2026-01-26T13:30:00Z"
}
```

### 5. 部分更新表单配置

**请求**:
```bash
PATCH /api/form-configs/1/
Content-Type: application/json

{
  "name": "用户注册表单（最终版）"
}
```

**响应** (200 OK):
```json
{
  "id": 1,
  "name": "用户注册表单（最终版）",
  "config": "{\"components\": [{\"type\": \"text\", \"label\": \"用户名\", \"key\": \"username\"}, {\"type\": \"email\", \"label\": \"邮箱\", \"key\": \"email\"}], \"settings\": {}}",
  "created_at": "2026-01-26T12:00:00Z",
  "updated_at": "2026-01-26T13:45:00Z"
}
```

### 6. 删除表单配置

**请求**:
```bash
DELETE /api/form-configs/1/
```

**响应** (204 No Content):
```
# 无响应体
```

## 错误处理

### 常见错误响应

#### 400 Bad Request

当请求数据无效时返回：

```json
{
  "name": ["该字段为必填项。"],
  "config": ["该字段为必填项。"]
}
```

#### 404 Not Found

当请求的资源不存在时返回：

```json
{
  "detail": "Not found."
}
```

#### 500 Internal Server Error

当服务器内部错误时返回：

```json
{
  "detail": "Internal Server Error"
}
```

## 前端集成示例

### Vue 3 + Axios 示例

```javascript
import axios from 'axios'

// 配置axios默认值
axios.defaults.baseURL = 'http://localhost:8000'

// 获取所有表单配置
const fetchForms = async () => {
  try {
    const response = await axios.get('/api/form-configs/')
    return response.data
  } catch (error) {
    console.error('获取表单配置失败', error)
    return []
  }
}

// 创建新表单
const createForm = async (formData) => {
  try {
    const response = await axios.post('/api/form-configs/', formData)
    return response.data
  } catch (error) {
    console.error('创建表单失败', error)
    throw error
  }
}

// 更新表单
const updateForm = async (id, formData) => {
  try {
    const response = await axios.put(`/api/form-configs/${id}/`, formData)
    return response.data
  } catch (error) {
    console.error('更新表单失败', error)
    throw error
  }
}

// 删除表单
const deleteForm = async (id) => {
  try {
    await axios.delete(`/api/form-configs/${id}/`)
    return true
  } catch (error) {
    console.error('删除表单失败', error)
    throw error
  }
}
```

## 高级用法

### 1. 表单配置JSON结构

表单配置JSON遵循vform3-builds的格式规范，基本结构如下：

```json
{
  "components": [
    {
      "type": "text",
      "label": "字段标签",
      "key": "field_key",
      "validate": {
        "required": true,
        "pattern": "",
        "minLength": 0,
        "maxLength": 0
      },
      "defaultValue": "",
      "placeholder": "请输入"
    }
  ],
  "settings": {
    "labelWidth": 100,
    "size": "medium",
    "labelPosition": "left",
    "hideRequiredMark": false,
    "customClass": ""
  }
}
```

### 2. 支持的表单组件类型

- **基础组件**: text, password, number, textarea, select, radio, checkbox, switch, date, time, datetime, upload
- **布局组件**: grid, subform, tabs
- **高级组件**: cascader, color-picker, rate, slider, transfer, tree-select

### 3. 性能优化

- **分页查询**: 当表单配置数量较多时，建议使用分页查询
- **缓存策略**: 可根据实际需求添加缓存机制
- **批量操作**: 如需批量处理表单配置，可考虑添加批量操作端点

## 扩展建议

1. **添加认证授权**: 集成JWT或OAuth2，实现API访问控制
2. **添加表单数据存储**: 创建FormData模型，存储用户提交的表单数据
3. **添加版本控制**: 实现表单配置的版本管理
4. **添加权限管理**: 基于Django的权限系统，控制表单配置的访问权限
5. **添加搜索功能**: 支持根据表单名称、创建时间等条件搜索表单配置

## 故障排查

### 常见问题及解决方案

1. **API无法访问**
   - 检查后端服务是否正在运行
   - 检查CORS配置是否正确
   - 检查API URL是否正确

2. **表单配置保存失败**
   - 检查config字段是否为有效的JSON字符串
   - 检查name字段是否已填写
   - 检查网络连接是否正常

3. **表单渲染错误**
   - 检查表单配置JSON格式是否正确
   - 检查vform3-builds版本是否兼容
   - 检查前端代码是否正确处理配置数据

## 联系信息

如有问题或建议，请通过GitHub Issues与我们联系。
