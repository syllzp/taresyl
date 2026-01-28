<template>
  <div class="route-permission-container">
    <div class="content-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>系统设置</el-breadcrumb-item>
        <el-breadcrumb-item>路由权限</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="content-actions">
        <el-button size="small" @click="refreshRoutePermissions">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 路由权限列表 -->
    <el-card class="route-permission-card">
      <template #header>
        <div class="card-header">
          <span>前端路由权限管理</span>
          <span class="route-count">共 {{ routePermissions.length }} 个路由</span>
        </div>
      </template>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>

      <div v-else-if="routePermissions.length === 0" class="empty-container">
        <el-empty description="暂无路由权限数据" />
      </div>

      <el-table
        v-else
        :data="routePermissions"
        style="width: 100%"
        border
        stripe
      >
        <el-table-column prop="path" label="路由路径" min-width="200" />
        <el-table-column prop="name" label="路由名称" min-width="150" />
        <el-table-column prop="component" label="组件路径" min-width="300" />
        <el-table-column prop="meta.title" label="页面标题" min-width="150" />
        <el-table-column prop="meta.requiredPermission" label="所需权限" min-width="150">
          <template #default="scope">
            <el-tag v-if="scope.row.meta.requiredPermission" type="info">
              {{ scope.row.meta.requiredPermission }}
            </el-tag>
            <el-tag v-else type="default">
              无
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="meta.requiresAuth" label="需要认证" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.meta.requiresAuth ? 'success' : 'info'">
              {{ scope.row.meta.requiresAuth ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="用户权限" min-width="150">
          <template #default="scope">
            <div v-if="scope.row.meta.requiredPermission">
              <el-tag :type="hasPermission(scope.row.meta.requiredPermission) ? 'success' : 'danger'">
                {{ hasPermission(scope.row.meta.requiredPermission) ? '有权限' : '无权限' }}
              </el-tag>
            </div>
            <div v-else>
              <el-tag type="success">
                无需权限
              </el-tag>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 权限说明 -->
    <el-card class="permission-guide-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>权限说明</span>
        </div>
      </template>
      <div class="permission-guide-content">
        <h4>路由权限配置</h4>
        <p>1. 在路由配置中，通过 <code>meta.requiredPermission</code> 属性设置路由所需的权限</p>
        <p>2. 通过 <code>meta.requiresAuth</code> 属性设置路由是否需要认证</p>
        <p>3. 无 <code>requiredPermission</code> 属性的路由表示不需要特定权限</p>
        <h4>权限检查</h4>
        <p>1. 路由守卫会检查用户是否有权限访问特定路由</p>
        <p>2. 组件中可以使用 <code>v-permission</code> 指令进行权限控制</p>
        <p>3. 代码中可以使用 <code>permissionService.hasPermission()</code> 进行权限检查</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import permissionService from '../services/permissionService'
import router from '../router/index.js'

// 响应式数据
const routePermissions = ref([])
const loading = ref(false)

// 计算属性：获取用户权限
const userPermissions = computed(() => {
  return permissionService.userPermissions.map(p => p.codename)
})

// 检查用户是否有指定权限
const hasPermission = (permission) => {
  return permissionService.hasPermission(permission)
}

// 获取路由权限信息
const getRoutePermissions = () => {
  loading.value = true
  try {
    // 从路由配置中提取权限信息
    const routes = router.getRoutes()
    const permissionRoutes = []

    // 递归处理路由
    const processRoute = (route) => {
      // 只处理有路径的路由
      if (route.path && route.path !== '*') {
        permissionRoutes.push({
          path: route.path,
          name: route.name || '',
          component: route.component?.name || route.component?.toString() || '',
          meta: {
            title: route.meta?.title || '',
            requiresAuth: route.meta?.requiresAuth || false,
            requiredPermission: route.meta?.requiredPermission || ''
          }
        })
      }

      // 处理子路由
      if (route.children && route.children.length > 0) {
        route.children.forEach(childRoute => {
          processRoute(childRoute)
        })
      }
    }

    // 处理所有路由
    routes.forEach(route => {
      processRoute(route)
    })

    routePermissions.value = permissionRoutes
  } catch (error) {
    console.error('获取路由权限失败', error)
    ElMessage.error('获取路由权限失败')
  } finally {
    loading.value = false
  }
}

// 刷新路由权限
const refreshRoutePermissions = async () => {
  try {
    // 刷新用户权限
    await permissionService.refreshPermissions()
    // 重新获取路由权限
    getRoutePermissions()
    ElMessage.success('路由权限刷新成功')
  } catch (error) {
    console.error('刷新路由权限失败', error)
    ElMessage.error('刷新路由权限失败')
  }
}

// 初始化
onMounted(() => {
  getRoutePermissions()
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

/* 路由权限卡片 */
.route-permission-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.route-count {
  font-size: 14px;
  color: #606266;
}

.loading-container {
  padding: 20px 0;
}

.empty-container {
  padding: 40px 0;
}

/* 权限说明卡片 */
.permission-guide-content {
  line-height: 1.8;
}

.permission-guide-content h4 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #303133;
}

.permission-guide-content p {
  margin-bottom: 8px;
  color: #606266;
}

.permission-guide-content code {
  background-color: #f5f7fa;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: Consolas, Monaco, 'Andale Mono', monospace;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .content-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>