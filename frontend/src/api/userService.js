import apiClient from './axiosConfig'

const API_BASE_URL = '/api/auth'

/**
 * 用户管理API服务
 */
export const userApi = {
  /**
   * 获取用户列表
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getAll: (params = {}) => {
    return apiClient.get(`${API_BASE_URL}/users/`, { params })
      .then(response => response.data)
  },
  
  /**
   * 根据ID获取用户详情
   * @param {number} id - 用户ID
   * @returns {Promise}
   */
  getById: (id) => {
    return apiClient.get(`${API_BASE_URL}/users/${id}/`)
      .then(response => response.data)
  },
  
  /**
   * 创建用户
   * @param {Object} userData - 用户数据
   * @returns {Promise}
   */
  create: (userData) => {
    return apiClient.post(`${API_BASE_URL}/users/`, userData)
      .then(response => response.data)
  },
  
  /**
   * 更新用户
   * @param {number} id - 用户ID
   * @param {Object} userData - 用户数据
   * @returns {Promise}
   */
  update: (id, userData) => {
    return apiClient.put(`${API_BASE_URL}/users/${id}/`, userData)
      .then(response => response.data)
  },
  
  /**
   * 删除用户
   * @param {number} id - 用户ID
   * @returns {Promise}
   */
  delete: (id) => {
    return apiClient.delete(`${API_BASE_URL}/users/${id}/`)
      .then(response => response.data)
  },
  
  /**
   * 用户登录
   * @param {Object} credentials - 登录凭证
   * @returns {Promise}
   */
  login: (credentials) => {
    return apiClient.post(`${API_BASE_URL}/login/`, credentials)
      .then(response => response.data)
  },
  
  /**
   * 用户注册
   * @param {Object} userData - 用户数据
   * @returns {Promise}
   */
  register: (userData) => {
    return apiClient.post(`${API_BASE_URL}/register/`, userData)
      .then(response => response.data)
  },
  
  /**
   * 获取当前用户信息
   * @returns {Promise}
   */
  getProfile: () => {
    return apiClient.get(`${API_BASE_URL}/profile/`)
      .then(response => response.data)
  },
  
  /**
   * 修改密码
   * @param {Object} passwordData - 密码数据
   * @returns {Promise}
   */
  changePassword: (passwordData) => {
    return apiClient.put(`${API_BASE_URL}/change-password/`, passwordData)
      .then(response => response.data)
  }
}
