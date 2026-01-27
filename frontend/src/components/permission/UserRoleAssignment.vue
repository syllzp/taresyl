<template>
  <div class="user-role-assignment">
    <!-- 操作栏 -->
    <div class="assignment-actions">
      <el-input
        v-model="searchQuery"
        placeholder="搜索用户姓名或用户名"
        prefix-icon="Search"
        class="search-input"
        @keyup.enter="getUsers"
      />
    </div>

    <!-- 用户列表 -->
    <el-card class="user-list-card">
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
          <span class="user-count">共 {{ totalUsers }} 个用户</span>
        </div>
      </template>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="users.length === 0" class="empty-container">
        <el-empty description="暂无用户数据" />
      </div>

      <el-table
        v-else
        :data="users"
        style="width: 100%"
        border
        stripe
        @row-click="selectUser"
        :row-class-name="({row}) => selectedUser?.id === row.id ? 'selected-row' : ''"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" min-width="150" />
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column prop="first_name" label="姓名" min-width="150">
          <template #default="{ row }">
            {{ row.first_name }} {{ row.last_name }}
          </template>
        </el-table-column>
        <el-table-column label="当前角色" min-width="200">
          <template #default="{ row }">
            <div v-if="getUserRoles(row.id).length > 0">
              <el-tag
                v-for="role in getUserRoles(row.id)"
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
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click.stop="openAssignDialog(row)"
              class="assign-button"
            >
              分配角色
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click.stop="openRemoveDialog(row)"
              class="remove-button"
              :disabled="getUserRoles(row.id).length === 0"
            >
              移除角色
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div v-if="totalUsers > 0" class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalUsers"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 分配角色对话框 -->
    <el-dialog
      v-model="assignDialogVisible"
      title="为用户分配角色"
      width="500px"
    >
      <div v-if="selectedUser">
        <div class="user-info">
          <span class="user-label">用户：</span>
          <span class="user-value">{{ selectedUser.username }}</span>
          <span class="user-email">({{ selectedUser.email }})</span>
        </div>
        
        <el-form
          :model="assignForm"
          :rules="assignRules"
          ref="assignFormRef"
          label-width="80px"
          class="assign-form"
        >
          <el-form-item label="选择角色" prop="roleId">
            <el-select
              v-model="assignForm.roleId"
              placeholder="请选择要分配的角色"
              size="large"
              class="role-select"
            >
              <el-option
                v-for="role in roles"
                :key="role.id"
                :label="role.name"
                :value="role.id"
                :disabled="isRoleAssigned(role.id)"
              />
            </el-select>
          </el-form-item>
        </el-form>
        
        <div v-if="getUserRoles(selectedUser.id).length > 0" class="current-roles">
          <span class="current-roles-label">当前角色：</span>
          <el-tag
            v-for="role in getUserRoles(selectedUser.id)"
            :key="role.id"
            type="primary"
            effect="light"
            class="current-role-tag"
          >
            {{ role.name }}
          </el-tag>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="assignDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="assignRole">分配</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 移除角色对话框 -->
    <el-dialog
      v-model="removeDialogVisible"
      title="移除用户角色"
      width="500px"
    >
      <div v-if="selectedUser">
        <div class="user-info">
          <span class="user-label">用户：</span>
          <span class="user-value">{{ selectedUser.username }}</span>
          <span class="user-email">({{ selectedUser.email }})</span>
        </div>
        
        <el-form
          :model="removeForm"
          :rules="removeRules"
          ref="removeFormRef"
          label-width="80px"
          class="remove-form"
        >
          <el-form-item label="选择角色" prop="roleId">
            <el-select
              v-model="removeForm.roleId"
              placeholder="请选择要移除的角色"
              size="large"
              class="role-select"
            >
              <el-option
                v-for="role in getUserRoles(selectedUser.id)"
                :key="role.id"
                :label="role.name"
                :value="role.id"
              />
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="removeDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="removeRole">移除</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Edit, Delete, Plus } from '@element-plus/icons-vue'
import apiClient from '../../api/axiosConfig'

// 响应式数据
const users = ref([])
const roles = ref([])
const userRoles = ref([])
const loading = ref(false)
const totalUsers = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')

// 选中的用户
const selectedUser = ref(null)

// 对话框状态
const assignDialogVisible = ref(false)
const removeDialogVisible = ref(false)

// 分配角色表单
const assignForm = reactive({
  roleId: null
})

// 移除角色表单
const removeForm = reactive({
  roleId: null
})

// 表单规则
const assignRules = {
  roleId: [
    { required: true, message: '请选择要分配的角色', trigger: 'change' }
  ]
}

const removeRules = {
  roleId: [
    { required: true, message: '请选择要移除的角色', trigger: 'change' }
  ]
}

// 表单引用
const assignFormRef = ref(null)
const removeFormRef = ref(null)

// 获取用户列表
const getUsers = async () => {
  loading.value = true
  try {
    const response = await apiClient.get('/api/auth/users/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        search: searchQuery.value
      }
    })
    users.value = response.data.results || response.data
    totalUsers.value = response.data.count || users.value.length
  } catch (error) {
    console.error('获取用户列表失败', error)
    ElMessage.error('获取用户列表失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 获取角色列表
const getRoles = async () => {
  try {
    const response = await apiClient.get('/api/auth/roles/')
    roles.value = response.data.results || response.data
  } catch (error) {
    console.error('获取角色列表失败', error)
    ElMessage.error('获取角色列表失败，请稍后重试')
  }
}

// 获取用户角色关联
const getUserRolesData = async () => {
  try {
    const response = await apiClient.get('/api/auth/user-roles/')
    userRoles.value = response.data.results || response.data
  } catch (error) {
    console.error('获取用户角色关联失败', error)
    ElMessage.error('获取用户角色关联失败，请稍后重试')
  }
}

// 获取用户的角色
const getUserRoles = (userId) => {
  const userRoleIds = userRoles.value
    .filter(ur => ur.user.id === userId)
    .map(ur => ur.role.id)
  
  return roles.value.filter(role => userRoleIds.includes(role.id))
}

// 检查角色是否已分配给用户
const isRoleAssigned = (roleId) => {
  if (!selectedUser) return false
  return userRoles.value.some(ur => ur.user.id === selectedUser.id && ur.role.id === roleId)
}

// 选择用户
const selectUser = (user) => {
  selectedUser.value = user
}

// 打开分配角色对话框
const openAssignDialog = (user) => {
  selectedUser.value = user
  assignForm.roleId = null
  assignDialogVisible.value = true
}

// 打开移除角色对话框
const openRemoveDialog = (user) => {
  selectedUser.value = user
  removeForm.roleId = null
  removeDialogVisible.value = true
}

// 分配角色
const assignRole = async () => {
  if (!assignFormRef.value || !selectedUser) return
  
  try {
    await assignFormRef.value.validate()
    
    const response = await apiClient.post('/api/auth/user-roles/', {
      user_id: selectedUser.id,
      role_id: assignForm.roleId
    })
    
    ElMessage.success('角色分配成功')
    assignDialogVisible.value = false
    getUserRolesData()
  } catch (error) {
    console.error('分配角色失败', error)
    if (error.response && error.response.status === 400) {
      ElMessage.error('该角色已分配给用户')
    } else {
      ElMessage.error('分配角色失败，请稍后重试')
    }
  }
}

// 移除角色
const removeRole = async () => {
  if (!removeFormRef.value || !selectedUser) return
  
  try {
    await removeFormRef.value.validate()
    
    // 找到对应的用户角色关联
    const userRole = userRoles.value.find(
      ur => ur.user.id === selectedUser.id && ur.role.id === removeForm.roleId
    )
    
    if (userRole) {
      await apiClient.delete(`/api/auth/user-roles/${userRole.id}/`)
      ElMessage.success('角色移除成功')
      removeDialogVisible.value = false
      getUserRolesData()
    } else {
      ElMessage.error('未找到对应的角色关联')
    }
  } catch (error) {
    console.error('移除角色失败', error)
    ElMessage.error('移除角色失败，请稍后重试')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  getUsers()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getUsers()
}

// 页面加载时获取数据
onMounted(async () => {
  await Promise.all([
    getUsers(),
    getRoles(),
    getUserRolesData()
  ])
})
</script>

<style scoped>
.user-role-assignment {
  padding: 20px 0;
}

.assignment-actions {
  margin-bottom: 20px;
}

.search-input {
  width: 350px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-count {
  font-size: 0.9rem;
  color: #606266;
}

.loading-container {
  padding: 20px 0;
}

.empty-container {
  padding: 40px 0;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.selected-row {
  background-color: #ecf5ff !important;
}

.role-tag {
  margin-right: 5px;
}

.no-role {
  color: #909399;
  font-style: italic;
}

.user-info {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.user-label {
  font-weight: 600;
  margin-right: 5px;
}

.user-value {
  font-weight: 600;
  color: #409eff;
  margin-right: 5px;
}

.user-email {
  color: #606266;
  font-size: 0.9rem;
}

.assign-form {
  margin-bottom: 20px;
}

.role-select {
  width: 100%;
}

.current-roles {
  margin-top: 20px;
}

.current-roles-label {
  font-weight: 600;
  margin-right: 10px;
}

.current-role-tag {
  margin-right: 5px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .search-input {
    width: 100%;
  }
}
</style>
