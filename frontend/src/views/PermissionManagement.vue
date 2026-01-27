<template>
  <div class="permission-management-container">
    <div class="permission-header">
      <h2>权限管理</h2>
      <p>管理系统角色和权限分配</p>
    </div>
    
    <div class="permission-tabs">
      <el-tabs v-model="activeTab" class="permission-tabs">
        <el-tab-pane label="角色管理" name="roles">
          <RoleManagement />
        </el-tab-pane>
        <el-tab-pane label="权限管理" name="permissions">
          <PermissionList />
        </el-tab-pane>
        <el-tab-pane label="用户角色分配" name="user-roles">
          <UserRoleAssignment />
        </el-tab-pane>
        <el-tab-pane label="角色权限分配" name="role-permissions">
          <RolePermissionAssignment />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import RoleManagement from '../components/permission/RoleManagement.vue'
import PermissionList from '../components/permission/PermissionList.vue'
import UserRoleAssignment from '../components/permission/UserRoleAssignment.vue'
import RolePermissionAssignment from '../components/permission/RolePermissionAssignment.vue'

const activeTab = ref('roles')
</script>

<style scoped>
.permission-management-container {
  padding: 20px;
  min-height: 80vh;
  background-color: #f5f7fa;
}

.permission-header {
  margin-bottom: 30px;
  text-align: center;
}

.permission-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #303133;
  margin-bottom: 10px;
}

.permission-header p {
  font-size: 1rem;
  color: #606266;
}

.permission-tabs {
  max-width: 1200px;
  margin: 0 auto;
}

.permission-tabs .el-tabs__header {
  margin-bottom: 30px;
}

.permission-tabs .el-tabs__item {
  font-size: 1rem;
  font-weight: 500;
  padding: 0 20px;
}

.permission-tabs .el-tabs__content {
  background-color: #fff;
  border-radius: 0 0 12px 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .permission-management-container {
    padding: 10px;
  }
  
  .permission-header h2 {
    font-size: 1.8rem;
  }
  
  .permission-tabs {
    padding: 0 10px;
  }
  
  .permission-tabs .el-tabs__content {
    padding: 15px;
  }
}
</style>
