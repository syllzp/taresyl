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

# 暴露端口
EXPOSE 8000

# 启动Django开发服务器
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]