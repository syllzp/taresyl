<template>
  <div class="system-log-container">
    <div class="content-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>系统设置</el-breadcrumb-item>
        <el-breadcrumb-item>系统日志</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="content-actions">
        <el-button size="small" @click="refreshLogs">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
        <el-button size="small" @click="clearLogs">
          <el-icon><Delete /></el-icon>
          清空日志
        </el-button>
      </div>
    </div>

    <!-- 筛选区 -->
    <div class="filter-section">
      <el-form :inline="true" size="small">
        <el-form-item label="日志级别">
          <el-select v-model="filterForm.level" placeholder="请选择日志级别">
            <el-option label="全部" value="" />
            <el-option label="调试" value="DEBUG" />
            <el-option label="信息" value="INFO" />
            <el-option label="警告" value="WARNING" />
            <el-option label="错误" value="ERROR" />
            <el-option label="严重" value="CRITICAL" />
          </el-select>
        </el-form-item>
        <el-form-item label="资源类型">
          <el-select v-model="filterForm.resourceType" placeholder="请选择资源类型">
            <el-option label="全部" value="" />
            <el-option label="表单" value="FORM" />
            <el-option label="用户" value="USER" />
            <el-option label="系统" value="SYSTEM" />
            <el-option label="其他" value="OTHER" />
          </el-select>
        </el-form-item>
        <el-form-item label="操作时间">
          <el-date-picker
            v-model="filterForm.dateRange"
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
          <el-button @click="resetFilter">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 日志列表 -->
    <div class="log-list-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>系统日志</span>
            <span class="log-count">共 {{ total }} 条日志</span>
          </div>
        </template>
        <el-table :data="logList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="level" label="级别" width="100">
            <template #default="scope">
              <el-tag :type="getLevelType(scope.row.level)">
                {{ getLevelText(scope.row.level) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="message" label="消息" min-width="400">
            <template #default="scope">
              <div class="log-message" @click="showLogDetail(scope.row)">
                {{ scope.row.message }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="resource_type" label="资源类型" width="120">
            <template #default="scope">
              {{ getResourceTypeText(scope.row.resource_type) }}
            </template>
          </el-table-column>
          <el-table-column prop="resource_id" label="资源ID" width="100" />
          <el-table-column prop="user" label="操作用户" width="150">
            <template #default="scope">
              {{ scope.row.user ? scope.row.user.username : '-' }}
            </template>
          </el-table-column>
          <el-table-column prop="ip_address" label="IP地址" width="150" />
          <el-table-column prop="created_at" label="操作时间" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.created_at) }}
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

    <!-- 日志详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="日志详情"
      width="80%"
    >
      <div class="log-detail" v-if="selectedLog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="日志ID">{{ selectedLog.id }}</el-descriptions-item>
          <el-descriptions-item label="日志级别">
            <el-tag :type="getLevelType(selectedLog.level)">
              {{ getLevelText(selectedLog.level) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="日志消息">{{ selectedLog.message }}</el-descriptions-item>
          <el-descriptions-item label="资源类型">{{ getResourceTypeText(selectedLog.resource_type) }}</el-descriptions-item>
          <el-descriptions-item label="资源ID">{{ selectedLog.resource_id || '-' }}</el-descriptions-item>
          <el-descriptions-item label="操作用户">{{ selectedLog.user ? selectedLog.user.username : '-' }}</el-descriptions-item>
          <el-descriptions-item label="操作IP地址">{{ selectedLog.ip_address || '-' }}</el-descriptions-item>
          <el-descriptions-item label="操作时间">{{ formatDateTime(selectedLog.created_at) }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { systemLogApi } from '../api/systemService'
import {
  Refresh,
  Delete,
  Search
} from '@element-plus/icons-vue'

// 响应式数据
const logList = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const filterForm = ref({
  level: '',
  resourceType: '',
  dateRange: []
})
const detailDialogVisible = ref(false)
const selectedLog = ref(null)

// 格式化时间
const formatDateTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

// 获取日志级别对应的标签类型
const getLevelType = (level) => {
  const typeMap = {
    'DEBUG': 'info',
    'INFO': 'success',
    'WARNING': 'warning',
    'ERROR': 'danger',
    'CRITICAL': 'danger'
  }
  return typeMap[level] || 'info'
}

// 获取日志级别对应的文本
const getLevelText = (level) => {
  const textMap = {
    'DEBUG': '调试',
    'INFO': '信息',
    'WARNING': '警告',
    'ERROR': '错误',
    'CRITICAL': '严重'
  }
  return textMap[level] || level
}

// 获取资源类型对应的文本
const getResourceTypeText = (resourceType) => {
  if (!resourceType) return '-'
  const textMap = {
    'FORM': '表单',
    'USER': '用户',
    'SYSTEM': '系统',
    'OTHER': '其他'
  }
  return textMap[resourceType] || resourceType
}

// 刷新日志列表
const refreshLogs = () => {
  fetchLogs()
}

// 清空日志
const clearLogs = () => {
  ElMessageBox.confirm('确定要清空所有系统日志吗？此操作不可恢复。', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 这里应该调用清空日志的API，暂时用模拟实现
    ElMessage.success('日志清空成功')
    fetchLogs()
  }).catch(() => {
    // 取消操作
  })
}

// 搜索日志
const handleSearch = () => {
  currentPage.value = 1
  fetchLogs()
}

// 重置筛选条件
const resetFilter = () => {
  filterForm.value = {
    level: '',
    resourceType: '',
    dateRange: []
  }
  currentPage.value = 1
  fetchLogs()
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchLogs()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchLogs()
}

// 获取日志列表
const fetchLogs = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    // 添加筛选条件
    if (filterForm.value.level) {
      params.level = filterForm.value.level
    }
    if (filterForm.value.resourceType) {
      params.resource_type = filterForm.value.resourceType
    }
    if (filterForm.value.dateRange && filterForm.value.dateRange.length === 2) {
      params.start_date = filterForm.value.dateRange[0]
      params.end_date = filterForm.value.dateRange[1]
    }
    
    const data = await systemLogApi.getAll(params)
    logList.value = data.results || data
    total.value = data.count || data.length
  } catch (error) {
    console.error('获取系统日志失败', error)
    ElMessage.error('获取系统日志失败')
  }
}

// 显示日志详情
const showLogDetail = (log) => {
  selectedLog.value = log
  detailDialogVisible.value = true
}

// 初始化
onMounted(() => {
  fetchLogs()
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

/* 日志列表区 */
.log-list-section {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.log-count {
  font-size: 14px;
  color: #606266;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 日志消息 */
.log-message {
  cursor: pointer;
  color: #409eff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.log-message:hover {
  text-decoration: underline;
}

/* 日志详情 */
.log-detail {
  padding: 10px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .filter-section {
    padding: 10px;
  }
  
  .log-list-section {
    margin-bottom: 10px;
  }
  
  .pagination {
    margin-top: 10px;
  }
}
</style>
