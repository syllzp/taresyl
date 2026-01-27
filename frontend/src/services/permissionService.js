import apiClient from '../api/axiosConfig'

// 权限服务
const permissionService = {
  // 用户权限缓存
  userPermissions: [],
  
  // 获取用户权限
  async getPermissions() {
    try {
      const response = await apiClient.get('/api/auth/user-permissions/')
      this.userPermissions = response.data
      return this.userPermissions
    } catch (error) {
      console.error('获取用户权限失败', error)
      this.userPermissions = []
      return []
    }
  },
  
  // 检查用户是否拥有指定权限
  hasPermission(codename) {
    return this.userPermissions.some(permission => permission.codename === codename)
  },
  
  // 检查用户是否拥有多个权限中的任意一个
  hasAnyPermission(codenames) {
    return codenames.some(codename => this.hasPermission(codename))
  },
  
  // 检查用户是否拥有所有指定权限
  hasAllPermissions(codenames) {
    return codenames.every(codename => this.hasPermission(codename))
  },
  
  // 刷新用户权限
  async refreshPermissions() {
    return this.getPermissions()
  }
}

export default permissionService
