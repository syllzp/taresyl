# GitHub Packages配置说明

## 1. 登录GitHub Packages
```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin
```

## 2. 构建镜像
```bash
# 前端
docker build -t ghcr.io/syllzp/taresyl-frontend:latest ./frontend

# 后端
docker build -t ghcr.io/syllzp/taresyl-backend:latest ./backend
```

## 3. 推送镜像
```bash
# 前端
docker push ghcr.io/syllzp/taresyl-frontend:latest

# 后端
docker push ghcr.io/syllzp/taresyl-backend:latest
```

## 4. CI/CD配置
在GitHub Actions中使用以下步骤推送镜像到GitHub Packages：

```yaml
- name: Login to GitHub Packages
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.repository_owner }}
    password: ${{ secrets.GITHUB_TOKEN }}

- name: Build and push frontend image
  uses: docker/build-push-action@v5
  with:
    context: ./frontend
    file: ./frontend/Dockerfile
    push: true
    tags: ghcr.io/syllzp/taresyl-frontend:${{ github.sha }},ghcr.io/syllzp/taresyl-frontend:latest

- name: Build and push backend image
  uses: docker/build-push-action@v5
  with:
    context: ./backend
    file: ./backend/Dockerfile
    push: true
    tags: ghcr.io/syllzp/taresyl-backend:${{ github.sha }},ghcr.io/syllzp/taresyl-backend:latest
```

## 5. 使用GitHub Packages中的镜像
```bash
# 拉取镜像
docker pull ghcr.io/syllzp/taresyl-frontend:latest
docker pull ghcr.io/syllzp/taresyl-backend:latest

# 运行容器
docker run -d -p 3000:80 ghcr.io/syllzp/taresyl-frontend:latest
docker run -d -p 8000:8000 ghcr.io/syllzp/taresyl-backend:latest
```
