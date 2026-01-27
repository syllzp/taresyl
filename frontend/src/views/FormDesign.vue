<template>
  <div class="form-design-container">
    <div class="content-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>表单管理</el-breadcrumb-item>
        <el-breadcrumb-item>{{ isEditing ? '编辑表单' : '新建表单' }}</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="content-actions">
        <el-button size="small" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
      </div>
    </div>

    <div class="designer-container">
      <div class="designer-section">
        <div class="designer-header">
          <el-button type="primary" @click="saveForm">
            <el-icon><Check /></el-icon>
            保存表单
          </el-button>
        </div>
        <v-form-designer 
          ref="designerRef" 
          :disabled="false"
          :height="500"
          :title="false"
        />

      </div>
      <div class="preview-section">
        <h3>表单预览</h3>
        <v-form-render 
          v-if="formJson" 
          :form-json="formJson"
          :form-data="formData"
          @submit="handleSubmit"
        />
        <div v-else class="empty-preview">
          请先设计表单
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { formConfigApi } from '../api/formService'
import {
  ArrowLeft,
  Check,
  Download,
  Delete
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

// 响应式数据
const designerRef = ref(null)
const formJson = ref(null)
const formData = ref({})
const formId = ref(null)
const isEditing = ref(false)

// 返回上一页
const goBack = () => {
  router.push('/')
}

// 保存表单配置
const saveForm = async () => {
  try {
    const config = designerRef.value.getFormJson()
    if (!config) {
      ElMessage.warning('请先设计表单')
      return
    }
    
    // 生成4位UUID
    const generateShortUUID = () => {
      return Math.random().toString(36).substring(2, 6).toUpperCase()
    }
    
    const formData = {
      name: isEditing.value ? `表单${formId.value}` : `新表单_${generateShortUUID()}`,
      config: JSON.stringify(config)
    }
    
    if (isEditing.value) {
      // 更新表单
      const response = await formConfigApi.update(formId.value, formData)
      console.log('表单更新成功', response)
      ElMessage.success('表单更新成功')
    } else {
      // 创建新表单
      const response = await formConfigApi.create(formData)
      formId.value = response.id
      isEditing.value = true
      console.log('表单保存成功', response)
      ElMessage.success('表单保存成功')
    }
  } catch (error) {
    console.error('保存表单失败', error)
    ElMessage.error('保存表单失败')
  }
}



// 处理表单提交
const handleSubmit = (data) => {
  console.log('表单提交数据', data)
  ElMessage.success('表单提交成功！\n' + JSON.stringify(data, null, 2))
}

// 初始化
const initForm = async () => {
  const id = route.params.id
  if (id) {
    try {
      isEditing.value = true
      formId.value = id
      const form = await formConfigApi.getById(id)
      formJson.value = JSON.parse(form.config)
      designerRef.value.setFormJson(formJson.value)
      console.log('表单加载成功', form)
    } catch (error) {
      console.error('加载表单失败', error)
      ElMessage.error('加载表单失败')
    }
  }
}

onMounted(() => {
  initForm()
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

/* 设计器容器 */
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

.designer-header {
  margin-bottom: 15px;
  display: flex;
  justify-content: flex-start;
}

.preview-section h3 {
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

/* 设计器操作按钮 */
.designer-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

/* 空预览状态 */
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

/* 响应式设计 */
@media (max-width: 768px) {
  .designer-container {
    grid-template-columns: 1fr;
  }
}
</style>
