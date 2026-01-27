<template>
  <div class="register-container">
    <div class="register-wrapper">
      <!-- 左侧图片区域 -->
      <div class="register-image-section">
        <img 
          src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=modern%20technology%20background%20with%20green%20elements%2C%20innovative%20business%20concept%2C%20clean%20design%2C%20high%20quality&image_size=landscape_16_9" 
          alt="注册背景" 
          class="register-image"
        />
        <div class="image-overlay">
          <div class="overlay-content">
            <h2>创建账号</h2>
            <p>注册新账号，开始使用低代码表单平台</p>
          </div>
        </div>
      </div>
      
      <!-- 右侧注册表单区域 -->
      <div class="register-form-section">
        <div class="form-container">
          <div class="form-header">
            <h1>账号注册</h1>
            <p>请填写以下信息创建新账号</p>
          </div>
          
          <el-form 
            :model="registerForm" 
            :rules="rules" 
            ref="registerFormRef" 
            class="register-form"
          >
            <el-form-item prop="username">
              <el-input 
                v-model="registerForm.username" 
                placeholder="请输入用户名" 
                prefix-icon="User" 
                size="large"
                :class="{ 'is-focused': isFocused('username') }"
                @focus="setFocus('username')"
                @blur="removeFocus('username')"
              />
            </el-form-item>
            

            
            <el-form-item prop="password">
              <el-input 
                v-model="registerForm.password" 
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
            
            <el-form-item prop="confirmPassword">
              <el-input 
                v-model="registerForm.confirmPassword" 
                type="password" 
                placeholder="请确认密码" 
                prefix-icon="Lock" 
                show-password 
                size="large"
                :class="{ 'is-focused': isFocused('confirmPassword') }"
                @focus="setFocus('confirmPassword')"
                @blur="removeFocus('confirmPassword')"
              />
            </el-form-item>
            

            
            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                class="register-button" 
                @click="handleRegister"
                :loading="loading"
                :disabled="loading"
              >
                {{ loading ? '注册中...' : '注册' }}
              </el-button>
            </el-form-item>
            
            <div class="form-footer">
              <p>已有账号？ <el-button type="text" @click="handleLogin">立即登录</el-button></p>
            </div>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { userApi } from '../api/userService'
import {
  User,
  Message,
  Lock,
  Avatar
} from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 150, message: '用户名长度应在3-150个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (value !== registerForm.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ]
}

const registerFormRef = ref(null)
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

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    // 调用注册API
    const response = await userApi.register({
      username: registerForm.value.username,
      password: registerForm.value.password,
      password2: registerForm.value.confirmPassword
    })
    
    ElMessage.success('注册成功，请登录')
    // 跳转到登录页面
    router.push('/login')
  } catch (error) {
    console.error('注册失败', error)
    // 提取具体的错误信息
    let errorMessage = '注册失败，请检查输入信息'
    if (error.response && error.response.data) {
      const data = error.response.data
      console.log('后端返回的错误数据:', data)
      if (typeof data === 'string') {
        errorMessage = data
      } else if (data.detail) {
        errorMessage = data.detail
      } else {
        // 处理所有字段的错误信息
        const errorMessages = []
        for (const [field, errors] of Object.entries(data)) {
          if (Array.isArray(errors)) {
            errorMessages.push(...errors)
          } else {
            errorMessages.push(errors)
          }
        }
        if (errorMessages.length > 0) {
          errorMessage = errorMessages.join('\n')
        }
      }
    } else if (error.message) {
      errorMessage = error.message
    }
    console.log('最终的错误信息:', errorMessage)
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}

// 处理登录
const handleLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
/* 注册容器 */
.register-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* 注册包装器 */
.register-wrapper {
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
.register-image-section {
  flex: 1;
  position: relative;
  overflow: hidden;
  min-width: 500px;
}

.register-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.register-image-section:hover .register-image {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(45, 200, 150, 0.8) 0%, rgba(75, 200, 135, 0.6) 100%);
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

/* 右侧注册表单区域 */
.register-form-section {
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

/* 注册表单 */
.register-form {
  margin-bottom: 30px;
}

.register-form .el-form-item {
  margin-bottom: 20px;
}

.register-form .el-input {
  height: 50px;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.register-form .el-input.is-focused {
  box-shadow: 0 0 0 2px rgba(45, 200, 150, 0.2);
}

/* 注册按钮 */
.register-button {
  width: 100%;
  height: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #2dca96 0%, #4bca87 100%);
  border: none;
  transition: all 0.3s ease;
}

.register-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(45, 200, 150, 0.4);
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

/* 响应式设计 */
@media (max-width: 992px) {
  .register-wrapper {
    flex-direction: column;
    max-width: 600px;
    min-height: auto;
  }
  
  .register-image-section {
    flex: none;
    height: 300px;
    min-width: auto;
  }
  
  .register-form-section {
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
  .register-container {
    padding: 10px;
  }
  
  .register-wrapper {
    border-radius: 12px;
  }
  
  .register-image-section {
    height: 250px;
  }
  
  .register-form-section {
    padding: 30px 20px;
  }
  
  .form-header h1 {
    font-size: 1.8rem;
  }
  
  .overlay-content h2 {
    font-size: 1.8rem;
  }
  
  .register-form .el-form-item {
    margin-bottom: 16px;
  }
  
  .register-form .el-input {
    height: 45px;
  }
  
  .register-button {
    height: 45px;
  }
}
</style>
