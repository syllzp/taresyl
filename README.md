# 低代码表单项目

一个基于前后端分离架构的低代码表单设计平台，前端使用Vue 3 + vform3-builds实现可视化表单设计，后端使用Django + DRF实现表单配置的存储和管理。

## 功能特性

- 🎨 **可视化表单设计**: 拖拽式表单设计器，支持多种表单控件
- 💾 **表单配置管理**: 完整的CRUD操作，支持表单配置的存储、查询、更新和删除
- 📱 **响应式设计**: 适配各种屏幕尺寸，支持移动端预览
- 🔌 **API集成**: 自动生成RESTful API，支持与其他系统集成
- 📋 **表单数据管理**: 支持表单数据的提交、存储和查询
- 📖 **自动API文档**: 使用drf-spectacular生成Swagger UI和Redoc文档
- 🐳 **容器化部署**: 支持Docker和Docker Compose快速部署
- 🔄 **CI/CD集成**: 自动构建和推送镜像到GitHub Packages

## 技术栈

### 前端
- **框架**: Vue 3 + Vite
- **低代码表单**: vform3-builds
- **UI组件库**: Element Plus
- **HTTP客户端**: Axios

### 后端
- **框架**: Django 5.2
- **API框架**: Django REST Framework
- **CORS**: django-cors-headers
- **API文档**: drf-spectacular

### 容器化
- **前端**: Nginx + Node.js 20
- **后端**: Python 3.11
- **容器注册表**: GitHub Packages (ghcr.io)

### CI/CD
- **持续集成**: GitHub Actions
- **镜像构建**: Docker Buildx

## 快速开始

### 环境要求
- Docker
- Docker Compose
- Python 3.11+ (可选，用于本地开发)
- Node.js 20+ (可选，用于本地开发)

### Docker部署

1. **拉取代码**
   ```bash
   git clone https://github.com/syllzp/taresyl.git
   cd taresyl
   ```

2. **启动服务**
   ```bash
   docker-compose up -d
   ```

3. **访问应用**
   - 前端应用: http://localhost
   - 后端API: http://localhost:8000/api
   - Swagger UI文档: http://localhost:8000/api/docs/
   - Redoc文档: http://localhost:8000/api/redoc/

### 本地开发

#### 后端开发

1. **创建虚拟环境**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行迁移**
   ```bash
   python manage.py migrate
   ```

4. **启动开发服务器**
   ```bash
   python manage.py runserver
   ```

#### 前端开发

1. **安装依赖**
   ```bash
   cd frontend
   npm install
   ```

2. **启动开发服务器**
   ```bash
   npm run dev
   ```

3. **访问应用**
   - 前端应用: http://localhost:3000
   - API代理已配置，指向 http://localhost:8000

## 项目结构

```
taresyl/
├── frontend/                  # 前端项目
│   ├── src/
│   │   ├── App.vue            # 主应用组件
│   │   ├── main.js            # 应用入口
│   │   └── vite-env.d.ts      # Vite环境类型定义
│   ├── Dockerfile             # 前端Dockerfile
│   ├── package.json           # 前端依赖
│   └── vite.config.js         # Vite配置
├── backend/                   # 后端项目
│   ├── core/                  # Django项目配置
│   │   ├── settings.py        # 项目配置
│   │   ├── urls.py            # 项目URL配置
│   │   └── wsgi.py            # WSGI配置
│   ├── form_app/              # 表单应用
│   │   ├── models.py          # 数据模型
│   │   ├── serializers.py     # 序列化器
│   │   ├── views.py           # 视图集
│   │   └── urls.py            # 应用URL配置
│   ├── Dockerfile             # 后端Dockerfile
│   ├── requirements.txt       # 后端依赖
│   └── manage.py              # Django管理脚本
├── .github/
│   └── workflows/
│       └── docker-build-deploy.yml  # GitHub Actions工作流
├── docker-compose.yml         # Docker Compose配置
└── README.md                  # 项目文档
```

## 核心功能说明

### 表单设计器

- **拖拽式设计**: 支持从组件库拖拽表单控件到设计区域
- **实时预览**: 设计过程中实时查看表单效果
- **表单配置导出**: 支持将设计好的表单配置导出为JSON格式
- **表单配置导入**: 支持导入JSON配置恢复表单设计

### 表单配置管理

- **配置存储**: 将表单配置存储到后端数据库
- **版本管理**: 支持表单配置的版本控制
- **权限控制**: 基于Django的权限系统，控制表单配置的访问权限
- **搜索功能**: 支持根据表单名称、创建时间等条件搜索表单配置

### 表单渲染

- **动态渲染**: 根据表单配置动态渲染表单
- **表单验证**: 支持前端和后端双重验证
- **数据提交**: 支持将表单数据提交到后端存储
- **表单联动**: 支持表单控件之间的联动效果

## API文档

### 自动生成的API文档

项目使用drf-spectacular自动生成OpenAPI文档，提供两种UI风格：

- **Swagger UI**: http://localhost:8000/api/docs/
  - 交互式API文档，支持在线测试API
  - 直观的界面，适合开发人员使用

- **Redoc**: http://localhost:8000/api/redoc/
  - 现代化的API文档，支持响应式设计
  - 适合作为最终文档提供给用户

### API端点

- **表单配置管理**:
  - `GET /api/form-configs/` - 获取所有表单配置
  - `POST /api/form-configs/` - 创建新的表单配置
  - `GET /api/form-configs/{id}/` - 获取单个表单配置
  - `PUT /api/form-configs/{id}/` - 更新表单配置
  - `DELETE /api/form-configs/{id}/` - 删除表单配置

## CI/CD

项目使用GitHub Actions实现持续集成和部署：

1. **触发条件**: 推送到main分支或创建PR
2. **构建步骤**:
   - 检出代码
   - 设置Docker Buildx
   - 登录到GitHub Packages
   - 构建并推送前端镜像
   - 构建并推送后端镜像
3. **镜像标签**:
   - `ghcr.io/syllzp/taresyl-frontend:latest`
   - `ghcr.io/syllzp/taresyl-backend:latest`
   - `ghcr.io/syllzp/taresyl-frontend:{sha}`
   - `ghcr.io/syllzp/taresyl-backend:{sha}`

## 开发指南

### 前端开发

1. **表单设计器**: `frontend/src/App.vue`
2. **API请求**: 使用Axios，基础URL已配置
3. **组件库**: 使用Element Plus，已全局注册
4. **开发流程**:
   - 启动开发服务器: `npm run dev`
   - 构建生产版本: `npm run build`
   - 代码检查: `npm run lint`

### 后端开发

1. **数据模型**: `backend/form_app/models.py`
2. **API视图**: `backend/form_app/views.py`
3. **序列化器**: `backend/form_app/serializers.py`
4. **API路由**: `backend/form_app/urls.py`
5. **开发流程**:
   - 启动开发服务器: `python manage.py runserver`
   - 创建迁移: `python manage.py makemigrations`
   - 运行迁移: `python manage.py migrate`
   - 创建超级用户: `python manage.py createsuperuser`

### 容器化开发

1. **前端镜像构建**: `docker build -t ghcr.io/syllzp/taresyl-frontend:latest frontend/`
2. **后端镜像构建**: `docker build -t ghcr.io/syllzp/taresyl-backend:latest backend/`
3. **测试镜像**: `docker-compose up -d`
4. **查看日志**: `docker-compose logs -f`

## 配置说明

### 前端配置

- **API地址**: 在`vite.config.js`中配置`server.proxy`
- **构建配置**: 在`vite.config.js`中配置构建选项
- **依赖管理**: 在`package.json`中管理前端依赖

### 后端配置

- **数据库配置**: 在`backend/core/settings.py`中配置`DATABASES`
- **CORS配置**: 在`backend/core/settings.py`中配置`CORS_ALLOW_ALL_ORIGINS`
- **API文档配置**: 在`backend/core/settings.py`中配置`SPECTACULAR_SETTINGS`
- **依赖管理**: 在`backend/requirements.txt`中管理后端依赖

## 常见问题

### 1. 前端无法连接到后端API

- 检查后端服务是否正在运行
- 检查CORS配置是否正确
- 检查API代理配置是否正确

### 2. Docker构建失败

- 检查Docker版本是否支持Buildx
- 检查网络连接是否正常
- 检查Dockerfile语法是否正确

### 3. API文档无法访问

- 检查drf-spectacular是否已正确安装
- 检查URL配置是否正确
- 检查Django应用是否已添加到INSTALLED_APPS

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请通过GitHub Issues与我们联系。