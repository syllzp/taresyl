<template>
  <div class="permission-list">
    <!-- 操作栏 -->
    <div class="permission-actions">
      <el-input
        v-model="searchQuery"
        placeholder="搜索权限名称或代码"
        prefix-icon="Search"
        class="search-input"
        @keyup.enter="getPermissions"
      />
      <el-button
        type="primary"
        size="large"
        @click="openCreateDialog"
        class="create-button"
      >
        <el-icon><Plus /></el-icon>
        创建权限
      </el-button>
    </div>

    <!-- 权限列表 -->
    <el-card class="permission-list-card">
      <template #header>
        <div class="card-header">
          <span>权限列表</span>
          <span class="permission-count">共 {{ totalPermissions }} 个权限</span>
        </div>
      </template>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="permissions.length === 0" class="empty-container">
        <el-empty description="暂无权限数据" />
      </div>

      <el-table
        v-else
        :data="permissions"
        style="width: 100%"
        border
        stripe
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="codename" label="权限代码" min-width="150" />
        <el-table-column prop="name" label="权限名称" min-width="150" />
        <el-table-column prop="type" label="权限类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getPermissionTypeTagType(row.type)">
              {{ getPermissionTypeName(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="权限描述" min-width="300" />
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
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div v-if="totalPermissions > 0" class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalPermissions"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 创建权限对话框 -->
    <el-dialog
      v-model="createDialogVisible"
      title="创建权限"
      width="600px"
    >
      <el-form
        :model="permissionForm"
        :rules="permissionRules"
        ref="permissionFormRef"
        label-width="100px"
      >
        <el-form-item label="权限代码" prop="codename">
          <el-input
            v-model="permissionForm.codename"
            placeholder="请输入权限代码（英文小写，下划线分隔）"
            size="large"
          />
        </el-form-item>
        <el-form-item label="权限名称" prop="name">
          <el-input
            v-model="permissionForm.name"
            placeholder="请输入权限名称"
            size="large"
          />
        </el-form-item>
        <el-form-item label="权限类型" prop="type">
          <el-select
            v-model="permissionForm.type"
            placeholder="请选择权限类型"
            size="large"
          >
            <el-option
              v-for="type in permissionTypes"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="权限描述" prop="description">
          <el-input
            v-model="permissionForm.description"
            type="textarea"
            placeholder="请输入权限描述"
            rows="3"
            size="large"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createPermission">创建</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑权限对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑权限"
      width="600px"
    >
      <el-form
        :model="permissionForm"
        :rules="permissionRules"
        ref="permissionFormRef"
        label-width="100px"
      >
        <el-form-item label="权限代码" prop="codename">
          <el-input
            v-model="permissionForm.codename"
            placeholder="请输入权限代码（英文小写，下划线分隔）"
            size="large"
            :disabled="true"
          />
          <div class="form-tip">权限代码一旦创建，不可修改</div>
        </el-form-item>
        <el-form-item label="权限名称" prop="name">
          <el-input
            v-model="permissionForm.name"
            placeholder="请输入权限名称"
            size="large"
          />
        </el-form-item>
        <el-form-item label="权限类型" prop="type">
          <el-select
            v-model="permissionForm.type"
            placeholder="请选择权限类型"
            size="large"
          >
            <el-option
              v-for="type in permissionTypes"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="权限描述" prop="description">
          <el-input
            v-model="permissionForm.description"
            type="textarea"
            placeholder="请输入权限描述"
            rows="3"
            size="large"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updatePermission">保存</el-button>
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
      <p>确定要删除权限 <span class="permission-name">{{ selectedPermission?.name }}</span> 吗？</p>
      <p class="delete-warning">删除后将无法恢复，且会影响所有拥有该权限的角色。</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="deletePermission">删除</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Search, Edit, Delete } from '@element-plus/icons-vue'
import apiClient from '../../api/axiosConfig'

// 响应式数据
const permissions = ref([])
const loading = ref(false)
const totalPermissions = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')

// 对话框状态
const createDialogVisible = ref(false)
const editDialogVisible = ref(false)
const deleteDialogVisible = ref(false)

// 表单数据
const permissionForm = reactive({
  id: null,
  codename: '',
  name: '',
  type: 'model',
  description: ''
})

// 权限类型选项
const permissionTypes = [
  { value: 'model', label: '模型权限' },
  { value: 'object', label: '对象权限' },
  { value: 'menu', label: '菜单权限' },
  { value: 'api', label: 'API权限' }
]

// 表单规则
const permissionRules = {
  codename: [
    { required: true, message: '请输入权限代码', trigger: 'blur' },
    { pattern: /^[a-z_]+$/, message: '权限代码只能包含小写字母和下划线', trigger: 'blur' },
    { min: 3, max: 100, message: '权限代码长度应在 3-100 个字符之间', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入权限名称', trigger: 'blur' },
    { min: 2, max: 100, message: '权限名称长度应在 2-100 个字符之间', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择权限类型', trigger: 'change' }
  ],
  description: [
    { max: 200, message: '权限描述长度不能超过 200 个字符', trigger: 'blur' }
  ]
}

// 表单引用
const permissionFormRef = ref(null)

// 选中的权限
const selectedPermission = ref(null)

// 获取权限类型的标签类型
const getPermissionTypeTagType = (type) => {
  const typeMap = {
    'model': 'primary',
    'object': 'success',
    'menu': 'warning',
    'api': 'info'
  }
  return typeMap[type] || 'default'
}

// 获取权限类型的中文名称
const getPermissionTypeName = (type) => {
  const typeMap = {
    'model': '模型权限',
    'object': '对象权限',
    'menu': '菜单权限',
    'api': 'API权限'
  }
  return typeMap[type] || type
}

// 获取权限列表
const getPermissions = async () => {
  loading.value = true
  try {
    const response = await apiClient.get('/api/auth/permissions/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        search: searchQuery.value
      }
    })
    permissions.value = response.data.results || response.data
    totalPermissions.value = response.data.count || permissions.value.length
  } catch (error) {
    console.error('获取权限列表失败', error)
    ElMessage.error('获取权限列表失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 打开创建对话框
const openCreateDialog = () => {
  // 重置表单
  permissionForm.id = null
  permissionForm.codename = ''
  permissionForm.name = ''
  permissionForm.type = 'model'
  permissionForm.description = ''
  if (permissionFormRef.value) {
    permissionFormRef.value.resetFields()
  }
  createDialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (permission) => {
  // 填充表单数据
  permissionForm.id = permission.id
  permissionForm.codename = permission.codename
  permissionForm.name = permission.name
  permissionForm.type = permission.type
  permissionForm.description = permission.description
  editDialogVisible.value = true
}

// 确认删除
const confirmDelete = (permission) => {
  selectedPermission.value = permission
  deleteDialogVisible.value = true
}

// 创建权限
const createPermission = async () => {
  if (!permissionFormRef.value) return
  
  try {
    await permissionFormRef.value.validate()
    
    const response = await apiClient.post('/api/auth/permissions/', {
      codename: permissionForm.codename,
      name: permissionForm.name,
      type: permissionForm.type,
      description: permissionForm.description
    })
    
    ElMessage.success('权限创建成功')
    createDialogVisible.value = false
    getPermissions()
  } catch (error) {
    console.error('创建权限失败', error)
    if (error.response && error.response.status === 400) {
      ElMessage.error('权限代码已存在，请使用其他代码')
    } else {
      ElMessage.error('创建权限失败，请稍后重试')
    }
  }
}

// 更新权限
const updatePermission = async () => {
  if (!permissionFormRef.value) return
  
  try {
    await permissionFormRef.value.validate()
    
    const response = await apiClient.put(`/api/auth/permissions/${permissionForm.id}/`, {
      name: permissionForm.name,
      type: permissionForm.type,
      description: permissionForm.description
    })
    
    ElMessage.success('权限更新成功')
    editDialogVisible.value = false
    getPermissions()
  } catch (error) {
    console.error('更新权限失败', error)
    ElMessage.error('更新权限失败，请稍后重试')
  }
}

// 删除权限
const deletePermission = async () => {
  if (!selectedPermission.value) return
  
  try {
    await apiClient.delete(`/api/auth/permissions/${selectedPermission.value.id}/`)
    ElMessage.success('权限删除成功')
    deleteDialogVisible.value = false
    getPermissions()
  } catch (error) {
    console.error('删除权限失败', error)
    ElMessage.error('删除权限失败，请稍后重试')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  getPermissions()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getPermissions()
}

// 页面加载时获取权限列表
onMounted(() => {
  getPermissions()
})
</script>

<style scoped>
.permission-list {
  padding: 20px 0;
}

.permission-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  width: 350px;
}

.create-button {
  min-width: 150px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.permission-count {
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

.permission-name {
  font-weight: 600;
  color: #409eff;
}

.delete-warning {
  color: #f56c6c;
  font-size: 0.9rem;
  margin-top: 10px;
}

.form-tip {
  font-size: 0.8rem;
  color: #909399;
  margin-top: 5px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .permission-actions {
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
