<template>
  <div class="role-permission-assignment">
    <!-- 操作栏 -->
    <div class="assignment-actions">
      <el-input
        v-model="searchQuery"
        placeholder="搜索角色名称"
        prefix-icon="Search"
        class="search-input"
        @keyup.enter="getRoles"
      />
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
        @row-click="selectRole"
        :row-class-name="({row}) => selectedRole?.id === row.id ? 'selected-row' : ''"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="角色名称" min-width="150" />
        <el-table-column prop="description" label="角色描述" min-width="300" />
        <el-table-column label="当前权限数" width="120">
          <template #default="{ row }">
            <span class="permission-count">{{ getRolePermissions(row.id).length }}</span>
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
              分配权限
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click.stop="openRemoveDialog(row)"
              class="remove-button"
              :disabled="getRolePermissions(row.id).length === 0"
            >
              移除权限
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

    <!-- 分配权限对话框 -->
    <el-dialog
      v-model="assignDialogVisible"
      title="为角色分配权限"
      width="700px"
      :close-on-click-modal="false"
    >
      <div v-if="selectedRole">
        <div class="role-info">
          <span class="role-label">角色：</span>
          <span class="role-value">{{ selectedRole.name }}</span>
        </div>
        
        <div class="permission-filter">
          <el-input
            v-model="permissionSearch"
            placeholder="搜索权限名称或代码"
            prefix-icon="Search"
            class="permission-search"
            @keyup.enter="filterPermissions"
          />
          <el-select
            v-model="permissionTypeFilter"
            placeholder="按权限类型过滤"
            class="type-filter"
            @change="filterPermissions"
          >
            <el-option value="" label="全部类型" />
            <el-option value="model" label="模型权限" />
            <el-option value="object" label="对象权限" />
            <el-option value="menu" label="菜单权限" />
            <el-option value="api" label="API权限" />
          </el-select>
        </div>
        
        <div class="permission-list">
          <div class="permission-list-header">
            <span>权限列表</span>
            <span class="filtered-count">共 {{ filteredPermissions.length }} 个权限</span>
          </div>
          
          <el-checkbox-group v-model="selectedPermissionIds" class="permission-checkbox-group">
            <el-checkbox
              v-for="permission in filteredPermissions"
              :key="permission.id"
              :label="permission.id"
              :disabled="isPermissionAssigned(permission.id)"
              class="permission-checkbox"
            >
              <div class="permission-info">
                <div class="permission-name">{{ permission.name }}</div>
                <div class="permission-meta">
                  <span class="permission-codename">{{ permission.codename }}</span>
                  <el-tag
                    :type="getPermissionTypeTagType(permission.type)"
                    size="small"
                    class="permission-type-tag"
                  >
                    {{ getPermissionTypeName(permission.type) }}
                  </el-tag>
                </div>
                <div v-if="permission.description" class="permission-description">{{ permission.description }}</div>
              </div>
            </el-checkbox>
          </el-checkbox-group>
        </div>
        
        <div v-if="getRolePermissions(selectedRole.id).length > 0" class="current-permissions">
          <span class="current-permissions-label">当前权限：</span>
          <div class="current-permission-tags">
            <el-tag
              v-for="permission in getRolePermissions(selectedRole.id)"
              :key="permission.id"
              type="primary"
              effect="light"
              class="current-permission-tag"
            >
              {{ permission.name }}
            </el-tag>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="assignDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="assignPermissions" :disabled="selectedPermissionIds.length === 0">
            分配（{{ selectedPermissionIds.length }}）
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 移除权限对话框 -->
    <el-dialog
      v-model="removeDialogVisible"
      title="从角色移除权限"
      width="700px"
      :close-on-click-modal="false"
    >
      <div v-if="selectedRole">
        <div class="role-info">
          <span class="role-label">角色：</span>
          <span class="role-value">{{ selectedRole.name }}</span>
        </div>
        
        <div class="permission-filter">
          <el-input
            v-model="removePermissionSearch"
            placeholder="搜索权限名称或代码"
            prefix-icon="Search"
            class="permission-search"
            @keyup.enter="filterRemovePermissions"
          />
        </div>
        
        <div class="permission-list">
          <div class="permission-list-header">
            <span>已分配权限列表</span>
            <span class="filtered-count">共 {{ filteredRemovePermissions.length }} 个权限</span>
          </div>
          
          <el-checkbox-group v-model="selectedRemovePermissionIds" class="permission-checkbox-group">
            <el-checkbox
              v-for="permission in filteredRemovePermissions"
              :key="permission.id"
              :label="permission.id"
              class="permission-checkbox"
            >
              <div class="permission-info">
                <div class="permission-name">{{ permission.name }}</div>
                <div class="permission-meta">
                  <span class="permission-codename">{{ permission.codename }}</span>
                  <el-tag
                    :type="getPermissionTypeTagType(permission.type)"
                    size="small"
                    class="permission-type-tag"
                  >
                    {{ getPermissionTypeName(permission.type) }}
                  </el-tag>
                </div>
                <div v-if="permission.description" class="permission-description">{{ permission.description }}</div>
              </div>
            </el-checkbox>
          </el-checkbox-group>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="removeDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="removePermissions" :disabled="selectedRemovePermissionIds.length === 0">
            移除（{{ selectedRemovePermissionIds.length }}）
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Edit, Delete, Plus } from '@element-plus/icons-vue'
import apiClient from '../../api/axiosConfig'

// 响应式数据
const roles = ref([])
const permissions = ref([])
const rolePermissions = ref([])
const loading = ref(false)
const totalRoles = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')

// 选中的角色
const selectedRole = ref(null)

// 对话框状态
const assignDialogVisible = ref(false)
const removeDialogVisible = ref(false)

// 权限搜索和过滤
const permissionSearch = ref('')
const permissionTypeFilter = ref('')
const removePermissionSearch = ref('')

// 选中的权限
const selectedPermissionIds = ref([])
const selectedRemovePermissionIds = ref([])

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

// 获取权限列表
const getPermissions = async () => {
  try {
    const response = await apiClient.get('/api/auth/permissions/')
    permissions.value = response.data.results || response.data
  } catch (error) {
    console.error('获取权限列表失败', error)
    ElMessage.error('获取权限列表失败，请稍后重试')
  }
}

// 获取角色权限关联
const getRolePermissionsData = async () => {
  try {
    const response = await apiClient.get('/api/auth/role-permissions/')
    rolePermissions.value = response.data.results || response.data
  } catch (error) {
    console.error('获取角色权限关联失败', error)
    ElMessage.error('获取角色权限关联失败，请稍后重试')
  }
}

// 过滤后的权限列表
const filteredPermissions = computed(() => {
  return permissions.value.filter(permission => {
    // 搜索过滤
    const matchesSearch = !permissionSearch.value || 
      permission.name.toLowerCase().includes(permissionSearch.value.toLowerCase()) ||
      permission.codename.toLowerCase().includes(permissionSearch.value.toLowerCase())
    
    // 类型过滤
    const matchesType = !permissionTypeFilter.value || permission.type === permissionTypeFilter.value
    
    // 排除已分配的权限
    const notAssigned = !isPermissionAssigned(permission.id)
    
    return matchesSearch && matchesType && notAssigned
  })
})

// 过滤后的移除权限列表
const filteredRemovePermissions = computed(() => {
  if (!selectedRole) return []
  
  const rolePerms = getRolePermissions(selectedRole.id)
  
  return rolePerms.filter(permission => {
    return !removePermissionSearch.value || 
      permission.name.toLowerCase().includes(removePermissionSearch.value.toLowerCase()) ||
      permission.codename.toLowerCase().includes(removePermissionSearch.value.toLowerCase())
  })
})

// 获取角色的权限
const getRolePermissions = (roleId) => {
  const rolePermissionIds = rolePermissions.value
    .filter(rp => rp.role.id === roleId)
    .map(rp => rp.permission.id)
  
  return permissions.value.filter(permission => rolePermissionIds.includes(permission.id))
}

// 检查权限是否已分配给角色
const isPermissionAssigned = (permissionId) => {
  if (!selectedRole) return false
  return rolePermissions.value.some(rp => rp.role.id === selectedRole.id && rp.permission.id === permissionId)
}

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

// 选择角色
const selectRole = (role) => {
  selectedRole.value = role
}

// 打开分配权限对话框
const openAssignDialog = (role) => {
  selectedRole.value = role
  selectedPermissionIds.value = []
  permissionSearch.value = ''
  permissionTypeFilter.value = ''
  assignDialogVisible.value = true
}

// 打开移除权限对话框
const openRemoveDialog = (role) => {
  selectedRole.value = role
  selectedRemovePermissionIds.value = []
  removePermissionSearch.value = ''
  removeDialogVisible.value = true
}

// 过滤权限
const filterPermissions = () => {
  // 计算属性会自动更新
}

// 过滤移除权限
const filterRemovePermissions = () => {
  // 计算属性会自动更新
}

// 分配权限
const assignPermissions = async () => {
  if (!selectedRole || selectedPermissionIds.value.length === 0) return
  
  try {
    // 批量分配权限
    const promises = selectedPermissionIds.value.map(permissionId => {
      return apiClient.post('/api/auth/role-permissions/', {
        role_id: selectedRole.id,
        permission_id: permissionId
      })
    })
    
    await Promise.all(promises)
    
    ElMessage.success(`成功分配 ${selectedPermissionIds.value.length} 个权限`)
    assignDialogVisible.value = false
    getRolePermissionsData()
  } catch (error) {
    console.error('分配权限失败', error)
    if (error.response && error.response.status === 400) {
      ElMessage.error('部分权限可能已分配给角色')
    } else {
      ElMessage.error('分配权限失败，请稍后重试')
    }
  }
}

// 移除权限
const removePermissions = async () => {
  if (!selectedRole || selectedRemovePermissionIds.value.length === 0) return
  
  try {
    // 批量移除权限
    const promises = selectedRemovePermissionIds.value.map(permissionId => {
      // 找到对应的角色权限关联
      const rolePerm = rolePermissions.value.find(
        rp => rp.role.id === selectedRole.id && rp.permission.id === permissionId
      )
      if (rolePerm) {
        return apiClient.delete(`/api/auth/role-permissions/${rolePerm.id}/`)
      }
      return Promise.resolve()
    })
    
    await Promise.all(promises)
    
    ElMessage.success(`成功移除 ${selectedRemovePermissionIds.value.length} 个权限`)
    removeDialogVisible.value = false
    getRolePermissionsData()
  } catch (error) {
    console.error('移除权限失败', error)
    ElMessage.error('移除权限失败，请稍后重试')
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

// 页面加载时获取数据
onMounted(async () => {
  await Promise.all([
    getRoles(),
    getPermissions(),
    getRolePermissionsData()
  ])
})
</script>

<style scoped>
.role-permission-assignment {
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

.selected-row {
  background-color: #ecf5ff !important;
}

.permission-count {
  font-weight: 600;
  color: #409eff;
}

.role-info {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.role-label {
  font-weight: 600;
  margin-right: 5px;
}

.role-value {
  font-weight: 600;
  color: #409eff;
}

.permission-filter {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.permission-search {
  flex: 1;
}

.type-filter {
  width: 150px;
}

.permission-list {
  margin-bottom: 20px;
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 10px;
}

.permission-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.filtered-count {
  font-size: 0.9rem;
  color: #606266;
}

.permission-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.permission-checkbox {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.permission-checkbox:hover {
  background-color: #f5f7fa;
}

.permission-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.permission-name {
  font-weight: 600;
  color: #303133;
}

.permission-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.permission-codename {
  font-size: 0.9rem;
  color: #606266;
  font-family: monospace;
}

.permission-type-tag {
  font-size: 0.8rem;
}

.permission-description {
  font-size: 0.9rem;
  color: #909399;
  margin-top: 5px;
}

.current-permissions {
  margin-top: 20px;
}

.current-permissions-label {
  font-weight: 600;
  margin-right: 10px;
  display: block;
  margin-bottom: 10px;
}

.current-permission-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.current-permission-tag {
  margin-bottom: 5px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .search-input {
    width: 100%;
  }
  
  .permission-filter {
    flex-direction: column;
  }
  
  .type-filter {
    width: 100%;
  }
}
</style>
