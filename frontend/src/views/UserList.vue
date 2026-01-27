<template>
  <div class="user-list-container">
    <div class="content-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>系统设置</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="content-actions">
        <el-button type="primary" @click="handleAddUser">
          <el-icon><Plus /></el-icon>
          新增用户
        </el-button>
        <el-button size="small" @click="refreshUsers">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 筛选区 -->
    <div class="filter-section">
      <el-form :inline="true" size="small">
        <el-form-item label="用户名">
          <el-input v-model="filterForm.username" placeholder="请输入用户名" style="width: 200px" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="filterForm.email" placeholder="请输入邮箱" style="width: 200px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetFilter">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 用户列表 -->
    <div class="user-list-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>用户列表</span>
            <span class="user-count">共 {{ total }} 名用户</span>
          </div>
        </template>
        <el-table :data="userList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" min-width="150" />
          <el-table-column prop="email" label="邮箱" min-width="200" />
          <el-table-column prop="first_name" label="姓名" min-width="100" />
          <el-table-column prop="last_name" label="姓氏" min-width="100" />
          <el-table-column prop="date_joined" label="创建时间" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.date_joined) }}
            </template>
          </el-table-column>
          <el-table-column prop="last_login" label="最后登录" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.last_login) }}
            </template>
          </el-table-column>
          <el-table-column label="角色" min-width="150">
            <template #default="scope">
              <div v-if="userRolesMap[scope.row.id] && userRolesMap[scope.row.id].length > 0">
                <el-tag
                  v-for="role in userRolesMap[scope.row.id]"
                  :key="role.id"
                  type="primary"
                  effect="light"
                  class="role-tag"
                >
                  {{ role.name }}
                </el-tag>
              </div>
              <div v-else class="no-role">
                无
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="handleEditUser(scope.row)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="handleDeleteUser(scope.row.id)">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 用户编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form :model="userForm" :rules="rules" ref="userFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" type="email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="姓名" prop="first_name">
          <el-input v-model="userForm.first_name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="姓氏" prop="last_name">
          <el-input v-model="userForm.last_name" placeholder="请输入姓氏" />
        </el-form-item>
        <el-form-item label="密码" v-if="!isEditing">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { userApi } from '../api/userService'
import apiClient from '../api/axiosConfig'
import {
  Plus,
  Refresh,
  Search,
  Edit,
  Delete
} from '@element-plus/icons-vue'

// 响应式数据
const userList = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const filterForm = ref({
  username: '',
  email: ''
})
const dialogVisible = ref(false)
const dialogTitle = ref('新增用户')
const isEditing = ref(false)
const userForm = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: ''
})
const userFormRef = ref(null)
const userRolesMap = ref({})
const loadingRoles = ref(false)

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 150, message: '用户名长度应在3-150个字符之间', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  first_name: [
    { max: 30, message: '姓名长度不能超过30个字符', trigger: 'blur' }
  ],
  last_name: [
    { max: 150, message: '姓氏长度不能超过150个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

// 格式化时间
const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

// 获取用户角色映射
const fetchUserRoles = async () => {
  loadingRoles.value = true
  try {
    console.log('开始获取用户角色...')
    const response = await apiClient.get('/api/auth/user-roles/')
    const userRoles = response.data.results || response.data
    console.log('用户角色数据:', userRoles)
    
    // 构建用户角色映射
    const rolesMap = {}
    
    // 先获取所有角色信息
    const rolesResponse = await apiClient.get('/api/auth/roles/')
    const allRoles = rolesResponse.data.results || rolesResponse.data
    console.log('所有角色数据:', allRoles)
    const roleMap = {}
    allRoles.forEach(role => {
      roleMap[role.id] = role
    })
    console.log('角色映射:', roleMap)
    
    // 构建用户角色映射
    userRoles.forEach(ur => {
      console.log('处理用户角色:', ur)
      // 检查ur.user和ur.role的结构
      let userId, roleId
      
      if (typeof ur.user === 'object' && ur.user.id) {
        userId = ur.user.id
      } else if (typeof ur.user === 'number') {
        userId = ur.user
      } else {
        console.error('无效的用户ID:', ur.user)
        return
      }
      
      if (typeof ur.role === 'object' && ur.role.id) {
        roleId = ur.role.id
      } else if (typeof ur.role === 'number') {
        roleId = ur.role
      } else {
        console.error('无效的角色ID:', ur.role)
        return
      }
      
      console.log('用户ID:', userId, '角色ID:', roleId)
      
      if (!rolesMap[userId]) {
        rolesMap[userId] = []
      }
      
      if (roleMap[roleId]) {
        rolesMap[userId].push(roleMap[roleId])
        console.log('添加角色到用户:', roleMap[roleId].name, '->', userId)
      }
    })
    
    console.log('最终用户角色映射:', rolesMap)
    userRolesMap.value = rolesMap
  } catch (error) {
    console.error('获取用户角色失败', error)
    userRolesMap.value = {}
  } finally {
    loadingRoles.value = false
  }
}

// 刷新用户列表
const refreshUsers = () => {
  fetchUsers()
}

// 搜索用户
const handleSearch = () => {
  currentPage.value = 1
  fetchUsers()
}

// 重置筛选条件
const resetFilter = () => {
  filterForm.value = {
    username: '',
    email: ''
  }
  currentPage.value = 1
  fetchUsers()
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchUsers()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchUsers()
}

// 获取用户列表
const fetchUsers = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    // 添加筛选条件
    if (filterForm.value.username) {
      params.username = filterForm.value.username
    }
    if (filterForm.value.email) {
      params.email = filterForm.value.email
    }
    
    const data = await userApi.getAll(params)
    userList.value = data.results || data
    total.value = data.count || data.length
    
    // 获取用户角色信息
    await fetchUserRoles()
  } catch (error) {
    console.error('获取用户列表失败', error)
    ElMessage.error('获取用户列表失败')
  }
}

// 新增用户
const handleAddUser = () => {
  dialogTitle.value = '新增用户'
  isEditing.value = false
  userForm.value = {
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: ''
  }
  dialogVisible.value = true
}

// 编辑用户
const handleEditUser = (user) => {
  dialogTitle.value = '编辑用户'
  isEditing.value = true
  userForm.value = {
    id: user.id,
    username: user.username,
    email: user.email,
    first_name: user.first_name,
    last_name: user.last_name
  }
  dialogVisible.value = true
}

// 删除用户
const handleDeleteUser = (id) => {
  ElMessageBox.confirm('确定要删除该用户吗？此操作不可恢复。', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await userApi.delete(id)
      ElMessage.success('用户删除成功')
      fetchUsers()
    } catch (error) {
      console.error('删除用户失败', error)
      ElMessage.error('删除用户失败')
    }
  }).catch(() => {
    // 取消操作
  })
}

// 提交表单
const handleSubmit = async () => {
  if (!userFormRef.value) return
  
  try {
    await userFormRef.value.validate()
    
    if (isEditing.value) {
      // 更新用户
      await userApi.update(userForm.value.id, userForm.value)
      ElMessage.success('用户更新成功')
    } else {
      // 创建用户
      await userApi.create(userForm.value)
      ElMessage.success('用户创建成功')
    }
    
    dialogVisible.value = false
    fetchUsers()
  } catch (error) {
    console.error('提交表单失败', error)
    ElMessage.error('提交表单失败')
  }
}

// 初始化
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
/* 内容头部 */
.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.content-actions {
  display: flex;
  gap: 10px;
}

/* 筛选区 */
.filter-section {
  background-color: #fff;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
}

/* 用户列表区 */
.user-list-section {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-count {
  font-size: 14px;
  color: #606266;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 对话框 */
.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.role-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.no-role {
  color: #909399;
  font-style: italic;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .filter-section {
    padding: 10px;
  }
  
  .user-list-section {
    margin-bottom: 10px;
  }
  
  .pagination {
    margin-top: 10px;
  }
}
</style>
