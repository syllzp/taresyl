import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 自动添加认证令牌
apiClient.interceptors.request.use(
  (config) => {
    // 从本地存储中获取令牌
    const token = localStorage.getItem('token')
    // 如果令牌存在，添加到请求头
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误和令牌刷新
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 处理 401 未授权错误
    if (error.response && error.response.status === 401) {
      // 清除本地存储中的令牌
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
      // 显示错误消息
      ElMessage.error('登录已过期，请重新登录')
      // 跳转到登录页面
      window.location.href = '/login'
    } else if (error.response && error.response.status === 403) {
      ElMessage.error('权限不足，无法访问该资源')
    } else if (error.response && error.response.status === 500) {
      ElMessage.error('服务器内部错误，请稍后重试')
    } else if (!error.response) {
      ElMessage.error('网络错误，请检查网络连接')
    }
    return Promise.reject(error)
  }
)

export default apiClient
