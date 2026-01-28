<template>
  <div class="login-container">
    <div class="login-wrapper">
      <!-- 左侧图片区域 -->
      <div class="login-image-section">
        <img 
          src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=modern%20office%20space%20with%20blue%20technology%20elements%2C%20professional%20business%20environment%2C%20clean%20design%2C%20high%20quality&image_size=landscape_16_9" 
          alt="登录背景" 
          class="login-image"
        />
        <div class="image-overlay">
          <div class="overlay-content">
            <h2>欢迎回来</h2>
            <p>登录您的账户，开始使用低代码表单平台</p>
          </div>
        </div>
      </div>
      
      <!-- 右侧登录表单区域 -->
      <div class="login-form-section">
        <div class="form-container">
          <div class="form-header">
            <h1>账号登录</h1>
            <p>请输入您的账号信息进行登录</p>
          </div>
          
          <el-form 
            :model="loginForm" 
            :rules="rules" 
            ref="loginFormRef" 
            class="login-form"
          >
            <el-form-item prop="username">
              <el-input 
                v-model="loginForm.username" 
                placeholder="请输入用户名/邮箱" 
                prefix-icon="User" 
                size="large"
                :class="{ 'is-focused': isFocused('username') }"
                @focus="setFocus('username')"
                @blur="removeFocus('username')"
              />
            </el-form-item>
            
            <el-form-item prop="password">
              <el-input 
                v-model="loginForm.password" 
                type="password" 
                placeholder="请输入密码" 
                prefix-icon="Lock" 
                show-password 
                size="large"
                :class="{ 'is-focused': isFocused('password') }"
                @focus="setFocus('password')"
                @blur="removeFocus('password')"
              />
            </el-form-item>
            
            <div class="form-options">
              <el-checkbox v-model="loginForm.remember">记住密码</el-checkbox>
              <el-button type="text" @click="handleForgotPassword" class="forgot-password">忘记密码？</el-button>
            </div>
            
            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                class="login-button" 
                @click="handleLogin"
                :loading="loading"
                :disabled="loading"
              >
                {{ loading ? '登录中...' : '登录' }}
              </el-button>
            </el-form-item>
            
            <div class="form-footer">
              <p>还没有账号？ <el-button type="text" @click="handleRegister">立即注册</el-button></p>
            </div>
          </el-form>
          
          <!-- 第三方登录 -->
          <div class="third-party-login">
            <div class="divider">
              <span>其他登录方式</span>
            </div>
            <div class="third-party-icons">
              <el-button circle @click="handleThirdPartyLogin('wechat')">
                <el-icon><ChatLineRound /></el-icon>
              </el-button>
              <el-button circle @click="handleThirdPartyLogin('qq')">
                <el-icon><Message /></el-icon>
              </el-button>
              <el-button circle @click="handleThirdPartyLogin('github')">
                <el-icon><Link /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { userApi } from '../api/userService'
import permissionService from '../services/permissionService'
import {
  User,
  Lock,
  ChatLineRound,
  Message,
  Link
} from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const loginForm = ref({
  username: '',
  password: '',
  remember: false
})

// 页面加载时，从本地存储中读取保存的登录信息
onMounted(() => {
  const savedUsername = localStorage.getItem('savedUsername')
  const savedPassword = localStorage.getItem('savedPassword')
  const savedRemember = localStorage.getItem('savedRemember') === 'true'
  
  if (savedRemember && savedUsername && savedPassword) {
    loginForm.value.username = savedUsername
    loginForm.value.password = savedPassword
    loginForm.value.remember = savedRemember
  }
})

const rules = {
  username: [
    { required: true, message: '请输入用户名/邮箱', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

const loginFormRef = ref(null)
const loading = ref(false)
const focusedField = ref('')

// 检查字段是否聚焦
const isFocused = (field) => {
  return focusedField.value === field
}

// 设置字段聚焦
const setFocus = (field) => {
  focusedField.value = field
}

// 移除字段聚焦
const removeFocus = () => {
  focusedField.value = ''
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    // 调用登录API
    const response = await userApi.login({
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    
    // 保存登录状态和token
    localStorage.setItem('token', response.access)
    localStorage.setItem('refreshToken', response.refresh)
    localStorage.setItem('user', JSON.stringify({
      username: response.username,
      email: response.email
    }))
    
    // 根据是否勾选了记住密码来保存或清除登录信息
    if (loginForm.value.remember) {
      localStorage.setItem('savedUsername', loginForm.value.username)
      localStorage.setItem('savedPassword', loginForm.value.password)
      localStorage.setItem('savedRemember', 'true')
    } else {
      localStorage.removeItem('savedUsername')
      localStorage.removeItem('savedPassword')
      localStorage.removeItem('savedRemember')
    }
    
    // 加载用户权限
    await permissionService.getPermissions()
    console.log('用户权限加载完成')
    
    ElMessage.success('登录成功')
    // 跳转到首页
    router.push('/')
  } catch (error) {
    console.error('登录失败', error)
    ElMessage.error('登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}

// 处理注册
const handleRegister = () => {
  // 跳转到注册页面
  router.push('/register')
}

// 处理忘记密码
const handleForgotPassword = () => {
  ElMessage.info('忘记密码功能即将开放')
}

// 处理第三方登录
const handleThirdPartyLogin = (provider) => {
  ElMessage.info(`${provider}登录功能即将开放`)
}
</script>

<style scoped>
/* 登录容器 */
.login-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* 登录包装器 */
.login-wrapper {
  display: flex;
  width: 100%;
  max-width: 1200px;
  min-height: 700px;
  background-color: #fff;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 左侧图片区域 */
.login-image-section {
  flex: 1;
  position: relative;
  overflow: hidden;
  min-width: 500px;
}

.login-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.login-image-section:hover .login-image {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(45, 100, 255, 0.8) 0%, rgba(75, 135, 255, 0.6) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.overlay-content {
  text-align: center;
  color: #fff;
  padding: 0 40px;
}

.overlay-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.overlay-content p {
  font-size: 1.2rem;
  line-height: 1.6;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* 右侧登录表单区域 */
.login-form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  min-width: 400px;
}

.form-container {
  width: 100%;
  max-width: 400px;
}

.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.form-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #303133;
  margin-bottom: 10px;
}

.form-header p {
  font-size: 1rem;
  color: #606266;
}

/* 登录表单 */
.login-form {
  margin-bottom: 30px;
}

.login-form .el-form-item {
  margin-bottom: 24px;
}

.login-form .el-input {
  height: 50px;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.login-form .el-input.is-focused {
  box-shadow: 0 0 0 2px rgba(45, 100, 255, 0.2);
}

/* 表单选项 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.forgot-password {
  color: #409eff;
}

/* 登录按钮 */
.login-button {
  width: 100%;
  height: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #2d64ff 0%, #4b87ff 100%);
  border: none;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(45, 100, 255, 0.4);
}

/* 表单底部 */
.form-footer {
  text-align: center;
  margin-top: 20px;
  color: #606266;
}

.form-footer .el-button {
  color: #409eff;
  padding: 0;
}

/* 第三方登录 */
.third-party-login {
  margin-top: 40px;
}

.divider {
  position: relative;
  text-align: center;
  margin-bottom: 30px;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background-color: #e4e7ed;
  transform: translateY(-50%);
}

.divider span {
  position: relative;
  background-color: #fff;
  padding: 0 20px;
  color: #909399;
  font-size: 0.9rem;
}

.third-party-icons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.third-party-icons .el-button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid #dcdfe6;
  transition: all 0.3s ease;
}

.third-party-icons .el-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  color: #409eff;
  border-color: #409eff;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .login-wrapper {
    flex-direction: column;
    max-width: 600px;
    min-height: auto;
  }
  
  .login-image-section {
    flex: none;
    height: 300px;
    min-width: auto;
  }
  
  .login-form-section {
    flex: none;
    min-width: auto;
    padding: 40px 30px;
  }
  
  .overlay-content h2 {
    font-size: 2rem;
  }
  
  .overlay-content p {
    font-size: 1rem;
  }
}

@media (max-width: 576px) {
  .login-container {
    padding: 10px;
  }
  
  .login-wrapper {
    border-radius: 12px;
  }
  
  .login-image-section {
    height: 250px;
  }
  
  .login-form-section {
    padding: 30px 20px;
  }
  
  .form-header h1 {
    font-size: 1.8rem;
  }
  
  .overlay-content h2 {
    font-size: 1.8rem;
  }
  
  .login-form .el-form-item {
    margin-bottom: 20px;
  }
  
  .login-form .el-input {
    height: 45px;
  }
  
  .login-button {
    height: 45px;
  }
}
</style>
