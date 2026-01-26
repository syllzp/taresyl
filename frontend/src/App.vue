<template>
  <div class="app-container">
    <h1>低代码表单设计器</h1>
    <div class="app-content">
      <div class="designer-section">
        <h2>表单设计器</h2>
        <v-form-design 
          ref="designerRef" 
          :disabled="false"
          :height="600"
        />
        <div class="designer-actions">
          <button @click="saveForm" class="action-btn save-btn">保存表单</button>
          <button @click="loadForm" class="action-btn load-btn">加载表单</button>
          <button @click="clearForm" class="action-btn clear-btn">清空表单</button>
        </div>
      </div>
      <div class="preview-section">
        <h2>表单预览</h2>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { VFormDesign, VFormRender } from 'vform3-builds'
import axios from 'axios'

// 配置axios默认值
axios.defaults.baseURL = 'http://localhost:8000'

const designerRef = ref(null)
const formConfig = ref(null)
const formData = ref({})
const formId = ref(null)

// 保存表单配置
const saveForm = async () => {
  try {
    const config = designerRef.value.getFormConfig()
    if (!config) return
    
    if (formId.value) {
      // 更新表单
      const response = await axios.put(`/api/form-configs/${formId.value}/`, { config: JSON.stringify(config) })
      console.log('表单更新成功', response.data)
    } else {
      // 创建新表单
      const response = await axios.post('/api/form-configs/', { config: JSON.stringify(config), name: '新表单' })
      formId.value = response.data.id
      console.log('表单保存成功', response.data)
    }
  } catch (error) {
    console.error('保存表单失败', error)
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
    }
  } catch (error) {
    console.error('加载表单失败', error)
  }
}

// 清空表单
const clearForm = () => {
  designerRef.value.clearFormConfig()
  formConfig.value = null
  formId.value = null
  formData.value = {}
}

// 处理表单提交
const handleSubmit = (data) => {
  console.log('表单提交数据', data)
  alert('表单提交成功！\n' + JSON.stringify(data, null, 2))
}

// 初始化
onMounted(() => {
  loadForm()
})
</script>

<style scoped>
.app-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.app-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.designer-section, .preview-section {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-top: 0;
  color: #555;
  font-size: 18px;
  margin-bottom: 15px;
}

.designer-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.action-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.save-btn {
  background-color: #409eff;
  color: white;
}

.save-btn:hover {
  background-color: #66b1ff;
}

.load-btn {
  background-color: #67c23a;
  color: white;
}

.load-btn:hover {
  background-color: #85ce61;
}

.clear-btn {
  background-color: #f56c6c;
  color: white;
}

.clear-btn:hover {
  background-color: #f78989;
}

.empty-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 600px;
  background: white;
  border: 2px dashed #ddd;
  border-radius: 4px;
  color: #999;
  font-size: 16px;
}
</style>