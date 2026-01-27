import apiClient from './axiosConfig'

const API_BASE_URL = '/api/system'

/**
 * 系统日志API服务
 */
export const systemLogApi = {
  /**
   * 获取系统日志列表
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getAll: (params = {}) => {
    return apiClient.get(`${API_BASE_URL}/logs/`, { params })
      .then(response => response.data)
  },
  
  /**
   * 根据ID获取系统日志详情
   * @param {number} id - 日志ID
   * @returns {Promise}
   */
  getById: (id) => {
    return apiClient.get(`${API_BASE_URL}/logs/${id}/`)
      .then(response => response.data)
  },
  
  /**
   * 创建系统日志
   * @param {Object} logData - 日志数据
   * @returns {Promise}
   */
  create: (logData) => {
    return apiClient.post(`${API_BASE_URL}/logs/`, logData)
      .then(response => response.data)
  },
  
  /**
   * 更新系统日志
   * @param {number} id - 日志ID
   * @param {Object} logData - 日志数据
   * @returns {Promise}
   */
  update: (id, logData) => {
    return apiClient.put(`${API_BASE_URL}/logs/${id}/`, logData)
      .then(response => response.data)
  },
  
  /**
   * 删除系统日志
   * @param {number} id - 日志ID
   * @returns {Promise}
   */
  delete: (id) => {
    return apiClient.delete(`${API_BASE_URL}/logs/${id}/`)
      .then(response => response.data)
  }
}
