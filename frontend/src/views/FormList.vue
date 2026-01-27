<template>
  <div class="form-list-container">
    <div class="content-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>表单管理</el-breadcrumb-item>
        <el-breadcrumb-item>表单列表</el-breadcrumb-item>
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
            <el-button type="primary" size="small" @click="navigateToDesign">
              <el-icon><Plus /></el-icon>
              新建表单
            </el-button>
          </div>
        </template>
        <el-table :data="formList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="表单名称" min-width="200">
            <template #default="scope">
              <div class="form-name-edit">
                <el-input
                  v-if="editingId === scope.row.id"
                  v-model="editingName"
                  size="small"
                  @blur="saveFormName(scope.row.id)"
                  @keyup.enter="saveFormName(scope.row.id)"
                  @keyup.esc="cancelEdit"
                  ref="nameInput"
                />
                <span
                  v-else
                  class="form-name-text"
                  @click="startEdit(scope.row)"
                >
                  {{ scope.row.name }}
                </span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="updated_at" label="更新时间" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.updated_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="240" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="navigateToEdit(scope.row.id)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button size="small" @click="previewForm(scope.row)">
                <el-icon><View /></el-icon>
                预览
              </el-button>
              <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">
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

    <!-- 表单预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      :title="previewFormData ? `预览表单: ${previewFormData.name}` : '表单预览'"
      width="80%"
      height="80vh"
    >
      <div class="preview-container">
        <v-form-render 
          v-if="previewFormConfig" 
          :form-json="previewFormConfig"
          :form-data="{}"
          @submit="handleFormSubmit"
        />
        <div v-else class="empty-preview">
          表单配置加载失败
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { formConfigApi } from '../api/formService'
import {
  Refresh,
  Download,
  Search,
  Plus,
  Edit,
  Delete,
  View
} from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const formName = ref('')
const createTime = ref([])
const formList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const previewDialogVisible = ref(false)
const previewFormData = ref(null)
const previewFormConfig = ref(null)
const editingId = ref(null)
const editingName = ref('')
const nameInput = ref(null)

// 导航到表单设计页面
const navigateToDesign = () => {
  router.push('/form/design')
}

// 导航到表单编辑页面
const navigateToEdit = (id) => {
  router.push(`/form/design/${id}`)
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

// 获取表单列表
const fetchForms = async () => {
  try {
    const data = await formConfigApi.getAll()
    formList.value = data
    total.value = data.length
  } catch (error) {
    console.error('获取表单列表失败', error)
    formList.value = []
    total.value = 0
    ElMessage.error('获取表单列表失败')
  }
}

// 删除表单
const handleDelete = async (id) => {
  try {
    await formConfigApi.delete(id)
    ElMessage.success('表单删除成功')
    fetchForms()
  } catch (error) {
    console.error('删除表单失败', error)
    ElMessage.error('删除表单失败')
  }
}

// 预览表单
const previewForm = (form) => {
  try {
    previewFormData.value = form
    previewFormConfig.value = JSON.parse(form.config)
    previewDialogVisible.value = true
  } catch (error) {
    console.error('预览表单失败', error)
    ElMessage.error('预览表单失败')
  }
}

// 处理表单提交
const handleFormSubmit = (data) => {
  console.log('表单提交数据', data)
  ElMessage.success('表单提交成功！\n' + JSON.stringify(data, null, 2))
}

// 开始编辑表单名称
const startEdit = (form) => {
  editingId.value = form.id
  editingName.value = form.name
  // 使用nextTick确保输入框已渲染，然后聚焦
  nextTick(() => {
    if (nameInput.value) {
      nameInput.value.focus()
    }
  })
}

// 保存表单名称
const saveFormName = async (id) => {
  try {
    if (editingName.value.trim() === '') {
      ElMessage.warning('表单名称不能为空')
      return
    }
    
    // 调用API更新表单名称
    const updatedForm = await formConfigApi.update(id, {
      name: editingName.value.trim(),
      config: formList.value.find(f => f.id === id).config
    })
    
    // 更新本地数据
    const index = formList.value.findIndex(f => f.id === id)
    if (index !== -1) {
      formList.value[index].name = editingName.value.trim()
    }
    
    ElMessage.success('表单名称更新成功')
    editingId.value = null
  } catch (error) {
    console.error('更新表单名称失败', error)
    ElMessage.error('更新表单名称失败')
  }
}

// 取消编辑
const cancelEdit = () => {
  editingId.value = null
  editingName.value = ''
}

// 格式化时间，精确到秒
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

// 初始化
onMounted(() => {
  fetchForms()
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

/* 预览容器 */
.preview-container {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  min-height: 400px;
}

.empty-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  background: white;
  border: 2px dashed #ddd;
  border-radius: 4px;
  color: #999;
  font-size: 16px;
}
</style>
