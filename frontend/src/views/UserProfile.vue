<template>
  <div class="user-profile-container">
    <div class="profile-header">
      <h2>个人中心</h2>
      <p>管理您的个人信息和账户设置</p>
    </div>
    
    <div class="profile-content">
      <!-- 用户信息卡片 -->
      <el-card class="profile-card">
        <template #header>
          <div class="card-header">
            <span>个人信息</span>
          </div>
        </template>
        
        <div class="profile-info">
          <div class="info-item">
            <label>用户名</label>
            <span>{{ userInfo.username }}</span>
          </div>
          <div class="info-item">
            <label>邮箱</label>
            <span>{{ userInfo.email || '未设置' }}</span>
          </div>
          <div class="info-item">
            <label>姓名</label>
            <span>{{ userInfo.firstName || '未设置' }} {{ userInfo.lastName || '' }}</span>
          </div>
        </div>
      </el-card>
      
      <!-- 修改密码卡片 -->
      <el-card class="profile-card">
        <template #header>
          <div class="card-header">
            <span>修改密码</span>
          </div>
        </template>
        
        <el-form 
          :model="passwordForm" 
          :rules="passwordRules" 
          ref="passwordFormRef" 
          class="password-form"
        >
          <el-form-item prop="oldPassword">
            <el-input 
              v-model="passwordForm.oldPassword" 
              type="password" 
              placeholder="请输入原密码" 
              prefix-icon="Lock" 
              size="large"
            />
          </el-form-item>
          
          <el-form-item prop="newPassword">
            <el-input 
              v-model="passwordForm.newPassword" 
              type="password" 
              placeholder="请输入新密码" 
              prefix-icon="Lock" 
              show-password 
              size="large"
            />
          </el-form-item>
          
          <el-form-item prop="confirmPassword">
            <el-input 
              v-model="passwordForm.confirmPassword" 
              type="password" 
              placeholder="请确认新密码" 
              prefix-icon="Lock" 
              show-password 
              size="large"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              size="large" 
              class="change-password-button" 
              @click="handleChangePassword"
              :loading="passwordLoading"
              :disabled="passwordLoading"
            >
              {{ passwordLoading ? '修改中...' : '修改密码' }}
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { userApi } from '../api/userService'
import {
  Lock
} from '@element-plus/icons-vue'

// 用户信息
const userInfo = ref({
  username: '',
  email: '',
  firstName: '',
  lastName: ''
})

// 密码表单
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ]
}

const passwordFormRef = ref(null)
const passwordLoading = ref(false)

// 获取用户信息
const getUserInfo = async () => {
  try {
    const response = await userApi.getProfile()
    userInfo.value = {
      username: response.username,
      email: response.email,
      firstName: response.first_name,
      lastName: response.last_name
    }
  } catch (error) {
    console.error('获取用户信息失败', error)
    ElMessage.error('获取用户信息失败')
  }
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  try {
    await passwordFormRef.value.validate()
    passwordLoading.value = true
    
    // 调用修改密码API
    await userApi.changePassword({
      old_password: passwordForm.value.oldPassword,
      new_password: passwordForm.value.newPassword
    })
    
    ElMessage.success('密码修改成功')
    // 重置表单
    passwordForm.value = {
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
    passwordFormRef.value.resetFields()
  } catch (error) {
    console.error('修改密码失败', error)
    ElMessage.error('修改密码失败，请检查输入信息')
  } finally {
    passwordLoading.value = false
  }
}

// 页面加载时获取用户信息
onMounted(() => {
  getUserInfo()
})
</script>

<style scoped>
/* 个人中心容器 */
.user-profile-container {
  padding: 20px;
  min-height: 80vh;
  background-color: #f5f7fa;
}

/* 个人中心头部 */
.profile-header {
  margin-bottom: 30px;
  text-align: center;
}

.profile-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #303133;
  margin-bottom: 10px;
}

.profile-header p {
  font-size: 1rem;
  color: #606266;
}

/* 个人中心内容 */
.profile-content {
  max-width: 800px;
  margin: 0 auto;
}

/* 卡片样式 */
.profile-card {
  margin-bottom: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: none;
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 1.1rem;
  font-weight: 600;
  color: #303133;
}

/* 个人信息样式 */
.profile-info {
  padding: 20px 0;
}

.info-item {
  display: flex;
  margin-bottom: 20px;
  align-items: center;
}

.info-item label {
  width: 100px;
  font-size: 1rem;
  color: #606266;
  font-weight: 500;
}

.info-item span {
  flex: 1;
  font-size: 1rem;
  color: #303133;
}

/* 密码表单样式 */
.password-form {
  padding: 20px 0;
}

.password-form .el-form-item {
  margin-bottom: 20px;
}

.password-form .el-input {
  height: 50px;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.password-form .el-input.is-focused {
  box-shadow: 0 0 0 2px rgba(45, 100, 255, 0.2);
}

/* 修改密码按钮 */
.change-password-button {
  width: 100%;
  height: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #2d64ff 0%, #4b87ff 100%);
  border: none;
  transition: all 0.3s ease;
}

.change-password-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(45, 100, 255, 0.4);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-profile-container {
    padding: 10px;
  }
  
  .profile-header h2 {
    font-size: 1.8rem;
  }
  
  .profile-content {
    padding: 0 10px;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .info-item label {
    width: 100%;
    margin-bottom: 5px;
  }
  
  .password-form .el-input {
    height: 45px;
  }
  
  .change-password-button {
    height: 45px;
  }
}
</style>