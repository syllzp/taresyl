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

# 构建生产版本
RUN npm run build

# 使用Nginx作为运行时镜像
FROM nginx:alpine

# 复制构建产物到Nginx的html目录
COPY --from=build /app/dist /usr/share/nginx/html

# 添加Nginx配置，将API请求代理到后端
COPY <<EOF /etc/nginx/conf.d/default.conf
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    # 将API请求代理到后端容器
    location /api {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
EOF

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]