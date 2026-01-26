# 前端Dockerfile
# 使用Node.js作为构建镜像
FROM node:20-alpine AS build

# 设置工作目录
WORKDIR /app

# 复制package*.json
COPY package*.json ./

# 安装依赖
RUN npm ci

# 全局安装vite
RUN npm install -g vite

# 复制源代码
COPY . .

# 添加调试信息
RUN echo "=== 调试信息 ==="
RUN echo "当前目录: $(pwd)"
RUN echo "文件列表: $(ls -la)"
RUN echo "Node版本: $(node --version)"
RUN echo "npm版本: $(npm --version)"
RUN echo "vite版本: $(vite --version || npx vite --version || echo 'vite not found')"
RUN echo "vite命令路径: $(which vite || echo 'vite not found')"
RUN echo "=== 开始构建 ==="

# 构建生产版本
RUN npm run build

# 使用Nginx作为运行时镜像
FROM nginx:alpine

# 复制构建产物到Nginx的html目录
COPY --from=build /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]