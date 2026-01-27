<template>
  <div class="form-data-container">
    <div class="content-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>表单管理</el-breadcrumb-item>
        <el-breadcrumb-item>表单数据</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="content-actions">
        <el-button size="small" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <el-button size="small">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>
    </div>

    <!-- 筛选区 -->
    <div class="filter-section">
      <el-form :inline="true" size="small">
        <el-form-item label="表单名称">
          <el-select v-model="selectedForm" placeholder="请选择表单">
            <el-option 
              v-for="form in formList" 
              :key="form.id" 
              :label="form.name" 
              :value="form.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="提交时间">
          <el-date-picker
            v-model="submitTime"
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

    <!-- 数据列表 -->
    <div class="data-list-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>表单数据列表</span>
            <span class="data-count">共 {{ total }} 条数据</span>
          </div>
        </template>
        <el-table :data="dataList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="formName" label="表单名称" min-width="150" />
          <el-table-column prop="data" label="提交数据" min-width="300">
            <template #default="scope">
              <el-button 
                type="text" 
                @click="showDataDetail(scope.row.data)"
              >
                查看详情
              </el-button>
            </template>
          </el-table-column>
          <el-table-column prop="submittedAt" label="提交时间" width="180" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="editData(scope.row)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="deleteData(scope.row.id)">
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

    <!-- 数据详情弹窗 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="数据详情"
      width="60%"
    >
      <pre>{{ formattedDataDetail }}</pre>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { formConfigApi } from '../api/formService'
import {
  ArrowLeft,
  Download,
  Search,
  Refresh,
  Edit,
  Delete
} from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const formList = ref([])
const selectedForm = ref('')
const submitTime = ref([])
const dataList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const detailDialogVisible = ref(false)
const dataDetail = ref({})

// 计算属性
const formattedDataDetail = computed(() => {
  return JSON.stringify(dataDetail.value, null, 2)
})

// 返回上一页
const goBack = () => {
  router.push('/')
}

// 搜索数据
const handleSearch = () => {
  // 模拟搜索功能
  console.log('搜索数据:', { selectedForm: selectedForm.value, submitTime: submitTime.value })
  fetchFormData()
}

// 重置表单
const resetForm = () => {
  selectedForm.value = ''
  submitTime.value = []
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchFormData()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchFormData()
}

// 获取表单列表
const fetchForms = async () => {
  try {
    const forms = await formConfigApi.getAll()
    formList.value = forms
  } catch (error) {
    console.error('获取表单列表失败', error)
    ElMessage.error('获取表单列表失败')
  }
}

// 获取表单数据
const fetchFormData = async () => {
  try {
    // 模拟数据
    dataList.value = [
      {
        id: 1,
        formName: '用户注册表单',
        data: { username: 'test1', email: 'test1@example.com', phone: '13800138001' },
        submittedAt: '2026-01-27 10:00:00'
      },
      {
        id: 2,
        formName: '用户注册表单',
        data: { username: 'test2', email: 'test2@example.com', phone: '13800138002' },
        submittedAt: '2026-01-27 11:00:00'
      }
    ]
    total.value = dataList.value.length
  } catch (error) {
    console.error('获取表单数据失败', error)
    ElMessage.error('获取表单数据失败')
  }
}

// 查看数据详情
const showDataDetail = (data) => {
  dataDetail.value = data
  detailDialogVisible.value = true
}

// 编辑数据
const editData = (row) => {
  console.log('编辑数据:', row)
  ElMessage.info('编辑功能开发中')
}

// 删除数据
const deleteData = (id) => {
  console.log('删除数据:', id)
  ElMessage.info('删除功能开发中')
}

// 初始化
onMounted(() => {
  fetchForms()
  fetchFormData()
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

/* 数据列表区 */
.data-list-section {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.data-count {
  color: #606266;
  font-size: 14px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 数据详情 */
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: monospace;
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  max-height: 400px;
  overflow-y: auto;
}
</style>
