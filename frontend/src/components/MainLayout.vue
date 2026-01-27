<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="header-left">
        <h1>低代码表单平台</h1>
      </div>
      <div class="header-right">
        <el-button @click="navigateToTemplates">模板库</el-button>
        <template v-if="isLoggedIn">
          <el-dropdown>
            <span class="user-dropdown">
              <el-avatar size="small">{{ user.username?.charAt(0) || 'U' }}</el-avatar>
              <span>{{ user.username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="navigateToProfile">个人中心</el-dropdown-item>
                <el-dropdown-item @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" @click="navigateToLogin">
            <el-icon><User /></el-icon>
            登录
          </el-button>
        </template>
      </div>
    </header>

    <!-- 三栏布局 -->
    <div class="app-layout">
      <!-- 左侧导航栏 -->
      <aside class="sidebar" :class="{ 'collapsed': !sidebarVisible }">
        <div class="sidebar-header">
          <el-button 
            class="collapse-btn" 
            @click="toggleSidebar"
            :icon="sidebarVisible ? Fold : Expand"
          />
        </div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <!-- 商品管理 -->
          <el-sub-menu index="1">
            <template #title>
              <el-icon><Goods /></el-icon>
              <span v-if="sidebarVisible">商品管理</span>
            </template>
            <el-menu-item index="1-1">
              <el-icon><List /></el-icon>
              <span v-if="sidebarVisible">商品列表</span>
            </el-menu-item>
            <el-menu-item index="1-2">
              <el-icon><Collection /></el-icon>
              <span v-if="sidebarVisible">商品分组</span>
            </el-menu-item>
            <el-menu-item index="1-3">
              <el-icon><Management /></el-icon>
              <span v-if="sidebarVisible">商品分类</span>
            </el-menu-item>
          </el-sub-menu>

          <!-- 订单管理 -->
          <el-sub-menu index="2">
            <template #title>
              <el-icon><Document /></el-icon>
              <span v-if="sidebarVisible">订单管理</span>
            </template>
            <el-menu-item index="2-1">
              <el-icon><List /></el-icon>
              <span v-if="sidebarVisible">订单列表</span>
            </el-menu-item>
            <el-menu-item index="2-2">
              <el-icon><Money /></el-icon>
              <span v-if="sidebarVisible">退款管理</span>
            </el-menu-item>
          </el-sub-menu>

          <!-- 表单管理 -->
          <el-sub-menu index="3" :class="{ 'active': activeMenu.startsWith('3') }">
            <template #title>
              <el-icon><Position /></el-icon>
              <span v-if="sidebarVisible">表单管理</span>
            </template>
            <el-menu-item index="3-1" @click="navigateToHome">
              <el-icon><List /></el-icon>
              <span v-if="sidebarVisible">表单列表</span>
            </el-menu-item>
            <el-menu-item index="3-2" @click="navigateToDesign">
              <el-icon><Edit /></el-icon>
              <span v-if="sidebarVisible">表单设计</span>
            </el-menu-item>
            <el-menu-item index="3-3" @click="navigateToData">
              <el-icon><DataAnalysis /></el-icon>
              <span v-if="sidebarVisible">表单数据</span>
            </el-menu-item>
          </el-sub-menu>

          <!-- 数据统计 -->
          <el-sub-menu index="4">
            <template #title>
              <el-icon><TrendCharts /></el-icon>
              <span v-if="sidebarVisible">数据统计</span>
            </template>
            <el-menu-item index="4-1">
              <el-icon><DataLine /></el-icon>
              <span v-if="sidebarVisible">销售统计</span>
            </el-menu-item>
            <el-menu-item index="4-2">
              <el-icon><DataBoard /></el-icon>
              <span v-if="sidebarVisible">用户统计</span>
            </el-menu-item>
          </el-sub-menu>

          <!-- 系统设置 -->
          <el-sub-menu index="5">
            <template #title>
              <el-icon><Setting /></el-icon>
              <span v-if="sidebarVisible">系统设置</span>
            </template>
            <el-menu-item index="5-1" @click="navigateToUserManagement">
              <el-icon><User /></el-icon>
              <span v-if="sidebarVisible">用户管理</span>
            </el-menu-item>
            <el-menu-item index="5-2" @click="navigateToPermissionManagement" v-permission="'permission_manage'">
              <el-icon><Lock /></el-icon>
              <span v-if="sidebarVisible">权限管理</span>
            </el-menu-item>
            <el-menu-item index="5-3" @click="navigateToSystemLogs">
              <el-icon><Monitor /></el-icon>
              <span v-if="sidebarVisible">系统日志</span>
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
      </aside>

      <!-- 中间主内容区 -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

      <!-- 右侧辅助面板 -->
      <aside v-if="rightPanelVisible" class="right-panel">
        <div class="panel-header">
          <el-button 
            class="collapse-btn" 
            @click="toggleRightPanel"
            :icon="ArrowRight" 
          />
        </div>
        <div class="panel-section">
          <h3>
            <el-icon><HelpFilled /></el-icon>
            帮助中心
          </h3>
          <ul class="help-list">
            <li>
              <el-icon><Reading /></el-icon>
              <a href="#">使用指南</a>
            </li>
            <li>
              <el-icon><Message /></el-icon>
              <a href="#">常见问题</a>
            </li>
            <li>
              <el-icon><DocumentCopy /></el-icon>
              <a href="http://localhost:8000/api/docs/" target="_blank">API文档</a>
            </li>
            <li>
              <el-icon><VideoCamera /></el-icon>
              <a href="#">视频教程</a>
            </li>
          </ul>
        </div>

        <div class="panel-section">
          <h3>
            <el-icon><Service /></el-icon>
            客服中心
          </h3>
          <div class="customer-service">
            <el-button type="primary" class="service-btn">
              <el-icon><ChatLineRound /></el-icon>
              在线客服
            </el-button>
            <div class="service-info">
              <p>工作时间：9:00-18:00</p>
              <p>联系电话：400-123-4567</p>
            </div>
          </div>
        </div>

        <div class="panel-section">
          <h3>
            <el-icon><Bell /></el-icon>
            系统通知
          </h3>
          <div class="notification-list">
            <el-alert
              v-for="(notification, index) in notifications"
              :key="index"
              :title="notification.title"
              :description="notification.content"
              type="info"
              :closable="false"
              show-icon
              size="small"
            />
          </div>
        </div>
      </aside>
      <!-- 右侧面板隐藏时的显示按钮 -->
      <div v-else class="right-panel-toggle" @click="toggleRightPanel">
        <el-button :icon="ArrowLeft" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Goods,
  List,
  Collection,
  Management,
  Document,
  Money,
  Position,
  Edit,
  DataAnalysis,
  TrendCharts,
  DataLine,
  DataBoard,
  User,
  Lock,
  Monitor,
  Setting,
  HelpFilled,
  Reading,
  Message,
  DocumentCopy,
  VideoCamera,
  Service,
  ChatLineRound,
  Bell,
  Fold,
  Expand,
  ArrowLeft,
  ArrowRight,
  SwitchButton
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

// 响应式数据
const activeMenu = ref('3-1')
const notifications = ref([
  { title: '系统更新', content: '平台已更新至最新版本，新增表单模板功能' },
  { title: '安全提醒', content: '请及时更新密码，保障账户安全' },
  { title: '数据备份', content: '系统已完成自动数据备份' }
])
const sidebarVisible = ref(true)
const rightPanelVisible = ref(true)
const user = ref(null)
const isLoggedIn = ref(false)

// 菜单选择
const handleMenuSelect = (key) => {
  activeMenu.value = key
}

// 导航到首页
const navigateToHome = () => {
  router.push('/')
  activeMenu.value = '3-1'
}

// 导航到表单设计页面
const navigateToDesign = () => {
  router.push('/form/design')
  activeMenu.value = '3-2'
}

// 导航到表单数据页面
const navigateToData = () => {
  router.push('/form/data')
  activeMenu.value = '3-3'
}

// 导航到模板库
const navigateToTemplates = () => {
  router.push('/templates')
}

// 导航到系统日志
const navigateToSystemLogs = () => {
  router.push('/system/logs')
}

// 导航到用户管理
const navigateToUserManagement = () => {
  router.push('/system/users')
}

// 导航到权限管理
const navigateToPermissionManagement = () => {
  router.push('/system/permissions')
}

// 导航到登录页面
const navigateToLogin = () => {
  router.push('/login')
}

// 导航到个人中心
const navigateToProfile = () => {
  router.push('/profile')
}

// 处理登出
const handleLogout = () => {
  // 清除本地存储的登录状态
  localStorage.removeItem('token')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('user')
  
  // 更新状态
  user.value = null
  isLoggedIn.value = false
  
  ElMessage.success('登出成功')
  // 跳转到登录页面
  router.push('/login')
}

// 初始化登录状态
const initLoginStatus = () => {
  const userInfo = localStorage.getItem('user')
  if (userInfo) {
    user.value = JSON.parse(userInfo)
    isLoggedIn.value = true
  }
}

// 切换左侧导航栏
const toggleSidebar = () => {
  sidebarVisible.value = !sidebarVisible.value
}

// 切换右侧面板
const toggleRightPanel = () => {
  rightPanelVisible.value = !rightPanelVisible.value
}

// 初始化
onMounted(() => {
  initLoginStatus()
})
</script>

<style scoped>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-container {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部导航栏 */
.app-header {
  background-color: #fff;
  border-bottom: 1px solid #eaeaea;
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-left h1 {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-dropdown:hover {
  background-color: #f5f7fa;
}

/* 三栏布局 */
.app-layout {
  display: flex;
  flex: 1;
  min-height: 0;
}

/* 左侧导航栏 */
.sidebar {
  width: 220px;
  background-color: #fff;
  border-right: 1px solid #eaeaea;
  overflow-y: auto;
  transition: width 0.3s;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.08);
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  display: flex;
  justify-content: flex-end;
  padding: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.collapse-btn {
  width: 32px;
  height: 32px;
  padding: 4px;
}

.sidebar-menu {
  border-right: none;
}

.sidebar-menu .el-sub-menu__title,
.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
  margin: 0 10px;
  border-radius: 4px;
}

.sidebar-menu .el-menu-item.is-active {
  background-color: #ecf5ff;
  color: #409eff;
}

/* 中间主内容区 */
.main-content {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
  overflow-y: auto;
}

/* 右侧辅助面板 */
.right-panel {
  width: 280px;
  background-color: #fff;
  border-left: 1px solid #eaeaea;
  padding: 20px;
  overflow-y: auto;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s;
}

.panel-header {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 15px;
}

/* 右侧面板隐藏时的显示按钮 */
.right-panel-toggle {
  width: 40px;
  background-color: #fff;
  border-left: 1px solid #eaeaea;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.right-panel-toggle:hover {
  background-color: #f5f7fa;
}

.panel-section {
  margin-bottom: 30px;
}

.panel-section h3 {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.help-list {
  list-style: none;
}

.help-list li {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.help-list li a {
  color: #409eff;
  text-decoration: none;
  transition: color 0.3s;
}

.help-list li a:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.customer-service {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.service-btn {
  width: 100%;
}

.service-info {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

.notification-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .right-panel {
    width: 240px;
  }
}

@media (max-width: 992px) {
  .sidebar {
    width: 180px;
  }
  
  .sidebar.collapsed {
    width: 64px;
  }
  
  .right-panel {
    display: none;
  }
  
  .right-panel-toggle {
    display: none;
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: -180px;
    top: 60px;
    height: calc(100vh - 60px);
    z-index: 999;
  }
  
  .sidebar.open {
    left: 0;
  }
  
  .sidebar.collapsed {
    left: 0;
    width: 64px;
  }
  
  .main-content {
    padding: 10px;
  }
}
</style>
