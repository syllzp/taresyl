<template>
  <div class="role-management">
    <!-- 操作栏 -->
    <div class="role-actions">
      <el-input
        v-model="searchQuery"
        placeholder="搜索角色名称"
        prefix-icon="Search"
        class="search-input"
        @keyup.enter="getRoles"
      />
      <el-button
        type="primary"
        size="large"
        @click="openCreateDialog"
        class="create-button"
      >
        <el-icon><Plus /></el-icon>
        创建角色
      </el-button>
    </div>

    <!-- 角色列表 -->
    <el-card class="role-list-card">
      <template #header>
        <div class="card-header">
          <span>角色列表</span>
          <span class="role-count">共 {{ totalRoles }} 个角色</span>
        </div>
      </template>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="roles.length === 0" class="empty-container">
        <el-empty description="暂无角色数据" />
      </div>

      <el-table
        v-else
        :data="roles"
        style="width: 100%"
        border
        stripe
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="角色名称" min-width="150">
          <template #default="{ row }">
            <span>
              {{ row.name }}
              <el-tag v-if="isBuiltinRole(row.name)" size="small" type="info" effect="dark" class="builtin-tag">
                内置
              </el-tag>
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="角色描述" min-width="300" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="openEditDialog(row)"
              class="edit-button"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="confirmDelete(row)"
              class="delete-button"
              :disabled="isBuiltinRole(row.name)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div v-if="totalRoles > 0" class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalRoles"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 创建角色对话框 -->
    <el-dialog
      v-model="createDialogVisible"
      title="创建角色"
      width="500px"
    >
      <el-form
        :model="roleForm"
        :rules="roleRules"
        ref="roleFormRef"
        label-width="80px"
      >
        <el-form-item label="角色名称" prop="name">
          <el-input
            v-model="roleForm.name"
            placeholder="请输入角色名称"
            size="large"
          />
        </el-form-item>
        <el-form-item label="角色描述" prop="description">
          <el-input
            v-model="roleForm.description"
            type="textarea"
            placeholder="请输入角色描述"
            rows="3"
            size="large"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createRole">创建</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑角色对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑角色"
      width="500px"
    >
      <el-form
        :model="roleForm"
        :rules="roleRules"
        ref="roleFormRef"
        label-width="80px"
      >
        <el-form-item label="角色名称" prop="name">
          <el-input
            v-model="roleForm.name"
            placeholder="请输入角色名称"
            size="large"
          />
        </el-form-item>
        <el-form-item label="角色描述" prop="description">
          <el-input
            v-model="roleForm.description"
            type="textarea"
            placeholder="请输入角色描述"
            rows="3"
            size="large"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updateRole">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="400px"
      :close-on-click-modal="false"
    >
      <p>确定要删除角色 <span class="role-name">{{ selectedRole?.name }}</span> 吗？</p>
      <p class="delete-warning">删除后将无法恢复，且会影响所有拥有该角色的用户。</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="deleteRole">删除</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Edit, Delete, Warning } from '@element-plus/icons-vue'
import apiClient from '../../api/axiosConfig'

// 响应式数据
const roles = ref([])
const loading = ref(false)
const totalRoles = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')

// 对话框状态
const createDialogVisible = ref(false)
const editDialogVisible = ref(false)
const deleteDialogVisible = ref(false)

// 表单数据
const roleForm = reactive({
  id: null,
  name: '',
  description: ''
})

// 表单规则
const roleRules = {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 2, max: 50, message: '角色名称长度应在 2-50 个字符之间', trigger: 'blur' }
  ],
  description: [
    { max: 200, message: '角色描述长度不能超过 200 个字符', trigger: 'blur' }
  ]
}

// 表单引用
const roleFormRef = ref(null)

// 选中的角色
const selectedRole = ref(null)

// 检查角色是否为内置角色
const isBuiltinRole = (roleName) => {
  return ['Admin', 'User'].includes(roleName)
}

// 获取角色列表
const getRoles = async () => {
  loading.value = true
  try {
    const response = await apiClient.get('/api/auth/roles/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        search: searchQuery.value
      }
    })
    roles.value = response.data.results || response.data
    totalRoles.value = response.data.count || roles.value.length
  } catch (error) {
    console.error('获取角色列表失败', error)
    ElMessage.error('获取角色列表失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 打开创建对话框
const openCreateDialog = () => {
  // 重置表单
  roleForm.id = null
  roleForm.name = ''
  roleForm.description = ''
  if (roleFormRef.value) {
    roleFormRef.value.resetFields()
  }
  createDialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (role) => {
  // 填充表单数据
  roleForm.id = role.id
  roleForm.name = role.name
  roleForm.description = role.description
  editDialogVisible.value = true
}

// 确认删除
const confirmDelete = (role) => {
  selectedRole.value = role
  deleteDialogVisible.value = true
}

// 创建角色
const createRole = async () => {
  if (!roleFormRef.value) return
  
  try {
    await roleFormRef.value.validate()
    
    const response = await apiClient.post('/api/auth/roles/', {
      name: roleForm.name,
      description: roleForm.description
    })
    
    ElMessage.success('角色创建成功')
    createDialogVisible.value = false
    getRoles()
  } catch (error) {
    console.error('创建角色失败', error)
    if (error.response && error.response.status === 400) {
      ElMessage.error('角色名称已存在，请使用其他名称')
    } else {
      ElMessage.error('创建角色失败，请稍后重试')
    }
  }
}

// 更新角色
const updateRole = async () => {
  if (!roleFormRef.value) return
  
  try {
    await roleFormRef.value.validate()
    
    const response = await apiClient.put(`/api/auth/roles/${roleForm.id}/`, {
      name: roleForm.name,
      description: roleForm.description
    })
    
    ElMessage.success('角色更新成功')
    editDialogVisible.value = false
    getRoles()
  } catch (error) {
    console.error('更新角色失败', error)
    if (error.response && error.response.status === 400) {
      ElMessage.error('角色名称已存在，请使用其他名称')
    } else {
      ElMessage.error('更新角色失败，请稍后重试')
    }
  }
}

// 删除角色
const deleteRole = async () => {
  if (!selectedRole.value) return
  
  try {
    await apiClient.delete(`/api/auth/roles/${selectedRole.value.id}/`)
    ElMessage.success('角色删除成功')
    deleteDialogVisible.value = false
    getRoles()
  } catch (error) {
    console.error('删除角色失败', error)
    ElMessage.error('删除角色失败，请稍后重试')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  getRoles()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getRoles()
}

// 页面加载时获取角色列表
onMounted(() => {
  getRoles()
})
</script>

<style scoped>
.role-management {
  padding: 20px 0;
}

.role-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.create-button {
  min-width: 150px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.role-count {
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

.role-name {
  font-weight: 600;
  color: #409eff;
}

.delete-warning {
  color: #f56c6c;
  font-size: 0.9rem;
  margin-top: 10px;
}

.builtin-tag {
  margin-left: 8px;
  font-size: 0.7rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .role-actions {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .search-input {
    width: 100%;
  }
  
  .create-button {
    width: 100%;
  }
}
</style>
