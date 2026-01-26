# 前端Dockerfile
# 使用Node.js作为构建镜像
FROM node:20-alpine AS build

# 设置工作目录
WORKDIR /app

# 复制package*.json
COPY package*.json ./

# 安装依赖
RUN npm ci

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# 使用Nginx作为运行时镜像
FROM nginx:alpine

# 复制构建产物到Nginx的html目录
COPY --from=build /app/dist /usr/share/nginx/html

# 复制自定义Nginx配置（如果需要）
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]