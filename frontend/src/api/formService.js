import apiClient from './axiosConfig'

// 表单配置相关API
export const formConfigApi = {
  // 获取所有表单配置
  getAll: async () => {
    try {
      const response = await apiClient.get('/api/form-configs/')
      return response.data
    } catch (error) {
      console.error('获取表单配置失败', error)
      throw error
    }
  },

  // 获取单个表单配置
  getById: async (id) => {
    try {
      const response = await apiClient.get(`/api/form-configs/${id}/`)
      return response.data
    } catch (error) {
      console.error('获取表单配置失败', error)
      throw error
    }
  },

  // 创建新表单配置
  create: async (formData) => {
    try {
      const response = await apiClient.post('/api/form-configs/', formData)
      return response.data
    } catch (error) {
      console.error('创建表单配置失败', error)
      throw error
    }
  },

  // 更新表单配置
  update: async (id, formData) => {
    try {
      const response = await apiClient.put(`/api/form-configs/${id}/`, formData)
      return response.data
    } catch (error) {
      console.error('更新表单配置失败', error)
      throw error
    }
  },

  // 删除表单配置
  delete: async (id) => {
    try {
      await apiClient.delete(`/api/form-configs/${id}/`)
      return true
    } catch (error) {
      console.error('删除表单配置失败', error)
      throw error
    }
  }
}

export default apiClient
