# 后端Dockerfile
# 使用Python作为基础镜像
FROM python:3.11-alpine

# 设置工作目录
WORKDIR /app

# 复制requirements.txt
COPY requirements.txt ./

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY . .

# 运行迁移
RUN python manage.py migrate

# 创建超级用户（可选，用于开发）
# RUN python manage.py createsuperuser --no-input --username admin --email admin@example.com

# 暴露端口
EXPOSE 8000

# 启动Django开发服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]