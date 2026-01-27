<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="header-left">
        <h1>低代码表单平台</h1>
      </div>
      <div class="header-right">
        <el-button type="primary">新建表单</el-button>
        <el-button>模板库</el-button>
        <el-dropdown>
          <span class="user-dropdown">
            <el-avatar size="small">U</el-avatar>
            <span>用户</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>

    <!-- 三栏布局 -->
    <div class="app-layout">
      <!-- 左侧导航栏 -->
      <aside class="sidebar">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <!-- 商品管理 -->
          <el-sub-menu index="1">
            <template #title>
              <el-icon><Goods /></el-icon>
              <span>商品管理</span>
            </template>
            <el-menu-item index="1-1">
              <el-icon><List /></el-icon>
              <span>商品列表</span>
            </el-menu-item>
            <el-menu-item index="1-2">
              <el-icon><Collection /></el-icon>
              <span>商品分组</span>
            </el-menu-item>
            <el-menu-item index="1-3">
              <el-icon><Management /></el-icon>
              <span>商品分类</span>
            </el-menu-item>
          </el-sub-menu>

          <!-- 订单管理 -->
          <el-sub-menu index="2">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>订单管理</span>
            </template>
            <el-menu-item index="2-1">
              <el-icon><List /></el-icon>
              <span>订单列表</span>
            </el-menu-item>
            <el-menu-item index="2-2">
              <el-icon><Money /></el-icon>
              <span>退款管理</span>
            </el-menu-item>
          </el-sub-menu>

          <!-- 表单管理 -->
          <el-sub-menu index="3" :class="{ 'active': activeMenu.startsWith('3') }">
            <template #title>
              <el-icon><Position /></el-icon>
              <span>表单管理</span>
            </template>
            <el-menu-item index="3-1" :class="{ 'active': activeMenu === '3-1' }">
              <el-icon><Edit /></el-icon>
              <span>表单设计</span>
            </el-menu-item>
            <el-menu-item index="3-2">
              <el-icon><DataAnalysis /></el-icon>
              <span>表单数据</span>
            </el-menu-item>
            <el-menu-item index="3-3">
              <el-icon><Setting /></el-icon>
              <span>表单设置</span>
            </el-menu-item>
          </el-sub-menu>

          <!-- 数据统计 -->
          <el-sub-menu index="4">
            <template #title>
              <el-icon><TrendCharts /></el-icon>
              <span>数据统计</span>
            </template>
            <el-menu-item index="4-1">
              <el-icon><DataLine /></el-icon>
              <span>销售统计</span>
            </el-menu-item>
            <el-menu-item index="4-2">
              <el-icon><DataBoard /></el-icon>
              <span>用户统计</span>
            </el-menu-item>
          </el-sub-menu>

          <!-- 系统设置 -->
          <el-sub-menu index="5">
            <template #title>
              <el-icon><Setting /></el-icon>
              <span>系统设置</span>
            </template>
            <el-menu-item index="5-1">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </el-menu-item>
            <el-menu-item index="5-2">
              <el-icon><Lock /></el-icon>
              <span>权限设置</span>
            </el-menu-item>
            <el-menu-item index="5-3">
              <el-icon><Monitor /></el-icon>
              <span>系统日志</span>
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
      </aside>

      <!-- 中间主内容区 -->
      <main class="main-content">
        <!-- 顶部状态标签 -->
        <div class="content-header">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>表单管理</el-breadcrumb-item>
            <el-breadcrumb-item>表单设计</el-breadcrumb-item>
          </el-breadcrumb>
          <div class="content-actions">
            <el-button size="small">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
            <el-button size="small">
              <el-icon><Download /></el-icon>
              导出
            </el-button>
          </div>
        </div>

        <!-- 筛选区 -->
        <div class="filter-section">
          <el-form :inline="true" size="small">
            <el-form-item label="表单名称">
              <el-input v-model="formName" placeholder="请输入表单名称" style="width: 200px" />
            </el-form-item>
            <el-form-item label="创建时间">
              <el-date-picker
                v-model="createTime"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                style="width: 250px"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">
                <el-icon><Search /></el-icon>
                搜索
              </el-button>
              <el-button @click="resetForm">
                <el-icon><Refresh /></el-icon>
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 表单列表 -->
        <div class="form-list-section">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>表单列表</span>
                <el-button type="primary" size="small" @click="openDesignDialog">
                  <el-icon><Plus /></el-icon>
                  新建表单
                </el-button>
              </div>
            </template>
            <el-table :data="formList" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="表单名称" min-width="200" />
              <el-table-column prop="created_at" label="创建时间" width="180" />
              <el-table-column prop="updated_at" label="更新时间" width="180" />
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="editForm(scope.row)">
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteForm(scope.row.id)">
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

        <!-- 表单设计弹窗 -->
        <el-dialog
          v-model="designDialogVisible"
          title="表单设计"
          width="90%"
          height="90vh"
        >
          <div class="designer-container">
            <div class="designer-section">
              <h3>表单设计器</h3>
              <v-form-design 
                ref="designerRef" 
                :disabled="false"
                :height="500"
              />
              <div class="designer-actions">
                <el-button type="primary" @click="saveForm">
                  <el-icon><Check /></el-icon>
                  保存表单
                </el-button>
                <el-button @click="loadForm">
                  <el-icon><Download /></el-icon>
                  加载表单
                </el-button>
                <el-button @click="clearForm">
                  <el-icon><Delete /></el-icon>
                  清空表单
                </el-button>
              </div>
            </div>
            <div class="preview-section">
              <h3>表单预览</h3>
              <v-form-render 
                v-if="formConfig" 
                :form-config="formConfig"
                :form-data="formData"
                @submit="handleSubmit"
              />
              <div v-else class="empty-preview">
                请先设计表单
              </div>
            </div>
          </div>
        </el-dialog>
      </main>

      <!-- 右侧辅助面板 -->
      <aside class="right-panel">
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
              <el-icon><Book /></el-icon>
              <a href="#">API文档</a>
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { VFormDesign, VFormRender } from 'vform3-builds'
import axios from 'axios'
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
  Setting,
  TrendCharts,
  DataLine,
  DataBoard,
  User,
  Lock,
  Monitor,
  Refresh,
  Download,
  Search,
  Plus,
  Check,
  Delete,
  HelpFilled,
  Reading,
  Message,
  Book,
  VideoCamera,
  Service,
  ChatLineRound,
  Bell
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 配置axios默认值
axios.defaults.baseURL = 'http://localhost:8000'

// 响应式数据
const activeMenu = ref('3-1')
const formName = ref('')
const createTime = ref([])
const formList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const designDialogVisible = ref(false)
const notifications = ref([
  { title: '系统更新', content: '平台已更新至最新版本，新增表单模板功能' },
  { title: '安全提醒', content: '请及时更新密码，保障账户安全' },
  { title: '数据备份', content: '系统已完成自动数据备份' }
])

// 表单设计相关
const designerRef = ref(null)
const formConfig = ref(null)
const formData = ref({})
const formId = ref(null)

// 菜单选择
const handleMenuSelect = (key) => {
  activeMenu.value = key
}

// 搜索表单
const handleSearch = () => {
  // 模拟搜索功能
  console.log('搜索表单:', { formName: formName.value, createTime: createTime.value })
  fetchForms()
}

// 重置表单
const resetForm = () => {
  formName.value = ''
  createTime.value = []
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchForms()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchForms()
}

// 打开设计弹窗
const openDesignDialog = () => {
  formId.value = null
  formConfig.value = null
  designDialogVisible.value = true
}

// 编辑表单
const editForm = (row) => {
  formId.value = row.id
  formConfig.value = JSON.parse(row.config)
  designDialogVisible.value = true
}

// 删除表单
const deleteForm = (id) => {
  // 模拟删除功能
  console.log('删除表单:', id)
  // 实际项目中应调用API删除
  fetchForms()
}

// 获取表单列表
const fetchForms = async () => {
  try {
    const response = await axios.get('/api/form-configs/')
    formList.value = response.data
    total.value = response.data.length
  } catch (error) {
    console.error('获取表单列表失败', error)
    formList.value = []
    total.value = 0
  }
}

// 保存表单配置
const saveForm = async () => {
  try {
    const config = designerRef.value.getFormConfig()
    if (!config) return
    
    if (formId.value) {
      // 更新表单
      const response = await axios.put(`/api/form-configs/${formId.value}/`, { config: JSON.stringify(config), name: `表单${formId.value}` })
      console.log('表单更新成功', response.data)
      ElMessage.success('表单更新成功')
    } else {
      // 创建新表单
      const response = await axios.post('/api/form-configs/', { config: JSON.stringify(config), name: '新表单' })
      formId.value = response.data.id
      console.log('表单保存成功', response.data)
      ElMessage.success('表单保存成功')
    }
    fetchForms()
  } catch (error) {
    console.error('保存表单失败', error)
    ElMessage.error('保存表单失败')
  }
}

// 加载表单配置
const loadForm = async () => {
  try {
    // 这里可以改为从列表中选择表单，暂时加载第一个
    const response = await axios.get('/api/form-configs/')
    if (response.data.length > 0) {
      const form = response.data[0]
      formId.value = form.id
      formConfig.value = JSON.parse(form.config)
      designerRef.value.setFormConfig(formConfig.value)
      console.log('表单加载成功', form)
      ElMessage.success('表单加载成功')
    }
  } catch (error) {
    console.error('加载表单失败', error)
    ElMessage.error('加载表单失败')
  }
}

// 清空表单
const clearForm = () => {
  designerRef.value.clearFormConfig()
  formConfig.value = null
  formId.value = null
  formData.value = {}
  ElMessage.info('表单已清空')
}

// 处理表单提交
const handleSubmit = (data) => {
  console.log('表单提交数据', data)
  ElMessage.success('表单提交成功！')
}

// 初始化
onMounted(() => {
  fetchForms()
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

/* 表单列表区 */
.form-list-section {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 设计器弹窗 */
.designer-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.designer-section,
.preview-section {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
}

.designer-section h3,
.preview-section h3 {
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.designer-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.empty-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 500px;
  background: white;
  border: 2px dashed #ddd;
  border-radius: 4px;
  color: #999;
  font-size: 16px;
}

/* 右侧辅助面板 */
.right-panel {
  width: 280px;
  background-color: #fff;
  border-left: 1px solid #eaeaea;
  padding: 20px;
  overflow-y: auto;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.08);
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
  
  .right-panel {
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
  
  .main-content {
    padding: 10px;
  }
  
  .designer-container {
    grid-template-columns: 1fr;
  }
}
</style>